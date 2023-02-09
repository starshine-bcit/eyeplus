from pathlib import Path

from PyQt6 import QtCore

from modules.eyedb import EyeDB
from utils.processor import ingest_and_process


class IngestWorkerSignals(QtCore.QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal((str, float))


class IngestWorker(QtCore.QRunnable):
    def __init__(self, eyedb: EyeDB, paths: list[Path], type: str = 'zip') -> None:
        super().__init__()
        self.signals = IngestWorkerSignals()
        self.eyedb = eyedb
        self.paths = paths
        self.type = type
        self.setAutoDelete(True)

    @QtCore.pyqtslot()
    def run(self):
        self.signals.started.emit()
        ingest_and_process(self.cb_progress, self.eyedb, self.paths, self.type)
        self.signals.finished.emit()

    def cb_progress(self, message: str, progress: float) -> None:
        self.signals.progress.emit((message, progress))
