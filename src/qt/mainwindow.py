from pathlib import Path
import sys

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

    def _connect_events(self):
        self.horizontalSliderSeek.sliderMoved.connect(self._seekbar_moved)
        self.horizontalSliderSeek.sliderReleased.connect(self._seekbar_moved)
        self.actionPlay.triggered.connect(self._play_clicked)
        self.actionExit.triggered.connect(self._safe_quit_menu)
        self.main_window.closeEvent = self._safe_quit_x
        self.actionPause.triggered.connect(self._pause_clicked)
        self.actionStop.triggered.connect(self._stop_clicked)
        self.tabWidgetMain.currentChanged.connect(self._main_tab_changed)

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
        self.actionPause.setChecked(True)
        self.playback_worker.timer.start()
        self.horizontalSliderSeek.setEnabled(True)
        self.actionPlay.setEnabled(False)
        self.actionPause.setEnabled(True)
        self.actionStop.setEnabled(True)

    def _playing_update_progress_callback(self, progress: int):
        if not self.horizontalSliderSeek.isSliderDown():
            self.horizontalSliderSeek.setSliderPosition(progress)

    def _playing_complete_callback(self):
        print('playing stopped')
        self.playback_worker.timer.stop()
        self.horizontalSliderSeek.setEnabled(False)
        self.horizontalSliderSeek.setSliderPosition(0)
        self.actionPlay.setEnabled(True)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)

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
