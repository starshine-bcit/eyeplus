import os
from pathlib import Path
import sys

mlib_path = str(Path(__file__).parent.parent / 'mlib')
if mlib_path not in os.environ['PATH']:
    os.environ['PATH'] = str(Path(__file__).parent.parent / 'mlib') + os.pathsep + os.environ['PATH']

from qt.mainwindow import EyeMainWindow
from PyQt6 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = EyeMainWindow(MainWindow, app)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
