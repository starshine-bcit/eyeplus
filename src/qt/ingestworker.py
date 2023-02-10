from pathlib import Path

from PyQt6 import QtCore

from modules.eyedb import EyeDB
from utils.processor import ingest_and_process


class IngestWorkerSignals(QtCore.QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal((str, float))


class IngestWorker(QtCore.QRunnable):
    def __init__(self, db_path: Path, paths: list[Path], type: str = 'zip') -> None:
        super().__init__()
        self.signals = IngestWorkerSignals()
        self.db_path = db_path
        self.paths = paths
        self.type = type
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        self.signals.started.emit()
        eyedb = EyeDB(self.db_path)
        ingest_and_process(self.cb_progress, eyedb, self.paths, self.type)
        self.signals.finished.emit()

    def cb_progress(self, message: str, progress: float) -> None:
        self.signals.progress.emit(message, progress)
