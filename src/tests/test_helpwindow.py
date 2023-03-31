import sys
import unittest
from PyQt6.QtWidgets import QApplication
from qt.helpwindow import Ui_helpDialog
from PyQt6 import QtCore, QtGui, QtWidgets


class TestUiHelpDialog(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_helpDialog()
        self.ui.setupUi(self.dialog)

    def test_display_text(self):
        expected_text = "Hello, world!"
        self.ui.textBrowserDisplay.setText(expected_text)
        actual_text = self.ui.textBrowserDisplay.toPlainText()
        self.assertEqual(actual_text, expected_text)

    def tearDown(self):
        self.dialog.close()
        del self.ui
        del self.dialog
        del self.app

if __name__ == '__main__':
    unittest.main()
