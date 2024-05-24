import sys
from print_color import print

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import *  # FileContainer, TabCloseDialog
from texteditor import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor")
        # self.setGeometry(0, 0, 800, 600)

        self.InitaliseEditorWindow()
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
    def InitaliseEditorWindow(self):
        print("initalising editor window", tag="init", tag_color="magenta", color="white")
        self.InitActions()
        self.AddTabs()
        self.AddMenubar()
        self.AddToolbar()

    def InitActions(self):
        print("initalising actions", tag="init", tag_color="magenta", color="white")
        self.newPageAction = QAction("&New Page", self) 
        # self.button_action.setToolTip("tooltip")
        self.newPageAction.triggered.connect(self.NewPageButton)

        self.newImageAction = QAction("&Insert Test Image", self)
        self.newImageAction.triggered.connect(self.InsertTestImage)

    def AddTabs(self):
        print("initalising tabs", tag="init", tag_color="magenta", color="white")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.OnTabChange)
        self.tabs.tabCloseRequested.connect(self.OnTabClose)

    def AddMenubar(self):
        print("initalising menu bar", tag="init", tag_color="magenta", color="white")
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        fileMenuButton = self.menubar.addMenu("File")
        fileMenuButton.addAction(self.newPageAction)

    def AddToolbar(self):
        print("initalising tool bar", tag="init", tag_color="magenta", color="white")
        self.toolbar = QToolBar("main toolbar", self)
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.newPageAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newImageAction)

    def AddPage(self, pageName="New Document"):
        print("adding new page", tag="editor", tag_color="green", color="white")
        self.currentEditor = TextEditor()
        self.tabs.addTab(self.currentEditor, pageName)
        self.tabs.setCurrentWidget(self.currentEditor)

    #   signals
    def OnTabChange(self):
        self.currentEditor = self.tabs.currentWidget()
        print("tab changed to", self.currentEditor, tag="editor", tag_color="green", color="white")

    def OnTabClose(self, tabIndex):
        self.tabs.setCurrentIndex(tabIndex)
        print("prompting close ", self.currentEditor, tag="editor", tag_color="green", color="yellow")
        
        closeTabDialogAnswer = TabCloseDialog().exec()
        if closeTabDialogAnswer == QMessageBox.StandardButton.Save:
            # self.currentEditor.save()
            print("save", tag="info", tag_color="blue", color="white")
        elif closeTabDialogAnswer == QMessageBox.StandardButton.Discard:
            print("discard", tag="info", tag_color="blue", color="white")
        elif closeTabDialogAnswer == QMessageBox.StandardButton.Cancel:
            print("cancel", tag="info", tag_color="blue", color="white")
            return

        self.tabs.removeTab(tabIndex)

        if self.tabs.count() <= 0: #ensure always one editor page available
            self.AddPage()

    #   actions
    def NewPageButton(self):
        print("new page prompted", tag="editor", tag_color="green", color="white")
        self.AddPage()

    def InsertTestImage(self):
        print("inserting test image", self.currentEditor, tag="editor", tag_color="green", color="white")
        self.currentEditor.insertImage()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
