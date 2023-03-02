import sys
import unittest
from PyQt6.QtWidgets import QApplication
from parameterwindow import ParameterWindow


class TestParameterWindow(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.parameter_window = ParameterWindow(None)
        self.ui = self.parameter_window.ui

    def tearDown(self):
        self.parameter_window.deleteLater()
        self.app.processEvents()

    def test_text_edited_updates_slider(self):
        self.ui.lineEditHorizonFuzzy.setText('50')
        self.assertEqual(self.ui.horizontalSliderHorizonFuzzy.value(), 0)

    def test_slider_moved_updates_text(self):
        self.ui.horizontalSliderPitchMulti.setValue(500)
        self.assertEqual(self.ui.lineEditPitchMulti.text(), '100')

    def test_reset_button_resets_values(self):
        self.ui.horizontalSliderHorizonFuzzy.setValue(50)
        self.ui.horizontalSliderPitchMulti.setValue(500)
        self.ui.horizontalSliderRollOffset.setValue(45)
        self.ui.lineEditHorizonFuzzy.setText('75')
        self.ui.lineEditPitchMulti.setText('750')
        self.ui.lineEditRollOffset.setText('30')
        self.ui.pushButtonReset.click()
        self.assertEqual(self.ui.horizontalSliderHorizonFuzzy.value(), 0)
        self.assertEqual(self.ui.lineEditHorizonFuzzy.text(), '0')
        self.assertEqual(self.ui.horizontalSliderPitchMulti.value(), 1000)
        self.assertEqual(self.ui.lineEditPitchMulti.text(), '1000')
        self.assertEqual(self.ui.horizontalSliderRollOffset.value(), 90)
        self.assertEqual(self.ui.lineEditRollOffset.text(), '90')


if __name__ == '__main__':
    unittest.main()
