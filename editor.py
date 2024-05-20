import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import *  # FileContainer
from texteditor import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor")
        # self.setGeometry(0, 0, 800, 600)

        self.Initalise()
        self.AddPage()

        '''self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready", 5000)'''

        '''recentTabPage = QScrollArea()
        recentTabPage.setAutoFillBackground(True)
        recentTabPage.setWidgetResizable(True)

        scrollingFrame = QFrame()
        scrollingFrame.setAutoFillBackground(True)

        scrollingVLayout = QVBoxLayout()

        for i in range(10):
            tab1 = FileContainer(str(random.randrange(0, 1000000)))
            scrollingVLayout.addWidget(tab1)

        scrollingFrame.setLayout(scrollingVLayout)
        recentTabPage.setWidget(scrollingFrame)

        self.tabs.addTab(recentTabPage, "Recent")
        self.setCentralWidget(self.tabs)'''
        
#   functions
    def Initalise(self):
        self.InitActions()
        self.AddTabs()
        self.AddMenubar()
        self.AddToolbar()

    def InitActions(self):
        self.newPageAction = QAction("&New Page", self) # self.button_action.setToolTip("tooltip")
        self.newPageAction.triggered.connect(self.NewPageButton)

        self.newImageAction = QAction("&Insert Test Image", self)
        self.newImageAction.triggered.connect(self.InsertTestImage)

    def AddTabs(self):
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.currentChanged.connect(self.OnTabChange)
    
    def AddMenubar(self):
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.addMenu("tests")

    def AddToolbar(self):
        self.toolbar = QToolBar("main toolbar", self)
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.newPageAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newImageAction)

    def AddPage(self, pageName="New Document"):
        self.currentEditor = TextEditor()
        self.tabs.addTab(self.currentEditor, pageName)
        self.tabs.setCurrentWidget(self.currentEditor)

#   signals
    def OnTabChange(self):
        self.currentEditor = self.tabs.currentWidget()
        print(self.currentEditor)

#   actions

    def NewPageButton(self):
        self.AddPage()

    def InsertTestImage(self):
        self.currentEditor.insertImage()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
