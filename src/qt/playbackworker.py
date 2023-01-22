from pathlib import Path

from PyQt6 import QtCore

from modules import mpv


class PlaybackWorkerSignals(QtCore.QObject):
    playing = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)


class PlaybackWorker(QtCore.QRunnable):
    def __init__(self, player: mpv.MPV, video: Path) -> None:
        super(PlaybackWorker, self).__init__()
        self.player = player
        self.video = video
        self.signals = PlaybackWorkerSignals()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_loop)
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        self.player.play(str(self.video))
        self.player.wait_until_playing()
        self.signals.playing.emit()
        self.player.wait_for_shutdown()

    def update_loop(self):
        if self.player.time_pos:
            duration = self.player.duration
            time_position = self.player.time_pos
            current_progress = int(time_position / duration * 1000)
            self.signals.progress.emit(current_progress)
        else:
            self.signals.finished.emit()
