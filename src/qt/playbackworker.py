from pathlib import Path

from PyQt6 import QtCore

from modules import mpv


class PlaybackWorkerSignals(QtCore.QObject):
    playing = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)


class PlaybackWorker(QtCore.QRunnable):
    def __init__(self, player: mpv.MPV, video: Path, start: float = -1.0, end: float = -1.0) -> None:
        super(PlaybackWorker, self).__init__()
        self.player = player
        self.video = video
        if start == -1.0:
            self.start = 0.0
        else:
            self.start = start
        self.end = end
        self.signals = PlaybackWorkerSignals()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_loop)
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        self.player.play(str(self.video))
        self.player.wait_until_playing()
        if self.end == -1.0:
            self.end = self.player.duration
        self.player.seek(self.start, 'absolute')
        self.signals.playing.emit()
        self.player.wait_for_shutdown()

    def update_loop(self):
        if self.player.time_pos:
            time_position = self.player.time_pos
            if time_position >= self.end:
                self.signals.finished.emit()
                self.player.stop()
            current_progress = int(
                (time_position - self.start) / (self.end - self.start) * 1000)
            self.signals.progress.emit(current_progress)
        else:
            self.signals.finished.emit()
