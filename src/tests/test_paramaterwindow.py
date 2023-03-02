import sys
import unittest
from PyQt6.QtWidgets import QApplication
from parameterwindow import ParameterWindow

app = QApplication(sys.argv)

class TestParameterWindow(unittest.TestCase):
    def setUp(self):
        self.window = ParameterWindow(None)

    def test_reset(self):
        self.window.reset()
        self.assertEqual(self.window.ui.lineEditHorizonFuzzy.text(), '0')
        self.assertEqual(self.window.ui.lineEditPitchMulti.text(), '1000')
        self.assertEqual(self.window.ui.lineEditRollOffset.text(), '90')
        self.assertEqual(self.window.ui.horizontalSliderHorizonFuzzy.value(), 0)
        self.assertEqual(self.window.ui.horizontalSliderPitchMulti.value(), 1000)
        self.assertEqual(self.window.ui.horizontalSliderRollOffset.value(), 90)

    def test_set_values(self):
        self.window.set_values(45, 0.75)
        self.assertEqual(self.window.ui.lineEditRollOffset.text(), '45')
        self.assertEqual(self.window.ui.horizontalSliderRollOffset.value(), 45)
        self.assertEqual(self.window.ui.lineEditPitchMulti.text(), '750')
        self.assertEqual(self.window.ui.horizontalSliderPitchMulti.value(), 750)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
