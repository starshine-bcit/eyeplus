from pathlib import Path
import sys
import os

from PyQt6 import QtCore, QtGui, QtWidgets

from qt.qtui import Ui_MainWindow
from modules import mpv
from qt.playbackworker import PlaybackWorker
import qt.resources


class EyeMainWindow(Ui_MainWindow):
    def __init__(self, main_window: QtWidgets.QMainWindow, app: QtWidgets.QApplication) -> None:
        self.app = app
        self.main_window = main_window
        self.setupUi(self.main_window)
        self._setup_custom_ui()
        self._connect_events()
        self._init_player()
        self._setup_test_video()

    def _setup_custom_ui(self):
        self.main_window.setWindowTitle('eyeplus')
        self.main_window.setWindowIcon(
            QtGui.QIcon(QtGui.QPixmap(':/icons/eye.svg')))
        self._thread_pool = QtCore.QThreadPool()
        self.tabWidgetMain.setCurrentIndex(0)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)
        self.toolBar.setVisible(False)
        self.actionMute.setEnabled(False)
        self.actionMute.setEnabled(False)
        self._reset_stats_text()
        self._populate_runs_tables()
        self._init_input_file_chooser()
        self._init_output_file_chooser()
        self._init_output_dir_chooser()
        self._init_status_bar()

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

    def _init_player(self):
        # self.widgetVideoContainer.setAttribute(
        #     QtCore.Qt.WA_DontCreateNativeAncestors)
        # self.widgetVideoContainer.setAttribute(QtCore.Qt.WA_NativeWindow)
        self.player = mpv.MPV(wid=str(int(self.widgetVideoContainer.winId())),
                              log_handler=print,
                              loglevel='info',
                              force_window='yes',
                              background="#FFFFFF")

    def _setup_test_video(self):
        sample_video = Path(__file__).parent.parent.parent / 'data' / \
            'sample' / 'Pilot video with head callibration.mp4'
        self.playback_worker = PlaybackWorker(
            player=self.player, video=sample_video)
        self.playback_worker.signals.playing.connect(
            self._playing_started_callback)
        self.playback_worker.signals.progress.connect(
            self._playing_update_progress_callback)
        self.playback_worker.signals.finished.connect(
            self._playing_complete_callback)

    def _playing_started_callback(self):
        print(f'playing started\nduration: {self.player.duration}')
        self.player.command('set', 'pause', 'yes')
        if self.actionMute.isChecked():
            self.player.command('set', 'mute', 'yes')
        self.actionPause.setChecked(True)
        self.playback_worker.timer.start()
        self.horizontalSliderSeek.setEnabled(True)
        self.actionPlay.setEnabled(False)
        self.actionPause.setEnabled(True)
        self.actionStop.setEnabled(True)
        self.actionMute.setEnabled(True)
        self.horizontalSliderVolume.setEnabled(True)
        self.actionMute.setEnabled(True)

    def _playing_update_progress_callback(self, progress: int):
        if not self.horizontalSliderSeek.isSliderDown():
            self.horizontalSliderSeek.setSliderPosition(progress)
        if not self.player.pause:
            self.plainTextEditStats.setPlainText(
                f'Timestamp     : {self.player.time_pos:.2f}\n'
                f'Duration      : {self.player.duration:.2f}\n'
                f'Additional Information...'
            )

    def _playing_complete_callback(self):
        print('playing stopped')
        self.playback_worker.timer.stop()
        self.horizontalSliderSeek.setEnabled(False)
        self.horizontalSliderSeek.setSliderPosition(0)
        self.actionPlay.setEnabled(True)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)
        self.actionMute.setEnabled(False)
        self.horizontalSliderVolume.setEnabled(False)
        self.actionMute.setEnabled(False)
        self._reset_stats_text()

    def _seekbar_moved(self):
        time_to_seek = self.horizontalSliderSeek.sliderPosition() * \
            self.player.duration / 1000
        self.player.seek(max(time_to_seek, 1), reference='absolute')

    def _play_clicked(self):
        self._setup_test_video()
        self._thread_pool.start(self.playback_worker)

    def _safe_quit_x(self, event):
        self.player.terminate()
        self.player.wait_for_shutdown()
        event.accept()

    def _safe_quit_menu(self):
        self.player.terminate()
        self.player.wait_for_shutdown()
        sys.exit(0)

    def _pause_clicked(self):
        if self.player.pause:
            self.player.command('set', 'pause', 'no')
        else:
            self.player.command('set', 'pause', 'yes')

    def _stop_clicked(self):
        self.player.stop()

    def _main_tab_changed(self):
        if self.tabWidgetMain.currentIndex() == 1:
            self.toolBar.setVisible(True)
        elif self.tabWidgetMain.currentIndex() == 0:
            self.toolBar.setVisible(False)
        elif self.tabWidgetMain.currentIndex() == 2:
            self.toolBar.setVisible(False)

    def _reset_stats_text(self):
        self.plainTextEditStats.setPlainText(
            f'Timestamp     : \n'
            f'Duration      : \n'
            f'Additional Information...'
        )

    def _populate_runs_tables(self):
        self.tableWidgetRuns.setHorizontalHeaderLabels(
            ['Date', 'Processed', 'Tags'])
        sample_dates = ['2022-01-05', '2022-01-08', '2022-01-12']
        sample_processed = ['2022-01-07', '2022-01-13', '2022-01-13']
        sample_tags = [['jim', 'pilot'], ['jim'], ['jane', 'pilot']]
        for i in range(3):
            self.tableWidgetRuns.insertRow(i)
            self.tableWidgetRuns.setItem(
                i, 0, QtWidgets.QTableWidgetItem(sample_dates[i]))
            self.tableWidgetRuns.setItem(
                i, 1, QtWidgets.QTableWidgetItem(sample_processed[i]))
            self.tableWidgetRuns.setItem(
                i, 2, QtWidgets.QTableWidgetItem(', '.join(sample_tags[i])))
        if self.tableWidgetRuns.rowCount() > 0:
            self.tableWidgetRuns.setSortingEnabled(True)
            self.tableWidgetRuns.sortByColumn(
                1, QtCore.Qt.SortOrder.AscendingOrder)

    def _init_input_file_chooser(self):
        self.input_file_chooser = QtWidgets.QFileDialog(self.main_window)
        self.input_file_chooser.setDirectory(os.path.expanduser('~'))
        self.input_file_chooser.setFileMode(
            QtWidgets.QFileDialog.FileMode.ExistingFiles)
        self.input_file_chooser.setViewMode(
            QtWidgets.QFileDialog.ViewMode.List)
        self.input_file_chooser.setNameFilter('zip (*.zip)')
        self.input_file_chooser.finished.connect(self._user_chosen_zip)

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
        self.output_file_chooser.finished.connect(self._user_chosen_csv)

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
        self.output_dir_chooser.finished.connect(self._user_chosen_dir)

    def _export_single_clicked(self):
        self.output_file_chooser.exec()

    def _import_zip_clicked(self):
        self.input_file_chooser.exec()

    def _export_all_clicked(self):
        self.output_dir_chooser.exec()

    def _user_chosen_csv(self):
        user_selected_file = self.output_file_chooser.selectedFiles()
        if len(user_selected_file) > 0 and user_selected_file[0] != '':
            self._csv_to_save = Path(user_selected_file[0])
            print(self._csv_to_save)

    def _user_chosen_dir(self):
        user_selected_dir = self.output_dir_chooser.selectedFiles()
        if len(user_selected_dir) > 0 and user_selected_dir[0] != '':
            self._dir_to_save = Path(user_selected_dir[0])
            print(self._dir_to_save)

    def _user_chosen_zip(self):
        user_selected_zips = self.input_file_chooser.selectedFiles()
        if len(user_selected_zips) > 0:
            self._zips_to_import = [Path(x)
                                    for x in user_selected_zips if x != '']
            print(self._zips_to_import)

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
