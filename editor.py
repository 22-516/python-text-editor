import sys
import os
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
    #       initalisation
    def InitaliseEditorWindow(self):
        print("initalising editor window", tag="init", tag_color="magenta", color="white")
        self.InitActions()
        self.InitTabs()
        self.InitMenubar()
        self.InitToolbar()

    def InitActions(self):
        print("initalising actions", tag="init", tag_color="magenta", color="white")
        self.newPageAction = QAction("&New Page", self) 
        # self.button_action.setToolTip("tooltip")
        self.newPageAction.triggered.connect(self.NewPageButton)

        self.newImageAction = QAction("&Insert Test Image", self)
        self.newImageAction.triggered.connect(self.InsertTestImage)
        
        self.openFileAction = QAction("&Open File", self)
        self.openFileAction.triggered.connect(self.OpenFile)
        
        self.saveFileAction = QAction("&Save File", self)
        self.saveFileAction.triggered.connect(self.SaveFile)

    def InitTabs(self):
        print("initalising tabs", tag="init", tag_color="magenta", color="white")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabsClosable(True)
        
        newTabButton = QPushButton(self) # the plus button
        newTabButton.setText("+")
        self.tabs.setCornerWidget(newTabButton)
        
        newTabButton.clicked.connect(self.NewPageButton)
        self.tabs.currentChanged.connect(self.OnTabChange)
        self.tabs.tabCloseRequested.connect(self.OnTabClose)

    def InitMenubar(self):
        print("initalising menu bar", tag="init", tag_color="magenta", color="white")
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        
        fileMenuButton = self.menubar.addMenu("File")
        fileMenuButton.addAction(self.newPageAction)
        fileMenuButton.addAction(self.openFileAction)

    def InitToolbar(self):
        print("initalising tool bar", tag="init", tag_color="magenta", color="white")
        self.toolbar = QToolBar("main toolbar", self)
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.newPageAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newImageAction)
        self.toolbar.addAction(self.openFileAction)
        self.toolbar.addAction(self.saveFileAction)
        
    #       editor functionality

    def AddPage(self, filePath=""):#pageName="New Document"):
        print("adding new page with path:", filePath or "None", tag="editor", tag_color="green", color="white")
        self.currentEditor = TextEditor(filePath)
        self.tabs.addTab(self.currentEditor, self.currentEditor.fileName)
        self.tabs.setCurrentWidget(self.currentEditor)
        
    def OpenFile(self):
        print("attempting to open from file", tag="editor", tag_color="green", color="white")
        selectedFile, extension = QFileDialog.getOpenFileName(self, "Open File")
        fileContent = None
        if selectedFile:
            try:
                with open(selectedFile, "r", encoding="utf-8") as tempFile:
                    fileContent = tempFile.read()
            except FileNotFoundError:
                pass
        if fileContent:
            self.AddPage(selectedFile) #(os.path.basename(selectedFile))
            self.currentEditor.setText(fileContent)
        else:
            print("opened file does not exist or no content", tag="info", tag_color="blue", color="white")
            
    def SaveFile(self):
        print("attempting to save to file", tag="editor", tag_color="green", color="white")
        
        filePath = self.currentEditor.filePath
        if not filePath:
            filePath, _1 = QFileDialog.getSaveFileName(self, "Save File")
        
        if filePath:
            # successfully found file path to save to
            print(filePath)
            with open(filePath, "w") as tempFile:
                tempFile.write(self.currentEditor.toPlainText())

    #   signals
    def OnTabChange(self):
        self.currentEditor = self.tabs.currentWidget()
        print("tab changed to", self.currentEditor, tag="editor", tag_color="green", color="white")

    def OnTabClose(self, tabIndex):
        self.tabs.setCurrentIndex(tabIndex)
        print("prompting close ", self.currentEditor, tag="editor", tag_color="green", color="yellow")
        
        closeTabDialogAnswer = TabCloseDialog().exec()
        
        match closeTabDialogAnswer:
            case QMessageBox.StandardButton.Save:
                print("save", tag="info", tag_color="blue", color="white")
            case QMessageBox.StandardButton.Discard:
                print("discard", tag="info", tag_color="blue", color="white")
            case QMessageBox.StandardButton.Cancel:
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
