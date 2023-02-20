from pathlib import Path
import sys
import os

from PyQt6 import QtCore, QtGui, QtWidgets

from qt.qtui import Ui_MainWindow
from modules import mpv
from qt.playbackworker import PlaybackWorker
from qt.ingestworker import IngestWorker, ReprocessWorker
import qt.resources
from modules.eyedb import EyeDB
from modules.analyze import Analyze
from qt.processui import Ui_dialogProcessing
from qt.helpwindow import Ui_helpDialog
from qt.parameterwindow import ParameterWindow
from modules.export import DataExporter
from utils.fileutils import validate_import_folder
from utils.imageutils import create_video_overlay


class EyeMainWindow(Ui_MainWindow):
    def __init__(self, main_window: QtWidgets.QMainWindow, app: QtWidgets.QApplication) -> None:
        self.app = app
        self.main_window = main_window
        self._db_path = Path(__file__).parent.parent.parent / 'data' / 'eye.db'
        self._db = EyeDB(self._db_path)
        self._csv = DataExporter(self._db)
        self._analyze = Analyze
        self.setupUi(self.main_window)
        self._setup_custom_ui()
        self._connect_events()

    def _setup_custom_ui(self):
        self.main_window.setWindowTitle('eyeplus')
        self.main_window.setWindowIcon(
            QtGui.QIcon(QtGui.QPixmap(':/icons/eye.svg')))
        self._thread_pool = QtCore.QThreadPool()
        self._error_box = QtWidgets.QErrorMessage(self.main_window)
        self._error_box.setWindowIcon(QtGui.QIcon(
            QtGui.QPixmap(':/icons/alert-triangle.svg')))
        self._error_box.setWindowTitle('ERROR: eyeplus')
        self.parameter_window = ParameterWindow(self.main_window)
        self.tabWidgetMain.setCurrentIndex(0)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)
        self.actionPlay.setEnabled(False)
        self.toolBar.setVisible(False)
        self.actionMute.setEnabled(False)
        self.actionMute.setEnabled(False)
        self.actionAdjust.setEnabled(False)
        self.actionRecalculate.setEnabled(False)
        self._videos = {}
        self._selected_run = 0
        self._roll_offset = 90
        self._pitch_multi = 1.0
        self._reset_stats_text()
        self._populate_runs_tables()
        self._init_input_file_chooser()
        self._init_output_file_chooser()
        self._init_output_dir_chooser()
        self._init_input_dir_chooser()
        self._init_status_bar()
        self._setup_loading_dialog()
        self._setup_help_window()

    def _connect_events(self):
        self.horizontalSliderSeek.sliderMoved.connect(self._seekbar_moved)
        self.horizontalSliderSeek.sliderReleased.connect(self._seekbar_moved)
        self.actionPlay.triggered.connect(self._play_clicked)
        self.actionExit.triggered.connect(self._safe_quit_menu)
        self.main_window.closeEvent = self._safe_quit_x
        self.actionPause.triggered.connect(self._pause_clicked)
        self.actionStop.triggered.connect(self._stop_clicked)
        self.tabWidgetMain.currentChanged.connect(self._main_tab_changed)
        self.pushButtonExportDisplayed.clicked.connect(
            self._export_single_clicked)
        self.actionImport_Zip.triggered.connect(self._import_zip_clicked)
        self.actionExport_All_Data.triggered.connect(self._export_all_clicked)
        self.pushButtonExportAll.clicked.connect(self._export_all_clicked)
        self.horizontalSliderVolume.sliderReleased.connect(self._change_volume)
        self.actionMute.triggered.connect(self._mute_clicked)
        self.actionImport_Folder.triggered.connect(self._import_dir_clicked)
        self.tableViewRuns.clicked.connect(
            self._table_item_single_clicked)
        self.pushButtonOpenReview.clicked.connect(self._open_review_clicked)
        self.actionAbout.triggered.connect(self._about_clicked)
        self.actionUsage.triggered.connect(self._usage_clicked)
        self.actionReadme.triggered.connect(self._readme_clicked)
        self.pushButtonRecalculateOne.clicked.connect(
            self._redo_single_calc_clicked)
        self.actionAdjust.triggered.connect(self._show_parameter_window)
        self.parameter_window.ui.pushButtonApply.clicked.connect(
            self._update_parameters)
        self.lineEditFilter.textChanged.connect(
            self._filter_runs)
        self.actionRecalculate.triggered.connect(
            self._update_fusion)

    def _setup_video(self):
        if 'playback_worker' in self.__dict__:
            self._stop_clicked()
        self.player = mpv.MPV(wid=str(int(self.widgetVideoContainer.winId())),
                              log_handler=print,
                              loglevel='error',
                              force_window='yes',
                              background="#FFFFFF")
        current_video = self._videos[self._selected_run]
        self.playback_worker = PlaybackWorker(
            player=self.player, video=current_video)
        self.playback_worker.signals.playing.connect(
            self._playing_started_callback)
        self.playback_worker.signals.progress.connect(
            self._playing_update_progress_callback)
        self.playback_worker.signals.finished.connect(
            self._playing_complete_callback)

    def _setup_loading_dialog(self):
        self.processing_dialog = QtWidgets.QDialog(parent=self.main_window)
        self.process_ui = Ui_dialogProcessing()
        self.process_ui.setupUi(self.processing_dialog)

    def _setup_help_window(self):
        self.help_window = QtWidgets.QDialog(parent=self.main_window)
        self.help_display = Ui_helpDialog()
        self.help_display.setupUi(self.help_window)
        self.help_window.setWindowIcon(
            QtGui.QIcon(QtGui.QPixmap(':/icons/life-buoy.svg')))

    def _playing_started_callback(self):
        if self.actionMute.isChecked():
            self.player.command('set', 'mute', 'yes')
        self.actionPause.setChecked(False)
        self.playback_worker.timer.start()
        self.horizontalSliderSeek.setEnabled(True)
        self.actionPlay.setEnabled(False)
        self.actionPause.setEnabled(True)
        self.actionStop.setEnabled(True)
        self.actionMute.setEnabled(True)
        self.actionAdjust.setEnabled(True)
        self.actionRecalculate.setEnabled(True)
        self.horizontalSliderVolume.setEnabled(True)
        self.actionMute.setEnabled(True)
        self._overlay = self.player.create_image_overlay()
        self._update_status('Playback started')

    def _playing_update_progress_callback(self, progress: int):
        if not self.horizontalSliderSeek.isSliderDown():
            self.horizontalSliderSeek.setSliderPosition(progress)
        if not self.player.pause:
            curr_timestamp = round(self.player.time_pos, 1)
            closest_fusion = self._fusion_timestamps[-1]
            for time in self._fusion_timestamps:
                if time >= curr_timestamp:
                    closest_fusion = time
                    break
            if self._overlay.overlay_id:
                self._overlay.remove()

            gaze_x = self._tree_predicted2d[curr_timestamp][0]
            gaze_y = self._tree_predicted2d[curr_timestamp][1]
            gaze_side = self._tree_predicted3d[curr_timestamp][0]
            gaze_vert = self._tree_predicted3d[curr_timestamp][1]
            gaze_dist = self._tree_predicted3d[curr_timestamp][2]
            y_intercept = self._fusion_data[closest_fusion]['y_intercept']
            x_intercept = self._fusion_data[closest_fusion]['x_intercept']
            slope = self._fusion_data[closest_fusion]['slope']
            roll = self._fusion_data[closest_fusion]['roll']
            pitch = self._fusion_data[closest_fusion]['pitch']

            roll += self._roll_offset
            pitch *= self._pitch_multi

            img, pos_x, pos_y = create_video_overlay(
                self.player.osd_dimensions, gaze_x, gaze_y, y_intercept, x_intercept, slope, roll, pitch)
            self._overlay.update(img, pos=(pos_x, pos_y))
            status = self._analyze.test_check(
                slope, y_intercept, gaze_x, gaze_y, gaze_dist)
            self.plainTextEditStats.setPlainText(
                f'RunID      : {self._selected_run}\n'
                f'Title      : {self._all_runs_list[self._selected_run -1]["tags"]}\n'
                f'Timestamp  : {self.player.time_pos:.2f}\n'
                f'Duration   : {self.player.duration:.2f}\n\n'
                f'Gaze X     : {gaze_x:.4f}\n'
                f'Gaze Y     : {gaze_y:.4f}\n\n'
                # f'Heading    : {self._fusion_data[closest_fusion]["heading"]:.4f}\n'
                f'Roll       : {roll:.4f}\n'
                f'Pitch      : {pitch:.4f}\n\n'
                f'x_intercept: {x_intercept:.4f}\n'
                f'y_intercept: {y_intercept:.4f}\n'
                f'slope      : {slope:.4f}\n\n'
                f'Gaze3d X   : {gaze_side:.4f}\n'
                f'Gaze3d Y   : {gaze_vert:.4f}\n'
                f'Gaze3d Z   : {gaze_dist:.4f}\n\n'
                f'Obervation : {status}\n'
            )

    def _playing_complete_callback(self):
        if self._overlay.overlay_id:
            self._overlay.remove()
        self.playback_worker.timer.stop()
        self.horizontalSliderSeek.setEnabled(False)
        self.horizontalSliderSeek.setSliderPosition(0)
        self.actionPlay.setEnabled(False)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)
        self.actionMute.setEnabled(False)
        self.actionAdjust.setEnabled(False)
        self.actionRecalculate.setEnabled(False)
        self.horizontalSliderVolume.setEnabled(False)
        self.actionMute.setEnabled(False)
        self._reset_stats_text()
        self._update_status('Playback stopped')

    def _seekbar_moved(self):
        time_to_seek = self.horizontalSliderSeek.sliderPosition() * \
            self.player.duration / 1000
        self.player.seek(max(time_to_seek, 1), reference='absolute')

    def _play_clicked(self):
        self.parameter_window.set_values(self._roll_offset, self._pitch_multi)
        self._tree_predicted2d = self._db.get_pgazed2d_data(self._selected_run)
        self._tree_predicted3d = self._db.get_pgazed3d_data(self._selected_run)
        self._fusion_data = self._db.get_fusion_data(self._selected_run)
        self._fusion_timestamps = list(self._fusion_data.keys())
        self._thread_pool.start(self.playback_worker)

    def _safe_quit_x(self, event):
        if 'player' in self.__dict__:
            self.player.terminate()
            self.player.wait_for_shutdown()
        event.accept()

    def _safe_quit_menu(self):
        if 'player' in self.__dict__:
            self.player.terminate()
            self.player.wait_for_shutdown()
        sys.exit(0)

    def _pause_clicked(self):
        if self.player.pause:
            self.player.command('set', 'pause', 'no')
        else:
            self.player.command('set', 'pause', 'yes')

    def _stop_clicked(self):
        self.parameter_window.hide()
        self.parameter_window.reset()
        self.player.terminate()
        self.player.wait_for_shutdown()
        self._playing_complete_callback()

    def _main_tab_changed(self):
        if self.tabWidgetMain.currentIndex() == 1:
            self.toolBar.setVisible(True)
        elif self.tabWidgetMain.currentIndex() == 0:
            self.toolBar.setVisible(False)
        elif self.tabWidgetMain.currentIndex() == 2:
            self.toolBar.setVisible(False)

        if self.parameter_window.isVisible():
            self.parameter_window.hide()
            self.parameter_window.reset()

    def _reset_stats_text(self):
        self.plainTextEditStats.setPlainText('Start playback to see info.')

    def _populate_runs_tables(self):
        self.tableViewRuns.setSortingEnabled(False)
        self._all_runs_list = self._db.get_all_runs()
        self._all_runs_dict = {}
        for run in self._all_runs_list:
            self._all_runs_dict[int(run['id'])] = {
                'process_date': run['processdate'],
                'import_date': run['importdate'],
                'tags': run['tags']
            }
        run_count = len(self._all_runs_list)
        if run_count > 0:
            self.tabWidgetMain.setEnabled(True)
            self._runs_model = QtGui.QStandardItemModel(run_count, 4)
            self._runs_model.setHorizontalHeaderLabels(
                ['ID', 'Date', 'Processed', 'Title'])
            for index, run in enumerate(self._all_runs_list):
                self._videos[run['id']] = run['video']
                new_id = QtGui.QStandardItem(str(run['id']))
                new_import_date = QtGui.QStandardItem(str(run['importdate']))
                new_process_date = QtGui.QStandardItem(str(run['processdate']))
                new_title = QtGui.QStandardItem(str(run['tags']))
                self._runs_model.setItem(index, 0, new_id)
                self._runs_model.setItem(index, 1, new_import_date)
                self._runs_model.setItem(index, 2, new_process_date)
                self._runs_model.setItem(index, 3, new_title)
            self._title_filter_model = QtCore.QSortFilterProxyModel()
            self._title_filter_model.setSourceModel(self._runs_model)
            self._title_filter_model.setFilterKeyColumn(3)
            self._title_filter_model.setFilterCaseSensitivity(
                QtCore.Qt.CaseSensitivity.CaseInsensitive)
            self.tableViewRuns.setModel(self._title_filter_model)
            self.tableViewRuns.resizeColumnsToContents()
            self.tableViewRuns.resizeRowsToContents()
            self.tableViewRuns.setSortingEnabled(True)
            self.tableViewRuns.sortByColumn(
                0, QtCore.Qt.SortOrder.AscendingOrder)
            self.tableViewRuns.selectRow(0)
            self._selected_run = 1
            self._roll_offset = self._all_runs_list[0]['roll_offset']
            self._pitch_multi = self._all_runs_list[0]['pitch_multi']
        else:
            self.tabWidgetMain.setEnabled(False)
            QtWidgets.QMessageBox
            message_box = QtWidgets.QMessageBox(
                text='It looks like this is your first time using eyeplus. Head over to File > Import... to get started, or check the documentation under Help.', parent=self.main_window)
            message_box.setWindowIcon(QtGui.QIcon(
                QtGui.QPixmap(':/icons/info.svg')))
            message_box.setWindowTitle('Welcome to eyeplus!')
            message_box.exec()

    def _table_item_single_clicked(self, index: QtCore.QModelIndex) -> None:
        original_index = self._title_filter_model.mapToSource(index)
        runid_index = self._runs_model.index(original_index.row(), 0)
        self._selected_run = int(self._runs_model.itemData(runid_index)[0])
        self.labelSummaryTitle.setText(
            f'Summary for Run ID {self._selected_run}')
        self.labelSummaryDate.setText(
            f'Date: {self._all_runs_dict[self._selected_run]["import_date"]}')
        self.labelSummaryProcessDate.setText(
            f'Processed: {self._all_runs_dict[self._selected_run]["process_date"]}')
        self.labelSummaryTag.setText(
            f'Title: {self._all_runs_dict[self._selected_run]["tags"]}')
        self._update_status(
            f'Successfully loaded summary for runid {self._selected_run}')
        # code to show summary here

    def _open_review_clicked(self) -> None:
        self._gaze = self._db.get_gaze_data(self._selected_run)
        self._roll_offset, self._pitch_multi = self._db.get_parameters(
            self._selected_run)
        self._setup_video()
        self.actionPlay.setEnabled(True)
        self.tabWidgetMain.tabBar().setHidden(False)
        self.tabWidgetMain.tabBar().setEnabled(True)
        self.tabWidgetMain.setCurrentIndex(1)
        self._update_status(
            f'Successfully opened review for runid {self._selected_run}')

    def _init_input_file_chooser(self):
        self.input_file_chooser = QtWidgets.QFileDialog(self.main_window)
        self.input_file_chooser.setDirectory(os.path.expanduser('~'))
        self.input_file_chooser.setFileMode(
            QtWidgets.QFileDialog.FileMode.ExistingFiles)
        self.input_file_chooser.setViewMode(
            QtWidgets.QFileDialog.ViewMode.List)
        self.input_file_chooser.setNameFilter('zip (*.zip)')
        self.input_file_chooser.accepted.connect(self._user_chosen_zip)

    def _init_input_dir_chooser(self):
        self.input_dir_chooser = QtWidgets.QFileDialog(self.main_window)
        self.input_dir_chooser.setFileMode(
            QtWidgets.QFileDialog.FileMode.Directory)
        self.input_dir_chooser.setOption(
            QtWidgets.QFileDialog.Option.ShowDirsOnly, True)
        self.input_dir_chooser.setDirectory(os.path.expanduser('~'))
        self.input_dir_chooser.setViewMode(
            QtWidgets.QFileDialog.ViewMode.List)
        self.input_dir_chooser.setAcceptMode(
            QtWidgets.QFileDialog.AcceptMode.AcceptOpen)
        self.input_dir_chooser.accepted.connect(self._user_chosen_input_dir)

    def _init_output_file_chooser(self):
        self.output_file_chooser = QtWidgets.QFileDialog(self.main_window)
        self.output_file_chooser.setDirectory(os.path.expanduser('~'))
        self.output_file_chooser.setFileMode(
            QtWidgets.QFileDialog.FileMode.AnyFile)
        self.output_file_chooser.setViewMode(
            QtWidgets.QFileDialog.ViewMode.List)
        self.output_file_chooser.setAcceptMode(
            QtWidgets.QFileDialog.AcceptMode.AcceptSave)
        self.output_file_chooser.setNameFilter('csv (*.csv)')
        self.output_file_chooser.accepted.connect(self._user_chosen_csv)

    def _init_output_dir_chooser(self):
        self.output_dir_chooser = QtWidgets.QFileDialog(self.main_window)
        self.output_dir_chooser.setFileMode(
            QtWidgets.QFileDialog.FileMode.Directory)
        self.output_dir_chooser.setOption(
            QtWidgets.QFileDialog.Option.ShowDirsOnly, True)
        self.output_dir_chooser.setDirectory(os.path.expanduser('~'))
        self.output_dir_chooser.setViewMode(
            QtWidgets.QFileDialog.ViewMode.List)
        self.output_dir_chooser.setAcceptMode(
            QtWidgets.QFileDialog.AcceptMode.AcceptOpen)
        self.output_dir_chooser.accepted.connect(self._user_chosen_output_dir)

    def _export_single_clicked(self):
        self.output_file_chooser.exec()

    def _import_zip_clicked(self):
        self.input_file_chooser.exec()

    def _export_all_clicked(self):
        self.output_dir_chooser.exec()

    def _import_dir_clicked(self):
        self.input_dir_chooser.exec()

    def _user_chosen_csv(self):
        user_selected_file = self.output_file_chooser.selectedFiles()
        if len(user_selected_file) > 0 and user_selected_file[0] != '':
            csv_to_save = Path(user_selected_file[0])
            self._csv.export_single(csv_to_save, self._selected_run)

    def _user_chosen_output_dir(self):
        user_selected_dir = self.output_dir_chooser.selectedFiles()
        if len(user_selected_dir) > 0 and user_selected_dir[0] != '':
            dir_to_save = Path(user_selected_dir[0])
            self._csv.export_all(dir_to_save)

    def _user_chosen_input_dir(self):
        user_selected_dir = self.input_dir_chooser.selectedFiles()
        if len(user_selected_dir) > 0 and user_selected_dir[0] != '':
            dir_to_load = Path(user_selected_dir[0])
            found_items = validate_import_folder(dir_to_load)
        else:
            found_items = []
        if len(found_items) <= 0:
            self._error_box.showMessage(
                'Error: You selected no directory to import.')
        else:
            self._ingest_data(found_items, 'dir')

    def _user_chosen_zip(self):
        user_selected_zips = self.input_file_chooser.selectedFiles()
        if len(user_selected_zips) > 0:
            zips_to_import = [Path(x)
                              for x in user_selected_zips if x != '']
            self._ingest_data(zips_to_import, 'zip')
        else:
            self._error_box.showMessage(
                'Error: You selected no zip file to import.')

    def _ingest_data(self, found_items: list[Path], ftype: str):
        try:
            ingest_worker = IngestWorker(self._db_path, found_items, ftype)
            ingest_worker.signals.started.connect(
                self._progress_dialog_start)
            ingest_worker.signals.progress.connect(
                self._progress_dialog_update)
            ingest_worker.signals.finished.connect(
                self._progress_dialog_finish)
            self._thread_pool.start(ingest_worker)
        except FileExistsError:
            self._error_box.showMessage(
                'Error: You have attempted to import one or more runs which already have been imported.')

    def _init_status_bar(self) -> None:
        """Initializes status bar widgets, since Qt Creator doesn't allow
            this
        """
        self.labelPermStatusBar = QtWidgets.QLabel()
        self.labelPermStatusBar.setObjectName('labelPermStatusBar')
        self.horizontalSliderVolume = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderVolume.setOrientation(
            QtCore.Qt.Orientation.Horizontal)
        self.horizontalSliderVolume.setObjectName('horizontalSliderVolume')
        self.horizontalSliderVolume.setToolTip('Volume')
        self.horizontalSliderVolume.setFixedWidth(100)
        self.horizontalSliderVolume.setRange(0, 100)
        self.statusbar.addPermanentWidget(self.labelPermStatusBar)
        self.statusbar.addPermanentWidget(self.horizontalSliderVolume)
        self.labelPermStatusBar.setText('Volume')
        self.horizontalSliderVolume.setValue(100)
        self.horizontalSliderVolume.setEnabled(False)

    def _change_volume(self):
        volume_to_set = self.horizontalSliderVolume.value()
        self.player.command(
            'set', 'volume', volume_to_set)
        if volume_to_set > 0:
            if self.player.mute:
                self.actionMute.setChecked(False)
                self.player.command('set', 'mute', 'no')

    def _mute_clicked(self):
        if self.player.mute:
            self.player.command('set', 'mute', 'no')
        else:
            self.player.command('set', 'mute', 'yes')

    def _update_status(self, message: str) -> None:
        self.statusbar.showMessage(message, 2500)

    def _progress_dialog_start(self) -> None:
        self._update_status('Beginning import and processing...')
        self.process_ui.labelProcessing.setText('Warming up...')
        self.process_ui.progressBarProcessing.setValue(0)
        self.main_window.hide()
        self.processing_dialog.show()

    def _progress_dialog_update(self, message: str, progress: float) -> None:
        self.process_ui.labelProcessing.setText(message)
        self.process_ui.progressBarProcessing.setValue(int(progress * 100))

    def _progress_dialog_finish(self) -> None:
        self.processing_dialog.hide()
        self.main_window.show()
        self._populate_runs_tables()
        self._update_status(f'Successfully imported data')

    def _readme_clicked(self) -> None:
        self.help_window.setWindowTitle('README')
        readme = Path(__file__).parent.parent.parent / 'README.md'
        self.help_display.textBrowserDisplay.setMarkdown(readme.read_text())
        self.help_window.resize(600, 700)
        self.help_window.show()

    def _usage_clicked(self) -> None:
        self.help_window.setWindowTitle('Usage')
        usage = Path(__file__).parent.parent.parent / 'docs' / 'usage.md'
        self.help_display.textBrowserDisplay.setMarkdown(usage.read_text())
        self.help_window.resize(600, 700)
        self.help_window.show()

    def _about_clicked(self) -> None:
        self.help_window.setWindowTitle('About')
        about = Path(__file__).parent.parent.parent / 'docs' / 'about.md'
        self.help_display.textBrowserDisplay.setMarkdown(about.read_text())
        self.help_window.resize(400, 300)
        self.help_window.show()

    def _redo_single_calc_clicked(self) -> None:
        runs_to_redo = [self._selected_run]
        ingest_worker = ReprocessWorker(
            self._db_path, runs_to_redo, self._roll_offset, self._pitch_multi)
        ingest_worker.signals.started.connect(
            self._reprocess_started)
        ingest_worker.signals.progress.connect(
            self._reprocess_dialog_update)
        ingest_worker.signals.finished.connect(
            self._reprocess_finished)
        self._thread_pool.start(ingest_worker)

    def _reprocess_started(self) -> None:
        self._update_status('Beginning to reprocess data')
        self.process_ui.labelProcessing.setText('Warming up...')
        self.process_ui.progressBarProcessing.setValue(0)
        self.main_window.hide()
        self.processing_dialog.show()

    def _reprocess_dialog_update(self, message: str, progress: float) -> None:
        self.process_ui.labelProcessing.setText(message)
        self.process_ui.progressBarProcessing.setValue(int(progress * 100))

    def _reprocess_finished(self) -> None:
        self.processing_dialog.hide()
        self.main_window.show()
        self._populate_runs_tables()
        self._update_status(f'Successfully imported data')
        self.tabWidgetMain.setCurrentIndex(0)

    def _show_parameter_window(self) -> None:
        self.parameter_window.set_values(self._roll_offset, self._pitch_multi)
        self.parameter_window.show()
        self.parameter_window.setFocus()
        self.parameter_window.move(250, 600)

    def _update_parameters(self) -> None:
        self._roll_offset = self.parameter_window.ui.horizontalSliderRollOffset.value()
        self._pitch_multi = float(
            self.parameter_window.ui.horizontalSliderPitchMulti.value() / 1000)

    def _filter_runs(self, text: str) -> None:
        self._title_filter_model.setFilterRegularExpression(text)
        self.tableViewRuns.resizeColumnsToContents()
        self.tableViewRuns.resizeRowsToContents()

    def _update_fusion(self) -> None:
        self._stop_clicked()
        runs_to_redo = [self._selected_run]
        ingest_worker = ReprocessWorker(
            self._db_path, runs_to_redo, self._roll_offset, self._pitch_multi)
        ingest_worker.signals.started.connect(
            self._reprocess_started)
        ingest_worker.signals.progress.connect(
            self._reprocess_dialog_update)
        ingest_worker.signals.finished.connect(
            self._reprocess_finished)
        self._thread_pool.start(ingest_worker)
