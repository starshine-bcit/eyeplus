from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_helpDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowserDisplay = QtWidgets.QTextBrowser(Dialog)
        self.textBrowserDisplay.setMinimumSize(QtCore.QSize(400, 300))
        self.textBrowserDisplay.setObjectName("textBrowserDisplay")
        self.verticalLayout.addWidget(self.textBrowserDisplay)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
