from pathlib import Path
import sys
import os
import re
from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets

from qt.qtui import Ui_MainWindow
from modules import mpv
from qt.playbackworker import PlaybackWorker
from qt.ingestworker import IngestWorker, ReprocessWorker
import qt.resources
from modules.eyedb import EyeDB
from qt.processui import Ui_dialogProcessing
from qt.helpwindow import Ui_helpDialog
from qt.parameterwindow import ParameterWindow
from modules.export import DataExporter
from modules.visualize import TotalUpDown, CumulativeUpDown, PitchLive, HeatMap, TotalUpDownStacked, GazeLive, OverallGaze2DY, OverallUpAndDown, PitchHistogram
from utils.fileutils import validate_import_folder
from utils.imageutils import create_video_overlay
from utils.statutils import next_greatest_element, get_gaze_stats, get_fusion_stats


class EyeMainWindow(Ui_MainWindow):
    def __init__(self, main_window: QtWidgets.QMainWindow, app: QtWidgets.QApplication) -> None:
        self.app = app
        self.screen = self.app.screens()[0]
        self.main_window = main_window
        self._db_path = Path(__file__).parent.parent.parent / 'data' / 'eye.db'
        self._db = EyeDB(self._db_path)
        self._csv = DataExporter(self._db)
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
        self._videos = {}
        self._overall_selected_runs = []
        self._selected_run = 0
        self._pitch_offset = 0
        self._pitch_multi = 1.0
        self._horizon_offset = 0.0
        self._part_selection_enabled = False
        self._selected_start_time = -1.0
        self._selected_end_time = -1.0
        self._dpi = self.screen.logicalDotsPerInch()
        self._reset_stats_text()
        self._setup_visual_widgets()
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
        self.actionAdjust.triggered.connect(self._show_parameter_window)
        self.parameter_window.ui.pushButtonApply.clicked.connect(
            self._update_parameters)
        self.lineEditFilter.textChanged.connect(
            self._filter_runs)
        self.parameter_window.ui.pushButtonRecalculate.clicked.connect(
            self._update_fusion)
        self.horizontalScrollBarLongChart.sliderMoved.connect(
            self._overall_graphic_slider_moved)
        self.listWidgetOverallSelectRuns.itemSelectionChanged.connect(
            self._overall_run_selection_changed)
        self.lineEditStartTime.editingFinished.connect(self._verify_start_time)
        self.lineEditEndTime.editingFinished.connect(self._verify_end_time)
        self.pushButtonApplyParts.clicked.connect(self._apply_parts_clicked)

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
            player=self.player, video=current_video, start=self._selected_start_time, end=self._selected_end_time)
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

    def _play_clicked(self):
        self._visual_review_pitch.plot(
            self._fusion_data, self._fusion_timestamps)
        self._thread_pool.start(self.playback_worker)

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
        self.horizontalSliderVolume.setEnabled(True)
        self.actionMute.setEnabled(True)
        self._overlay = self.player.create_image_overlay()
        self._update_status('Playback started')

    def _playing_update_progress_callback(self, progress: int):
        if self.player.duration:
            if not self.horizontalSliderSeek.isSliderDown():
                self.horizontalSliderSeek.setSliderPosition(progress)
            if not self.player.pause:
                curr_timestamp = round(self.player.time_pos, 1)
                if curr_timestamp < self._first_timestamp:
                    curr_timestamp = self._first_timestamp
                elif curr_timestamp < self._last_timestamp:
                    self._stop_clicked
                self._visual_review_pitch.update_frame(curr_timestamp)
                self._visual_review_gaze_live.update_frame(curr_timestamp)
                if self.player.duration - self.player.time_pos <= 2:
                    curr_timestamp = curr_timestamp - 2
                closest_fusion = next_greatest_element(
                    curr_timestamp, self._fusion_timestamps)
                closest_distance = next_greatest_element(
                    curr_timestamp, self._gaze_distance_timestamps)

                if self._overlay.overlay_id:
                    self._overlay.remove()

                gaze_x = self._tree_predicted2d[curr_timestamp][0]
                gaze_y = self._tree_predicted2d[curr_timestamp][1]
                y_intercept = self._fusion_data[closest_fusion]['y_intercept']
                x_intercept = self._fusion_data[closest_fusion]['x_intercept']
                slope = self._fusion_data[closest_fusion]['slope']
                roll = self._fusion_data[closest_fusion]['roll']
                pitch = self._fusion_data[closest_fusion]['pitch']
                total_count = self._horizon[curr_timestamp]['total']
                up_count = self._horizon[curr_timestamp]['up_count']
                down_count = self._horizon[curr_timestamp]['down_count']
                percent_up = self._horizon[curr_timestamp]['percent_up']
                percent_down = self._horizon[curr_timestamp]['percent_down']
                currently_up = self._horizon[curr_timestamp]['currently_up']

                pitch -= self._pitch_offset
                pitch *= self._pitch_multi

                img, pos_x, pos_y = create_video_overlay(
                    self.player.osd_dimensions, gaze_x, gaze_y, y_intercept, x_intercept, slope, roll, pitch, self._horizon_offset)
                self._overlay.update(img, pos=(pos_x, pos_y))

                self._visual_review_up_down.plot(
                    self._horizon[curr_timestamp], curr_timestamp)

                # catch timer having None type at end of video
                if self.player.time_pos == None or self.player.duration == None:
                    self._playing_complete_callback()
                else:
                    self.plainTextEditStats.setPlainText(
                        f'RunID      : {self._selected_run}\n'
                        f'Title      : {self._all_runs_list[self._selected_run -1]["tags"]}\n'
                        f'Timestamp  : {self.player.time_pos:.2f}\n'
                        f'Duration   : {self.player.duration:.2f}\n\n'
                        f'Human Time : {self._get_string_from_timestamp(self.player.time_pos)}\n\n'
                        f'Gaze X     : {gaze_x:.4f}\n'
                        f'Gaze Y     : {gaze_y:.4f}\n\n'
                        f'Roll       : {roll:.4f}\n'
                        f'Pitch      : {pitch:.4f}\n\n'
                        f'x_intercept: {x_intercept:.4f}\n'
                        f'y_intercept: {y_intercept:.4f}\n'
                        f'slope      : {slope:.4f}\n\n'
                        f'Gaze3d Z   : {closest_distance if closest_distance is not None else "None"}\n\n'
                        f'Obervation : {"Looking Up" if currently_up else "Looking Down"}\n'
                        f'Up %       : {percent_up:.4f}\n'
                        f'Down %     : {percent_down:.4f}\n'
                        f'Total Calcs: {total_count}\n'
                    )

    def _playing_complete_callback(self):
        if '_overlay' in self.__dict__:
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
        self.horizontalSliderVolume.setEnabled(False)
        self.actionMute.setEnabled(False)
        self._reset_stats_text()
        self._update_status('Playback stopped')

    def _seekbar_moved(self):
        time_to_seek = self.horizontalSliderSeek.sliderPosition() * \
            (self._selected_end_time - self._selected_start_time) / 1000
        self.player.seek(
            max(time_to_seek, self._selected_start_time), reference='absolute')

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
                'tags': run['tags'],
                'start': run['start'],
                'end': run['end']
            }
        run_count = len(self._all_runs_list)
        if run_count > 0:
            self.tabWidgetMain.setEnabled(True)
            self.listWidgetOverallSelectRuns.clear()
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
                new_item = QtWidgets.QListWidgetItem(
                    f'{run["id"]} - {run["tags"]}', self.listWidgetOverallSelectRuns)
                self.listWidgetOverallSelectRuns.addItem(new_item)
                self._overall_selected_runs.append(run['id'])
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
            self._table_item_single_clicked(
                self._title_filter_model.index(0, 0))
            if len(self._all_runs_list) in [1, 2]:
                self.listWidgetOverallSelectRuns.selectAll()
                self._display_overall_visuals()
                self._display_overall_text()
            else:
                self.plainTextEditOverallStats.setPlainText(
                    'Select one or more runs below to view statistics.')
        else:
            self.tabWidgetMain.setEnabled(False)
            QtWidgets.QMessageBox
            message_box = QtWidgets.QMessageBox(
                text='It looks like this is your first time using eyeplus. \nHead over to File > Import... to get started, or check the documentation under Help.', parent=self.main_window)
            message_box.setWindowIcon(QtGui.QIcon(
                QtGui.QPixmap(':/icons/info.svg')))
            message_box.setWindowTitle('Welcome to eyeplus!')
            message_box.exec()

    def _table_item_single_clicked(self, index: QtCore.QModelIndex) -> None:
        original_index = self._title_filter_model.mapToSource(index)
        runid_index = self._runs_model.index(original_index.row(), 0)
        self._selected_run = int(self._runs_model.itemData(runid_index)[0])
        self._pitch_offset, self._pitch_multi, self._horizon_offset = self._db.get_parameters(
            self._selected_run)
        self._pitch_offset = int(self._pitch_offset)
        self._max_allowed_timestamp = self._db.get_total_duration(
            self._selected_run)
        if 'player' in self.__dict__:
            self._stop_clicked()
        if self._all_runs_dict[self._selected_run]['start'] != -1 and self._all_runs_dict[self._selected_run]['end'] != -1:
            self._part_selection_enabled = True
            self._selected_start_time = float(
                self._all_runs_dict[self._selected_run]['start'])
            self._selected_end_time = float(
                self._all_runs_dict[self._selected_run]['end'])
        else:
            self._part_selection_enabled = False
        self._load_summary_data()
        self._display_summary_text()
        self._display_summary_visuals()
        if self._part_selection_enabled:
            self.lineEditStartTime.setText(
                self._get_string_from_timestamp(self._selected_start_time))
            self.lineEditEndTime.setText(
                self._get_string_from_timestamp(self._selected_end_time))
        else:
            self.lineEditStartTime.setText('00:00:00')
            self.lineEditEndTime.setText(
                self._get_string_from_timestamp(self._horizon_timestamps[-1]))
            self._selected_end_time = self._horizon_timestamps[-1]
            self._selected_start_time = 0.0
        self._update_status(
            f'Successfully loaded summary for runid {self._selected_run}')

    def _open_review_clicked(self) -> None:
        self._gaze = self._db.get_gaze_data(self._selected_run)
        if 'player' in self.__dict__:
            self._stop_clicked()
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
            self._display_confirmation_dialog(
                'Successfully wrote .csv files for one run!')

    def _user_chosen_output_dir(self):
        user_selected_dir = self.output_dir_chooser.selectedFiles()
        if len(user_selected_dir) > 0 and user_selected_dir[0] != '':
            dir_to_save = Path(user_selected_dir[0])
            self._csv.export_all(dir_to_save)
            self._display_confirmation_dialog(
                'Successfully wrote all .csv files!')

    def _display_confirmation_dialog(self, message: str) -> None:
        message_box = QtWidgets.QMessageBox(self.main_window)
        message_box.setWindowTitle('eyeplus | Confirmation')
        message_box.setText(message)
        message_box.exec()

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
        ingest_worker = IngestWorker(self._db_path, found_items, ftype)
        ingest_worker.signals.started.connect(
            self._progress_dialog_start)
        ingest_worker.signals.progress.connect(
            self._progress_dialog_update)
        ingest_worker.signals.finished.connect(
            self._progress_dialog_finish)
        ingest_worker.signals.error.connect(self._ingest_error)
        self._thread_pool.start(ingest_worker)

    def _ingest_error(self, error: str) -> None:
        self.main_window.show()
        self.processing_dialog.hide()
        self._error_box.showMessage(error)

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
        self.parameter_window.set_values(
            int(self._pitch_offset), self._pitch_multi, -self._horizon_offset)
        self.parameter_window.show()
        self.parameter_window.setFocus()
        self.parameter_window.move(250, 600)

    def _update_parameters(self) -> None:
        self._pitch_offset = self.parameter_window.ui.horizontalSliderPitchOffset.value()
        self._pitch_multi = float(
            self.parameter_window.ui.horizontalSliderPitchMulti.value() / 1000)
        self._horizon_offset = float(
            -self.parameter_window.ui.horizontalSliderHorizonFuzzy.value() / 100)

    def _filter_runs(self, text: str) -> None:
        self._title_filter_model.setFilterRegularExpression(text)
        self.tableViewRuns.resizeColumnsToContents()
        self.tableViewRuns.resizeRowsToContents()

    def _update_fusion(self) -> None:
        self._stop_clicked()
        runs_to_redo = [self._selected_run]
        ingest_worker = ReprocessWorker(
            self._db_path, runs_to_redo, self._pitch_offset, self._pitch_multi, self._horizon_offset)
        ingest_worker.signals.started.connect(
            self._reprocess_started)
        ingest_worker.signals.progress.connect(
            self._reprocess_dialog_update)
        ingest_worker.signals.finished.connect(
            self._reprocess_finished)
        self._thread_pool.start(ingest_worker)

    def _load_summary_data(self) -> None:
        if self._selected_start_time != -1 and self._selected_end_time != -1:
            self._part_selection_enabled = True
        self.labelSummaryTitle.setText(
            f'Summary for Run ID {self._selected_run}')
        self.labelSummaryDate.setText(
            f'Date: {self._all_runs_dict[self._selected_run]["import_date"]}')
        self.labelSummaryProcessDate.setText(
            f'Processed: {self._all_runs_dict[self._selected_run]["process_date"]}')
        self.labelSummaryTag.setText(
            f'Title: {self._all_runs_dict[self._selected_run]["tags"]}')
        if self._part_selection_enabled:
            self._tree_predicted2d = self._db.get_pgazed2d_data(
                self._selected_run, self._selected_start_time, self._selected_end_time)
            self._horizon = self._db.get_processed_data(
                self._selected_run, self._selected_start_time, self._selected_end_time)
            self._fusion_data = self._db.get_fusion_data(
                self._selected_run, self._selected_start_time, self._selected_end_time)
        else:
            self._tree_predicted2d = self._db.get_pgazed2d_data(
                self._selected_run)
            self._horizon = self._db.get_processed_data(self._selected_run)
            self._fusion_data = self._db.get_fusion_data(self._selected_run)
        self._gaze_distance = self._db.get_gaze3d_z(self._selected_run)
        self._gaze_distance_timestamps = list(self._gaze_distance.keys())
        self._horizon_timestamps = list(self._horizon.keys())
        self._fusion_timestamps = list(self._fusion_data.keys())
        self._first_timestamp = next(iter(self._tree_predicted2d.keys()))
        self._last_timestamp = round(self._horizon_timestamps[-1], 1) - 0.1
        self.parameter_window.set_values(
            self._pitch_offset, self._pitch_multi, self._horizon_offset)

    def _display_summary_visuals(self) -> None:
        self._visual_summary_up_down.plot(
            self._horizon[self._horizon_timestamps[-1]])
        self._visual_review_heat_map.plot(self._tree_predicted2d)
        self._visual_review_mean_pitch.plot(
            self._horizon[self._horizon_timestamps[-1]], self._fusion_data, self._pitch_multi)
        self._visual_review_gaze_live.plot(
            self._tree_predicted2d, self._horizon)

    def _display_summary_text(self) -> None:
        fusion_stats, gaze_stats = self._db.get_summary_data(
            self._selected_run)
        last_horizon = self._horizon_timestamps[-1]
        self.plainTextEditSummary.setPlainText(
            f'Gaze 2D: {gaze_stats["num_samples"]} Observations\n'
            f'     Mean     Median   Std. Dev.\n'
            f'  X: {gaze_stats["x"]["mean"]:>2.4f} | {gaze_stats["x"]["median"]:.4f} | {gaze_stats["x"]["stdev"]:>2.4f}\n'
            f'  Y: {gaze_stats["y"]["mean"]:>2.4f} | {gaze_stats["y"]["median"]:.4f} | {gaze_stats["y"]["stdev"]:>2.4f}\n\n'
            f'Sensor Fusion: {fusion_stats["num_samples"]} Observations\n'
            f'         Mean      Median    Std. Dev.\n'
            f'  Pitch: {fusion_stats["pitch"]["mean"]:>7.4f} | {fusion_stats["pitch"]["median"]:>7.4f} | {fusion_stats["pitch"]["stdev"]:>7.4f}\n'
            f'  Roll : {fusion_stats["roll"]["mean"]:>7.4f} | {fusion_stats["roll"]["median"]:>7.4f} | {fusion_stats["roll"]["stdev"]:>7.4f}\n\n'
            f'Horizon: {self._horizon[last_horizon]["total"]} Observations\n'
            f'                  Count   Prop.\n'
            f'  Looking Up  : {self._horizon[last_horizon]["up_count"]:>6} | {self._horizon[last_horizon]["percent_up"]:>7.4}\n'
            f'  Looking Down: {self._horizon[last_horizon]["down_count"]:>6} | {self._horizon[last_horizon]["percent_down"]:>7.4f}\n\n'
            f'Offsets\n'
            f'  Horizon    : {-self._horizon_offset:>5.2f}\n'
            f'  Pitch      : {self._pitch_offset:>2}\n'
            f'  Pitch Multi: {self._pitch_multi:>5.2f}'
        )

    def _setup_visual_widgets(self) -> None:
        self._visual_summary_up_down = TotalUpDown(
            500, 500, self._dpi)
        g1_summary_parent = self.widgetSummaryGraphic1.parentWidget().layout()
        g1_summary_parent.removeWidget(self.widgetSummaryGraphic1)
        g1_summary_parent.addWidget(self._visual_summary_up_down)
        self._visual_review_up_down = CumulativeUpDown(500, 500, self._dpi)
        g1_review_parent = self.widgetReviewGraphic1.parentWidget().layout()
        g1_review_parent.removeWidget(self.widgetReviewGraphic1)
        g1_review_parent.addWidget(self._visual_review_up_down)
        g2_summary_parent = self.widgetSummaryGraphic2.parentWidget().layout()
        self._visual_review_heat_map = HeatMap(500, 500, self._dpi)
        g2_summary_parent.removeWidget(self.widgetSummaryGraphic2)
        g2_summary_parent.addWidget(self._visual_review_heat_map)
        g3_summary_parent = self.widgetSummaryGraphic3.parentWidget().layout()
        self._visual_review_mean_pitch = TotalUpDownStacked(
            500, 500, self._dpi)
        g3_summary_parent.removeWidget(self.widgetSummaryGraphic3)
        g3_summary_parent.addWidget(self._visual_review_mean_pitch)
        g2_review_parent = self.widgetReviewGraphic2.parentWidget().layout()
        self._visual_review_pitch = PitchLive(500, 500, self._dpi)
        g2_review_parent.removeWidget(self.widgetReviewGraphic2)
        g2_review_parent.addWidget(self._visual_review_pitch)
        g3_review_parent = self.widgetReviewGraphic3.parentWidget().layout()
        g3_review_parent.removeWidget(self.widgetReviewGraphic3)
        self._visual_review_gaze_live = GazeLive(500, 500, self._dpi)
        g3_review_parent.addWidget(self._visual_review_gaze_live)
        g1_overall_parent = self.widgetOverallGraphic1.parentWidget().layout()
        self._visual_overall_up_down = OverallUpAndDown(500, 500, self._dpi)
        g1_overall_parent.removeWidget(self.widgetOverallGraphic1)
        g1_overall_parent.addWidget(self._visual_overall_up_down)
        g2_overall_parent = self.widgetOverallGraphic2.parentWidget().layout()
        self._visual_overall_pitch_hist = PitchHistogram(500, 500, self._dpi)
        g2_overall_parent.removeWidget(self.widgetOverallGraphic2)
        g2_overall_parent.addWidget(self._visual_overall_pitch_hist)
        g3_overall_parent = self.widgetOverallGraphic3.parentWidget().layout()
        self._visual_overall_gaze2d = OverallGaze2DY(10000, 500, self._dpi)
        g3_overall_parent.removeWidget(self.widgetOverallGraphic3)
        g3_overall_parent.removeWidget(self.horizontalScrollBarLongChart)
        g3_overall_parent.addWidget(self._visual_overall_gaze2d)
        g3_overall_parent.addWidget(self.horizontalScrollBarLongChart)

    def _display_overall_visuals(self) -> None:
        self._longest_run = self._visual_overall_gaze2d.plot(
            self._db.get_all_gaze_2dy(self._overall_selected_runs))
        self.horizontalScrollBarLongChart.setMaximum(self._longest_run)
        self.horizontalScrollBarLongChart.setValue(30)
        self.horizontalScrollBarLongChart.setMinimum(30)
        overall_up_down = self._db.get_overall_up_down(
            self._overall_selected_runs, self._selected_start_time, self._selected_end_time)
        self._visual_overall_up_down.plot(overall_up_down)
        if len(self._overall_selected_runs) > 2:
            binned_pitch = self._db.get_binned_pitch_data(
                self._overall_selected_runs[:2])
        else:
            binned_pitch = self._db.get_binned_pitch_data(
                self._overall_selected_runs)
        self._visual_overall_pitch_hist.plot(binned_pitch)

    def _overall_graphic_slider_moved(self, val: int) -> None:
        self._visual_overall_gaze2d.update_scroll(val)

    def _overall_run_selection_changed(self) -> None:
        self._overall_selected_runs.clear()
        indexes = self.listWidgetOverallSelectRuns.selectedIndexes()
        for index in indexes:
            run_data = self.listWidgetOverallSelectRuns.itemFromIndex(
                index).text()
            runid = int(re.search(r'^\d+', run_data).group(0))
            self._overall_selected_runs.append(runid)
        if not self._overall_selected_runs:
            self._overall_selected_runs.append(
                int(self._all_runs_list[0]['id']))
            self.listWidgetOverallSelectRuns.setCurrentRow(0)
        self._overall_selected_runs.sort()
        self._display_overall_visuals()
        self._display_overall_text()

    def _verify_start_time(self) -> None:
        if self._selected_end_time == -1.0:
            self._selected_end_time = self._horizon_timestamps[-1]
        new_time = self._get_timestamp_from_string(
            self.lineEditStartTime.text())
        if new_time + 60 > self._selected_end_time:
            self._selected_start_time = self._selected_end_time - 60
        else:
            self._selected_start_time = new_time
        self.lineEditStartTime.setText(
            self._get_string_from_timestamp(self._selected_start_time))

    def _verify_end_time(self) -> None:
        if self._selected_start_time == -1.0:
            self._selected_start_time = 0.0
        new_time = self._get_timestamp_from_string(self.lineEditEndTime.text())
        if new_time > self._max_allowed_timestamp:
            self._selected_end_time = self._max_allowed_timestamp
        elif new_time < self._selected_start_time + 60:
            self._selected_end_time = self._selected_start_time + 60
        else:
            self._selected_end_time = new_time
        self.lineEditEndTime.setText(
            self._get_string_from_timestamp(self._selected_end_time))

    def _get_string_from_timestamp(self, timestamp: float) -> str:
        seconds = timestamp
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours < 1:
            hours = 0.0
        if minutes < 1:
            minutes = 0.0
        return f'{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}'

    def _get_timestamp_from_string(self, string_time: str) -> float:
        year_2000 = datetime(2000, 1, 1)
        new_time = datetime.strptime(
            string_time, '%H:%M:%S').replace(year=2000)
        return (new_time - year_2000).total_seconds()

    def _apply_parts_clicked(self) -> None:
        self._part_selection_enabled = True
        if 'player' in self.__dict__:
            self._stop_clicked()
        self._db.update_start_end(self._selected_run, int(
            self._selected_start_time), int(self._selected_end_time))
        tree_predicted2d = self._db.get_pgazed2d_data(
            self._selected_run, self._selected_start_time, self._selected_end_time)
        fusion_data = self._db.get_fusion_data(
            self._selected_run, self._selected_start_time, self._selected_end_time)
        gaze_stats = get_gaze_stats(tree_predicted2d)
        fusion_stats = get_fusion_stats(fusion_data)
        self._db.write_summary_data(
            self._selected_run, fusion_stats, gaze_stats)
        self._load_summary_data()
        self._display_summary_visuals()
        self._display_summary_text()
        self._update_status(
            f'Successfully applied active time for runid {self._selected_run}')

    def _display_overall_text(self) -> None:
        overall_data = self._db.get_processed_view()
        max_up = -1
        max_up_run = -1
        max_down = -1
        max_down_run = -1
        for k, v in overall_data.items():
            if v[1] > max_up and k in self._overall_selected_runs:
                max_up = v[0]
                max_up_run = k
            if v[2] > max_down and k in self._overall_selected_runs:
                max_down = v[1]
                max_down_run = k
        max_pitch_mean = -100
        max_pitch_mean_run = -1
        min_pitch_mean = 100
        min_pitch_mean_run = 1
        rolly = -1
        rolly_run = -1
        eyey = -1
        eyey_run = -1
        gaze_samples = -1
        gaze_samples_run = -1
        fusion_samples = -1
        for runid in self._overall_selected_runs:
            fusion_stats, gaze_stats = self._db.get_summary_data(runid)
            if fusion_stats['pitch']['mean'] > max_pitch_mean:
                max_pitch_mean = fusion_stats['pitch']['mean']
                max_pitch_mean_run = runid
            if fusion_stats['pitch']['mean'] < min_pitch_mean:
                min_pitch_mean = fusion_stats['pitch']['mean']
                min_pitch_mean_run = runid
            if fusion_stats['roll']['stdev'] > rolly:
                rolly = fusion_stats['roll']['stdev']
                rolly_run = runid
            if gaze_stats['x']['stdev'] + gaze_stats['y']['stdev'] > eyey:
                eyey = gaze_stats['x']['stdev'] + gaze_stats['y']['stdev']
                eyey_run = runid
            if gaze_stats['num_samples'] > gaze_samples:
                gaze_samples = gaze_stats['num_samples']
                fusion_samples = fusion_stats['num_samples']
                gaze_samples_run = 1

        self.plainTextEditOverallStats.setPlainText(
            f'Selected run quantity : {len(self._overall_selected_runs)}\n\n'
            f'Up/Down:\n'
            f'  Max prop. up   : Run {max_up_run} @ {max_up:0.4f}\n'
            f'  Max prop. down : Run {max_down_run} @ {max_down:0.4f}\n\n'
            f'Pitch:\n'
            f'  Max pitch mean : Run {max_pitch_mean_run} @ {max_pitch_mean:4.2f}\n'
            f'  Min pitch mean : Run {min_pitch_mean_run} @ {min_pitch_mean:4.2f}\n\n'
            f'Longest run: {gaze_samples_run}\n'
            f'  Gaze samples   : {gaze_samples}\n'
            f'  Fusion samples : {fusion_samples}\n\n'
            f'Other:\n'
            f'  Run {rolly_run} had the max roll stdev @ {rolly:0.4f}\n'
            f'  Run {eyey_run} had the max gaze2d stdev @ {eyey:0.4f}'
        )
