import unittest
from pathlib import Path
from unittest import mock

from PyQt6 import QtCore

import mpv

from qt.playbackworker import PlaybackWorker, PlaybackWorkerSignals


class TestPlaybackWorker(unittest.TestCase):
    def setUp(self):
        self.player = mpv.MPV()
        self.signals = PlaybackWorkerSignals()
        self.worker = PlaybackWorker(self.player, Path('C:\BCIT\Term 4\ACIT 4900(ISSP)\MOT student pilot data\Pilot video with head callibration.mp4'))
        self.worker.signals.playing.connect(self.signals.playing.emit)
        self.worker.signals.finished.connect(self.signals.finished.emit)
        self.worker.signals.progress.connect(self.signals.progress.emit)
        self.timer_mock = mock.Mock(spec=QtCore.QTimer)
        self.worker.timer = self.timer_mock

    def tearDown(self):
        self.player.terminate()

    def test_run(self):
        self.worker.run()
        self.player.wait_for_shutdown.assert_called_once()
        self.signals.playing.emit.assert_called_once()

    def test_update_loop(self):
        self.player.duration = 10.0
        self.player.time_pos = 5.0
        self.worker.update_loop()
        self.signals.progress.emit.assert_called_once_with(500)

    def test_update_loop_finished(self):
        self.player.duration = 10.0
        self.player.time_pos = None
        self.worker.update_loop()
        self.signals.finished.emit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
