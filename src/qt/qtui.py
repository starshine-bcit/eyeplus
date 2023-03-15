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
        self.tableViewRuns = QtWidgets.QTableView(self.frameLeftProcessed)
        self.tableViewRuns.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.tableViewRuns.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableViewRuns.setAlternatingRowColors(True)
        self.tableViewRuns.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableViewRuns.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableViewRuns.setObjectName("tableViewRuns")
        self.verticalLayout_6.addWidget(self.tableViewRuns)
        self.horizontalLayoutSearch = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSearch.setObjectName("horizontalLayoutSearch")
        self.labelFilter = QtWidgets.QLabel(self.frameLeftProcessed)
        self.labelFilter.setObjectName("labelFilter")
        self.horizontalLayoutSearch.addWidget(self.labelFilter)
        self.lineEditFilter = QtWidgets.QLineEdit(self.frameLeftProcessed)
        self.lineEditFilter.setText("")
        self.lineEditFilter.setClearButtonEnabled(True)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.horizontalLayoutSearch.addWidget(self.lineEditFilter)
        self.horizontalLayoutSearch.setStretch(1, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayoutSearch)
        self.horizontalLayout_2.addWidget(self.frameLeftProcessed)
        self.frameSummary = QtWidgets.QFrame(self.tabDataList)
        self.frameSummary.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameSummary.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameSummary.setObjectName("frameSummary")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameSummary)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayoutSummaryTitle = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummaryTitle.setObjectName("horizontalLayoutSummaryTitle")
        self.labelSummaryTitle = QtWidgets.QLabel(self.frameSummary)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelSummaryTitle.setFont(font)
        self.labelSummaryTitle.setObjectName("labelSummaryTitle")
        self.horizontalLayoutSummaryTitle.addWidget(self.labelSummaryTitle)
        self.verticalLayout_2.addLayout(self.horizontalLayoutSummaryTitle)
        self.horizontalLayoutSummaryUnderTitle = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummaryUnderTitle.setObjectName("horizontalLayoutSummaryUnderTitle")
        self.labelSummaryDate = QtWidgets.QLabel(self.frameSummary)
        self.labelSummaryDate.setObjectName("labelSummaryDate")
        self.horizontalLayoutSummaryUnderTitle.addWidget(self.labelSummaryDate)
        self.labelSummaryProcessDate = QtWidgets.QLabel(self.frameSummary)
        self.labelSummaryProcessDate.setObjectName("labelSummaryProcessDate")
        self.horizontalLayoutSummaryUnderTitle.addWidget(self.labelSummaryProcessDate)
        self.labelSummaryTag = QtWidgets.QLabel(self.frameSummary)
        self.labelSummaryTag.setObjectName("labelSummaryTag")
        self.horizontalLayoutSummaryUnderTitle.addWidget(self.labelSummaryTag)
        self.horizontalLayoutSummaryUnderTitle.setStretch(0, 1)
        self.horizontalLayoutSummaryUnderTitle.setStretch(1, 1)
        self.horizontalLayoutSummaryUnderTitle.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayoutSummaryUnderTitle)
        self.horizontalLayoutSummaryTextGraphic = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummaryTextGraphic.setSpacing(4)
        self.horizontalLayoutSummaryTextGraphic.setObjectName("horizontalLayoutSummaryTextGraphic")
        self.plainTextEditSummary = QtWidgets.QPlainTextEdit(self.frameSummary)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        self.plainTextEditSummary.setFont(font)
        self.plainTextEditSummary.setObjectName("plainTextEditSummary")
        self.horizontalLayoutSummaryTextGraphic.addWidget(self.plainTextEditSummary)
        self.frameSummaryGraphic1 = QtWidgets.QFrame(self.frameSummary)
        self.frameSummaryGraphic1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameSummaryGraphic1.setObjectName("frameSummaryGraphic1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frameSummaryGraphic1)
        self.horizontalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widgetSummaryGraphic1 = QtWidgets.QWidget(self.frameSummaryGraphic1)
        self.widgetSummaryGraphic1.setObjectName("widgetSummaryGraphic1")
        self.horizontalLayout_4.addWidget(self.widgetSummaryGraphic1)
        self.horizontalLayoutSummaryTextGraphic.addWidget(self.frameSummaryGraphic1)
        self.horizontalLayoutSummaryTextGraphic.setStretch(0, 1)
        self.horizontalLayoutSummaryTextGraphic.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayoutSummaryTextGraphic)
        self.horizontalLayoutSummaryBottomGraphics = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummaryBottomGraphics.setSpacing(4)
        self.horizontalLayoutSummaryBottomGraphics.setObjectName("horizontalLayoutSummaryBottomGraphics")
        self.frameSummaryGraphic2 = QtWidgets.QFrame(self.frameSummary)
        self.frameSummaryGraphic2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameSummaryGraphic2.setObjectName("frameSummaryGraphic2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frameSummaryGraphic2)
        self.horizontalLayout_5.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widgetSummaryGraphic2 = QtWidgets.QWidget(self.frameSummaryGraphic2)
        self.widgetSummaryGraphic2.setObjectName("widgetSummaryGraphic2")
        self.horizontalLayout_5.addWidget(self.widgetSummaryGraphic2)
        self.horizontalLayoutSummaryBottomGraphics.addWidget(self.frameSummaryGraphic2)
        self.frameSummaryGraphic3 = QtWidgets.QFrame(self.frameSummary)
        self.frameSummaryGraphic3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameSummaryGraphic3.setObjectName("frameSummaryGraphic3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frameSummaryGraphic3)
        self.horizontalLayout_6.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.widgetSummaryGraphic3 = QtWidgets.QWidget(self.frameSummaryGraphic3)
        self.widgetSummaryGraphic3.setObjectName("widgetSummaryGraphic3")
        self.horizontalLayout_6.addWidget(self.widgetSummaryGraphic3)
        self.horizontalLayoutSummaryBottomGraphics.addWidget(self.frameSummaryGraphic3)
        self.horizontalLayoutSummaryBottomGraphics.setStretch(0, 1)
        self.horizontalLayoutSummaryBottomGraphics.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayoutSummaryBottomGraphics)
        self.horizontalLayoutSummaryButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummaryButtons.setObjectName("horizontalLayoutSummaryButtons")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutSummaryButtons.addItem(spacerItem)
        self.pushButtonExportDisplayed = QtWidgets.QPushButton(self.frameSummary)
        self.pushButtonExportDisplayed.setMinimumSize(QtCore.QSize(110, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/file-spreadsheet.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonExportDisplayed.setIcon(icon)
        self.pushButtonExportDisplayed.setObjectName("pushButtonExportDisplayed")
        self.horizontalLayoutSummaryButtons.addWidget(self.pushButtonExportDisplayed)
        self.pushButtonOpenReview = QtWidgets.QPushButton(self.frameSummary)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/sidebar-open.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonOpenReview.setIcon(icon1)
        self.pushButtonOpenReview.setObjectName("pushButtonOpenReview")
        self.horizontalLayoutSummaryButtons.addWidget(self.pushButtonOpenReview)
        self.verticalLayout_2.addLayout(self.horizontalLayoutSummaryButtons)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frameReviewImages)
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frameReviewGraphicTop1 = QtWidgets.QFrame(self.frameReviewImages)
        self.frameReviewGraphicTop1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameReviewGraphicTop1.setObjectName("frameReviewGraphicTop1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frameReviewGraphicTop1)
        self.horizontalLayout_7.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widgetReviewGraphic1 = QtWidgets.QWidget(self.frameReviewGraphicTop1)
        self.widgetReviewGraphic1.setObjectName("widgetReviewGraphic1")
        self.horizontalLayout_7.addWidget(self.widgetReviewGraphic1)
        self.horizontalLayout_3.addWidget(self.frameReviewGraphicTop1)
        self.frameReviewGraphicTop2 = QtWidgets.QFrame(self.frameReviewImages)
        self.frameReviewGraphicTop2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameReviewGraphicTop2.setObjectName("frameReviewGraphicTop2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frameReviewGraphicTop2)
        self.horizontalLayout_8.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.widgetReviewGraphic2 = QtWidgets.QWidget(self.frameReviewGraphicTop2)
        self.widgetReviewGraphic2.setObjectName("widgetReviewGraphic2")
        self.horizontalLayout_8.addWidget(self.widgetReviewGraphic2)
        self.horizontalLayout_3.addWidget(self.frameReviewGraphicTop2)
        self.frameReviewGraphicTop3 = QtWidgets.QFrame(self.frameReviewImages)
        self.frameReviewGraphicTop3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameReviewGraphicTop3.setObjectName("frameReviewGraphicTop3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frameReviewGraphicTop3)
        self.horizontalLayout_9.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.widgetReviewGraphic3 = QtWidgets.QWidget(self.frameReviewGraphicTop3)
        self.widgetReviewGraphic3.setObjectName("widgetReviewGraphic3")
        self.horizontalLayout_9.addWidget(self.widgetReviewGraphic3)
        self.horizontalLayout_3.addWidget(self.frameReviewGraphicTop3)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)
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
        self.verticalLayoutReviewRight.setStretch(1, 2)
        self.horizontalLayout.addLayout(self.verticalLayoutReviewRight)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.tabWidgetMain.addTab(self.tabReviewData, "")
        self.tabOverallSummary = QtWidgets.QWidget()
        self.tabOverallSummary.setObjectName("tabOverallSummary")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tabOverallSummary)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayoutOverallMain = QtWidgets.QHBoxLayout()
        self.horizontalLayoutOverallMain.setSpacing(4)
        self.horizontalLayoutOverallMain.setObjectName("horizontalLayoutOverallMain")
        self.verticalLayoutOverallLeft = QtWidgets.QVBoxLayout()
        self.verticalLayoutOverallLeft.setObjectName("verticalLayoutOverallLeft")
        self.labelOverallTitle = QtWidgets.QLabel(self.tabOverallSummary)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelOverallTitle.setFont(font)
        self.labelOverallTitle.setWordWrap(True)
        self.labelOverallTitle.setObjectName("labelOverallTitle")
        self.verticalLayoutOverallLeft.addWidget(self.labelOverallTitle)
        self.plainTextEditOverallStats = QtWidgets.QPlainTextEdit(self.tabOverallSummary)
        self.plainTextEditOverallStats.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.plainTextEditOverallStats.setReadOnly(True)
        self.plainTextEditOverallStats.setObjectName("plainTextEditOverallStats")
        self.verticalLayoutOverallLeft.addWidget(self.plainTextEditOverallStats)
        self.listWidgetOverallSelectRuns = QtWidgets.QListWidget(self.tabOverallSummary)
        self.listWidgetOverallSelectRuns.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.listWidgetOverallSelectRuns.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.listWidgetOverallSelectRuns.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.listWidgetOverallSelectRuns.setAlternatingRowColors(True)
        self.listWidgetOverallSelectRuns.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.listWidgetOverallSelectRuns.setObjectName("listWidgetOverallSelectRuns")
        self.verticalLayoutOverallLeft.addWidget(self.listWidgetOverallSelectRuns)
        self.verticalLayoutOverallLeft.setStretch(1, 2)
        self.verticalLayoutOverallLeft.setStretch(2, 1)
        self.horizontalLayoutOverallMain.addLayout(self.verticalLayoutOverallLeft)
        self.verticalLayoutOverallRight = QtWidgets.QVBoxLayout()
        self.verticalLayoutOverallRight.setObjectName("verticalLayoutOverallRight")
        self.horizontalLayoutOverallTop = QtWidgets.QHBoxLayout()
        self.horizontalLayoutOverallTop.setSpacing(4)
        self.horizontalLayoutOverallTop.setObjectName("horizontalLayoutOverallTop")
        self.frameOverallGraphic1 = QtWidgets.QFrame(self.tabOverallSummary)
        self.frameOverallGraphic1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameOverallGraphic1.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameOverallGraphic1.setObjectName("frameOverallGraphic1")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frameOverallGraphic1)
        self.horizontalLayout_10.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.widgetOverallGraphic1 = QtWidgets.QWidget(self.frameOverallGraphic1)
        self.widgetOverallGraphic1.setObjectName("widgetOverallGraphic1")
        self.horizontalLayout_10.addWidget(self.widgetOverallGraphic1)
        self.horizontalLayoutOverallTop.addWidget(self.frameOverallGraphic1)
        self.frameOverallGraphic2 = QtWidgets.QFrame(self.tabOverallSummary)
        self.frameOverallGraphic2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameOverallGraphic2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameOverallGraphic2.setObjectName("frameOverallGraphic2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frameOverallGraphic2)
        self.horizontalLayout_11.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.widgetOverallGraphic2 = QtWidgets.QWidget(self.frameOverallGraphic2)
        self.widgetOverallGraphic2.setObjectName("widgetOverallGraphic2")
        self.horizontalLayout_11.addWidget(self.widgetOverallGraphic2)
        self.horizontalLayoutOverallTop.addWidget(self.frameOverallGraphic2)
        self.verticalLayoutOverallRight.addLayout(self.horizontalLayoutOverallTop)
        self.frameOverallGraphic3 = QtWidgets.QFrame(self.tabOverallSummary)
        self.frameOverallGraphic3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameOverallGraphic3.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameOverallGraphic3.setObjectName("frameOverallGraphic3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameOverallGraphic3)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widgetOverallGraphic3 = QtWidgets.QWidget(self.frameOverallGraphic3)
        self.widgetOverallGraphic3.setObjectName("widgetOverallGraphic3")
        self.verticalLayout_3.addWidget(self.widgetOverallGraphic3)
        self.horizontalScrollBarLongChart = QtWidgets.QScrollBar(self.frameOverallGraphic3)
        self.horizontalScrollBarLongChart.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalScrollBarLongChart.setObjectName("horizontalScrollBarLongChart")
        self.verticalLayout_3.addWidget(self.horizontalScrollBarLongChart)
        self.verticalLayoutOverallRight.addWidget(self.frameOverallGraphic3)
        self.verticalLayoutOverallRight.setStretch(0, 1)
        self.verticalLayoutOverallRight.setStretch(1, 1)
        self.horizontalLayoutOverallMain.addLayout(self.verticalLayoutOverallRight)
        self.horizontalLayoutOverallMain.setStretch(0, 2)
        self.horizontalLayoutOverallMain.setStretch(1, 5)
        self.verticalLayout_5.addLayout(self.horizontalLayoutOverallMain)
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
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
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
        self.actionReadme = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/help-circle.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionReadme.setIcon(icon8)
        self.actionReadme.setObjectName("actionReadme")
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
        self.actionImport_Folder = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/folder-up.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionImport_Folder.setIcon(icon11)
        self.actionImport_Folder.setObjectName("actionImport_Folder")
        self.actionUsage = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/life-buoy.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionUsage.setIcon(icon12)
        self.actionUsage.setObjectName("actionUsage")
        self.actionAdjust = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/sliders.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAdjust.setIcon(icon13)
        self.actionAdjust.setObjectName("actionAdjust")
        self.menuFile.addAction(self.actionImport_Zip)
        self.menuFile.addAction(self.actionImport_Folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionReadme)
        self.menuHelp.addAction(self.actionUsage)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuActions.addAction(self.actionExport_All_Data)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionMute)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionPlay)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdjust)

        self.retranslateUi(MainWindow)
        self.tabWidgetMain.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelFilter.setText(_translate("MainWindow", "Filter:"))
        self.lineEditFilter.setToolTip(_translate("MainWindow", "Filters by title"))
        self.lineEditFilter.setPlaceholderText(_translate("MainWindow", "Enter Title To Filter Results"))
        self.labelSummaryTitle.setText(_translate("MainWindow", "Summary for Run ID"))
        self.labelSummaryDate.setText(_translate("MainWindow", "Date: "))
        self.labelSummaryProcessDate.setText(_translate("MainWindow", "Processed: "))
        self.labelSummaryTag.setText(_translate("MainWindow", "Title: "))
        self.pushButtonExportDisplayed.setToolTip(_translate("MainWindow", "Export a series for the selected run only"))
        self.pushButtonExportDisplayed.setText(_translate("MainWindow", "Export as CSV"))
        self.pushButtonOpenReview.setToolTip(_translate("MainWindow", "Open For individual review and playback"))
        self.pushButtonOpenReview.setText(_translate("MainWindow", "Open For Review"))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tabDataList), _translate("MainWindow", "Processed Runs"))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tabReviewData), _translate("MainWindow", "Review Run"))
        self.labelOverallTitle.setText(_translate("MainWindow", "Summary For All Runs"))
        self.pushButtonExportAll.setToolTip(_translate("MainWindow", "Export data from all runs in csv format"))
        self.pushButtonExportAll.setText(_translate("MainWindow", "Export All as CSV"))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tabOverallSummary), _translate("MainWindow", "Overall Summary"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuActions.setTitle(_translate("MainWindow", "Actions"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionImport_Zip.setText(_translate("MainWindow", "Import Zip(s)..."))
        self.actionImport_Zip.setToolTip(_translate("MainWindow", "Select one or more zip files to import"))
        self.actionImport_Zip.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionPause.setText(_translate("MainWindow", "Pause"))
        self.actionPause.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionPlay.setText(_translate("MainWindow", "Play"))
        self.actionPlay.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionStop.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExport_All_Data.setText(_translate("MainWindow", "Export All Data..."))
        self.actionExport_All_Data.setToolTip(_translate("MainWindow", "Export data from all runs in csv format"))
        self.actionExport_All_Data.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionReadme.setText(_translate("MainWindow", "Readme..."))
        self.actionReadme.setToolTip(_translate("MainWindow", "Opens the readme file in a new window"))
        self.actionAbout.setText(_translate("MainWindow", "About..."))
        self.actionAbout.setToolTip(_translate("MainWindow", "Opens about window"))
        self.actionMute.setText(_translate("MainWindow", "Mute"))
        self.actionMute.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionImport_Folder.setText(_translate("MainWindow", "Import Folder(s)..."))
        self.actionImport_Folder.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.actionUsage.setText(_translate("MainWindow", "Usage..."))
        self.actionUsage.setToolTip(_translate("MainWindow", "Opens user manual in a new window"))
        self.actionUsage.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionAdjust.setText(_translate("MainWindow", "Adjust"))
        self.actionAdjust.setToolTip(_translate("MainWindow", "Adjust parameters for this run"))
        self.actionAdjust.setShortcut(_translate("MainWindow", "Ctrl+T"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
