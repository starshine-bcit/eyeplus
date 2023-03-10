# Form implementation generated from reading ui file '.\qtsrc\eyeplus\parameterDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_parameterDialog(object):
    def setupUi(self, parameterDialog):
        parameterDialog.setObjectName("parameterDialog")
        parameterDialog.resize(524, 212)
        self.verticalLayout = QtWidgets.QVBoxLayout(parameterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelPitchMulti = QtWidgets.QLabel(parameterDialog)
        self.labelPitchMulti.setObjectName("labelPitchMulti")
        self.horizontalLayout_2.addWidget(self.labelPitchMulti)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.lineEditPitchMulti = QtWidgets.QLineEdit(parameterDialog)
        self.lineEditPitchMulti.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lineEditPitchMulti.setObjectName("lineEditPitchMulti")
        self.horizontalLayout_2.addWidget(self.lineEditPitchMulti)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalSliderPitchMulti = QtWidgets.QSlider(parameterDialog)
        self.horizontalSliderPitchMulti.setMinimum(0)
        self.horizontalSliderPitchMulti.setMaximum(2000)
        self.horizontalSliderPitchMulti.setProperty("value", 1000)
        self.horizontalSliderPitchMulti.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSliderPitchMulti.setObjectName("horizontalSliderPitchMulti")
        self.verticalLayout.addWidget(self.horizontalSliderPitchMulti)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelRollOffset = QtWidgets.QLabel(parameterDialog)
        self.labelRollOffset.setObjectName("labelRollOffset")
        self.horizontalLayout_3.addWidget(self.labelRollOffset)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.lineEditRollOffset = QtWidgets.QLineEdit(parameterDialog)
        self.lineEditRollOffset.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lineEditRollOffset.setObjectName("lineEditRollOffset")
        self.horizontalLayout_3.addWidget(self.lineEditRollOffset)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalSliderRollOffset = QtWidgets.QSlider(parameterDialog)
        self.horizontalSliderRollOffset.setMinimum(0)
        self.horizontalSliderRollOffset.setMaximum(179)
        self.horizontalSliderRollOffset.setProperty("value", 90)
        self.horizontalSliderRollOffset.setSliderPosition(90)
        self.horizontalSliderRollOffset.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSliderRollOffset.setObjectName("horizontalSliderRollOffset")
        self.verticalLayout.addWidget(self.horizontalSliderRollOffset)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelHorizonFuzzy = QtWidgets.QLabel(parameterDialog)
        self.labelHorizonFuzzy.setObjectName("labelHorizonFuzzy")
        self.horizontalLayout_4.addWidget(self.labelHorizonFuzzy)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.lineEditHorizonFuzzy = QtWidgets.QLineEdit(parameterDialog)
        self.lineEditHorizonFuzzy.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lineEditHorizonFuzzy.setObjectName("lineEditHorizonFuzzy")
        self.horizontalLayout_4.addWidget(self.lineEditHorizonFuzzy)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalSliderHorizonFuzzy = QtWidgets.QSlider(parameterDialog)
        self.horizontalSliderHorizonFuzzy.setMinimum(-500)
        self.horizontalSliderHorizonFuzzy.setMaximum(500)
        self.horizontalSliderHorizonFuzzy.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSliderHorizonFuzzy.setObjectName("horizontalSliderHorizonFuzzy")
        self.verticalLayout.addWidget(self.horizontalSliderHorizonFuzzy)
        self.line = QtWidgets.QFrame(parameterDialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonReset = QtWidgets.QPushButton(parameterDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/refresh-ccw.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonReset.setIcon(icon)
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.horizontalLayout.addWidget(self.pushButtonReset)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButtonApply = QtWidgets.QPushButton(parameterDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/check-circle.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonApply.setIcon(icon1)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(4, 1)

        self.retranslateUi(parameterDialog)
        QtCore.QMetaObject.connectSlotsByName(parameterDialog)

    def retranslateUi(self, parameterDialog):
        _translate = QtCore.QCoreApplication.translate
        parameterDialog.setWindowTitle(_translate("parameterDialog", "Dialog"))
        self.labelPitchMulti.setText(_translate("parameterDialog", "Pitch Multiplier"))
        self.lineEditPitchMulti.setInputMask(_translate("parameterDialog", "0000"))
        self.lineEditPitchMulti.setText(_translate("parameterDialog", "100"))
        self.labelRollOffset.setText(_translate("parameterDialog", "Roll Offset"))
        self.lineEditRollOffset.setInputMask(_translate("parameterDialog", "009"))
        self.lineEditRollOffset.setText(_translate("parameterDialog", "90"))
        self.labelHorizonFuzzy.setText(_translate("parameterDialog", "Horizon Offset"))
        self.lineEditHorizonFuzzy.setInputMask(_translate("parameterDialog", "#000"))
        self.lineEditHorizonFuzzy.setText(_translate("parameterDialog", "00"))
        self.pushButtonReset.setText(_translate("parameterDialog", "Reset"))
        self.pushButtonApply.setText(_translate("parameterDialog", "Apply"))
