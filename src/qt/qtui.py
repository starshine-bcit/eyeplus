# Form implementation generated from reading ui file '..\..\qtsrc\eyeplus\mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 725)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidgetMain = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetMain.setObjectName("tabWidgetMain")
        self.tabDataList = QtWidgets.QWidget()
        self.tabDataList.setObjectName("tabDataList")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabDataList)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frameLeftProcessed = QtWidgets.QFrame(self.tabDataList)
        self.frameLeftProcessed.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameLeftProcessed.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameLeftProcessed.setObjectName("frameLeftProcessed")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frameLeftProcessed)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tableWidgetRuns = QtWidgets.QTableWidget(self.frameLeftProcessed)
        self.tableWidgetRuns.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.tableWidgetRuns.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidgetRuns.setAlternatingRowColors(True)
        self.tableWidgetRuns.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidgetRuns.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidgetRuns.setRowCount(0)
        self.tableWidgetRuns.setColumnCount(3)
        self.tableWidgetRuns.setObjectName("tableWidgetRuns")
        self.tableWidgetRuns.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidgetRuns.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidgetRuns.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetRuns.verticalHeader().setDefaultSectionSize(20)
        self.verticalLayout_6.addWidget(self.tableWidgetRuns)
        self.horizontalLayoutSearch = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSearch.setObjectName("horizontalLayoutSearch")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.frameLeftProcessed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 28))
        self.plainTextEdit.setBaseSize(QtCore.QSize(0, 30))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayoutSearch.addWidget(self.plainTextEdit)
        self.pushButtonSearch = QtWidgets.QPushButton(self.frameLeftProcessed)
        self.pushButtonSearch.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonSearch.setBaseSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/search.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSearch.setIcon(icon)
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.horizontalLayoutSearch.addWidget(self.pushButtonSearch)
        self.horizontalLayoutSearch.setStretch(0, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayoutSearch)
        self.verticalLayout_6.setStretch(0, 1)
        self.horizontalLayout_2.addWidget(self.frameLeftProcessed)
        self.frameSummary = QtWidgets.QFrame(self.tabDataList)
        self.frameSummary.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameSummary.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameSummary.setObjectName("frameSummary")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameSummary)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelSummaryExample = QtWidgets.QLabel(self.frameSummary)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.labelSummaryExample.setFont(font)
        self.labelSummaryExample.setScaledContents(False)
        self.labelSummaryExample.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelSummaryExample.setWordWrap(True)
        self.labelSummaryExample.setObjectName("labelSummaryExample")
        self.verticalLayout_2.addWidget(self.labelSummaryExample)
        self.horizontalLayoutSummaryButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummaryButtons.setObjectName("horizontalLayoutSummaryButtons")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutSummaryButtons.addItem(spacerItem)
        self.pushButtonExportDisplayed = QtWidgets.QPushButton(self.frameSummary)
        self.pushButtonExportDisplayed.setMinimumSize(QtCore.QSize(110, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/file-spreadsheet.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonExportDisplayed.setIcon(icon1)
        self.pushButtonExportDisplayed.setObjectName("pushButtonExportDisplayed")
        self.horizontalLayoutSummaryButtons.addWidget(self.pushButtonExportDisplayed)
        self.verticalLayout_2.addLayout(self.horizontalLayoutSummaryButtons)
        self.verticalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.addWidget(self.frameSummary)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.tabWidgetMain.addTab(self.tabDataList, "")
        self.tabReviewData = QtWidgets.QWidget()
        self.tabReviewData.setObjectName("tabReviewData")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tabReviewData)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutReviewLeft = QtWidgets.QVBoxLayout()
        self.verticalLayoutReviewLeft.setObjectName("verticalLayoutReviewLeft")
        self.plainTextEditStats = QtWidgets.QPlainTextEdit(self.tabReviewData)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        self.plainTextEditStats.setFont(font)
        self.plainTextEditStats.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.plainTextEditStats.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.plainTextEditStats.setReadOnly(True)
        self.plainTextEditStats.setObjectName("plainTextEditStats")
        self.verticalLayoutReviewLeft.addWidget(self.plainTextEditStats)
        self.horizontalLayout.addLayout(self.verticalLayoutReviewLeft)
        self.verticalLayoutReviewRight = QtWidgets.QVBoxLayout()
        self.verticalLayoutReviewRight.setObjectName("verticalLayoutReviewRight")
        self.frameReviewImages = QtWidgets.QFrame(self.tabReviewData)
        self.frameReviewImages.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameReviewImages.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameReviewImages.setObjectName("frameReviewImages")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameReviewImages)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelReviewExample = QtWidgets.QLabel(self.frameReviewImages)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.labelReviewExample.setFont(font)
        self.labelReviewExample.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelReviewExample.setObjectName("labelReviewExample")
        self.verticalLayout_3.addWidget(self.labelReviewExample)
        self.verticalLayoutReviewRight.addWidget(self.frameReviewImages)
        self.frameVideo = QtWidgets.QFrame(self.tabReviewData)
        self.frameVideo.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameVideo.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameVideo.setObjectName("frameVideo")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frameVideo)
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widgetVideoContainer = QtWidgets.QWidget(self.frameVideo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetVideoContainer.sizePolicy().hasHeightForWidth())
        self.widgetVideoContainer.setSizePolicy(sizePolicy)
        self.widgetVideoContainer.setMinimumSize(QtCore.QSize(480, 270))
        self.widgetVideoContainer.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.widgetVideoContainer.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.widgetVideoContainer.setObjectName("widgetVideoContainer")
        self.verticalLayout_4.addWidget(self.widgetVideoContainer)
        self.verticalLayoutReviewRight.addWidget(self.frameVideo)
        self.horizontalSliderSeek = QtWidgets.QSlider(self.tabReviewData)
        self.horizontalSliderSeek.setEnabled(False)
        self.horizontalSliderSeek.setMaximum(1000)
        self.horizontalSliderSeek.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSliderSeek.setObjectName("horizontalSliderSeek")
        self.verticalLayoutReviewRight.addWidget(self.horizontalSliderSeek)
        self.verticalLayoutReviewRight.setStretch(0, 1)
        self.verticalLayoutReviewRight.setStretch(1, 3)
        self.horizontalLayout.addLayout(self.verticalLayoutReviewRight)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.tabWidgetMain.addTab(self.tabReviewData, "")
        self.tabOverallSummary = QtWidgets.QWidget()
        self.tabOverallSummary.setObjectName("tabOverallSummary")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tabOverallSummary)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.labelOverallSummaryExample = QtWidgets.QLabel(self.tabOverallSummary)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.labelOverallSummaryExample.setFont(font)
        self.labelOverallSummaryExample.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelOverallSummaryExample.setWordWrap(True)
        self.labelOverallSummaryExample.setObjectName("labelOverallSummaryExample")
        self.verticalLayout_5.addWidget(self.labelOverallSummaryExample)
        self.horizontalLayoutOverallButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutOverallButtons.setObjectName("horizontalLayoutOverallButtons")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutOverallButtons.addItem(spacerItem1)
        self.pushButtonExportAll = QtWidgets.QPushButton(self.tabOverallSummary)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/download.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonExportAll.setIcon(icon2)
        self.pushButtonExportAll.setObjectName("pushButtonExportAll")
        self.horizontalLayoutOverallButtons.addWidget(self.pushButtonExportAll)
        self.verticalLayout_5.addLayout(self.horizontalLayoutOverallButtons)
        self.verticalLayout_5.setStretch(0, 1)
        self.tabWidgetMain.addTab(self.tabOverallSummary, "")
        self.verticalLayout.addWidget(self.tabWidgetMain)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.toolBar.setIconSize(QtCore.QSize(38, 38))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.BottomToolBarArea, self.toolBar)
        self.actionImport_Zip = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/upload.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionImport_Zip.setIcon(icon3)
        self.actionImport_Zip.setObjectName("actionImport_Zip")
        self.actionExit = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/x.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon4)
        self.actionExit.setObjectName("actionExit")
        self.actionPause = QtGui.QAction(MainWindow)
        self.actionPause.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/pause.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPause.setIcon(icon5)
        self.actionPause.setObjectName("actionPause")
        self.actionPlay = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/play.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPlay.setIcon(icon6)
        self.actionPlay.setObjectName("actionPlay")
        self.actionStop = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/square.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionStop.setIcon(icon7)
        self.actionStop.setObjectName("actionStop")
        self.actionExport_All_Data = QtGui.QAction(MainWindow)
        self.actionExport_All_Data.setIcon(icon2)
        self.actionExport_All_Data.setObjectName("actionExport_All_Data")
        self.actionIndex = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/help-circle.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionIndex.setIcon(icon8)
        self.actionIndex.setObjectName("actionIndex")
        self.actionAbout = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/info.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAbout.setIcon(icon9)
        self.actionAbout.setObjectName("actionAbout")
        self.actionMute = QtGui.QAction(MainWindow)
        self.actionMute.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/volume-x.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMute.setIcon(icon10)
        self.actionMute.setObjectName("actionMute")
        self.menuFile.addAction(self.actionImport_Zip)
        self.menuFile.addAction(self.actionExport_All_Data)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionIndex)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionMute)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionPlay)

        self.retranslateUi(MainWindow)
        self.tabWidgetMain.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plainTextEdit.setPlaceholderText(_translate("MainWindow", "Enter Space Seperated Tags or Dates"))
        self.pushButtonSearch.setText(_translate("MainWindow", "Filter"))
        self.labelSummaryExample.setText(_translate("MainWindow", "Summary Information / Graphics Displayed Here"))
        self.pushButtonExportDisplayed.setText(_translate("MainWindow", "Export as CSV"))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tabDataList), _translate("MainWindow", "Processed Runs"))
        self.labelReviewExample.setText(_translate("MainWindow", "Graphical Display of Data"))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tabReviewData), _translate("MainWindow", "Review Run"))
        self.labelOverallSummaryExample.setText(_translate("MainWindow", "Overall Summary of Findings"))
        self.pushButtonExportAll.setText(_translate("MainWindow", "Export All as CSV"))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tabOverallSummary), _translate("MainWindow", "Overall Summary"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionImport_Zip.setText(_translate("MainWindow", "Import Zip(s)..."))
        self.actionImport_Zip.setToolTip(_translate("MainWindow", "Select one or more zip files to import"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPause.setText(_translate("MainWindow", "Pause"))
        self.actionPlay.setText(_translate("MainWindow", "Play"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionExport_All_Data.setText(_translate("MainWindow", "Export All Data..."))
        self.actionExport_All_Data.setToolTip(_translate("MainWindow", "Export all data in csv format"))
        self.actionIndex.setText(_translate("MainWindow", "Index"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionMute.setText(_translate("MainWindow", "Mute"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
