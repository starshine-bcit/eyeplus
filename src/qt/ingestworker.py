from pathlib import Path

from PyQt6 import QtCore

from modules.eyedb import EyeDB
from utils.processor import ingest_and_process, reprocess


class IngestWorkerSignals(QtCore.QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal((str, float))


class IngestWorker(QtCore.QRunnable):
    def __init__(self, db_path: Path, paths: list[Path], type: str = 'zip', horizon_offset: float = 0.0) -> None:
        super().__init__()
        self.signals = IngestWorkerSignals()
        self.db_path = db_path
        self.paths = paths
        self.type = type
        self.horizon_offset = horizon_offset
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        self.signals.started.emit()
        eyedb = EyeDB(self.db_path)
        ingest_and_process(self.cb_progress, eyedb, self.paths,
                           self.type, self.horizon_offset)
        self.signals.finished.emit()

    def cb_progress(self, message: str, progress: float) -> None:
        self.signals.progress.emit(message, progress)


class ReprocessWorker(QtCore.QRunnable):
    def __init__(self, db_path: Path, runs_to_redo: list[int], roll_offset: int, pitch_multi: float, horizon_offset: float) -> None:
        super().__init__()
        self.signals = IngestWorkerSignals()
        self.db_path = db_path
        self.runs_to_redo = runs_to_redo
        self.roll_offset = roll_offset
        self.pitch_multi = pitch_multi
        self.horizon_offset = horizon_offset
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        self.signals.started.emit()
        eyedb = EyeDB(self.db_path)
        reprocess(self.cb_progress, eyedb, self.runs_to_redo,
                  roll_offset=self.roll_offset, pitch_multi=self.pitch_multi, horizon_offset=self.horizon_offset)
        self.signals.finished.emit()

    def cb_progress(self, message: str, progress: float) -> None:
        self.signals.progress.emit(message, progress)
