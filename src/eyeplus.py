import sys

from PyQt6 import QtWidgets

from qt.mainwindow import EyeMainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = EyeMainWindow(MainWindow, app)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
