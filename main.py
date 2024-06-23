import sys
import re
from functools import partial
from print_color import print

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import *  # FileContainer, TabCloseDialog
from texteditor import *
from historycontroller import *

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

    #   functions
    #       initalisation
    def InitaliseEditorWindow(self):
        print("initalising editor window", tag="init", tag_color="magenta", color="white")
        self.InitActions()
        self.InitObjects()
        self.InitTabs()
        self.InitMenubar()
        self.InitToolbar()

    def InitActions(self):
        print("initalising actions", tag="init", tag_color="magenta", color="white")
        self.newPageAction = QAction("&New Page", self) 
        # self.button_action.setToolTip("tooltip")
        self.newPageAction.triggered.connect(self.NewPageButton)

        self.openFileAction = QAction("&Open", self)
        self.openFileAction.triggered.connect(self.OpenFile)

        self.saveFileAction = QAction("&Save", self)
        self.saveFileAction.triggered.connect(self.SaveFile)

        self.saveAsFileAction = QAction("&Save As", self)
        self.saveAsFileAction.triggered.connect(partial(self.SaveFile, True))

        self.homePageAction = QAction("&Home", self)
        self.homePageAction.triggered.connect(self.OpenHomePage)

        self.newImageAction = QAction("&Insert Test Image", self)
        self.newImageAction.triggered.connect(self.InsertTestImage)
        # text formatting actions
        self.textBoldAction = QAction("&Bold", self)
        self.textBoldAction.triggered.connect(self.FormatTextBold)
        self.textBoldAction.setCheckable(True)
        self.textBoldAction.setIcon(QIcon(os.path.join("images", "icons", "edit-bold.png")))

        self.textUnderlineAction = QAction("&Underline", self)
        self.textUnderlineAction.triggered.connect(self.FormatTextUnderline)
        self.textUnderlineAction.setCheckable(True)
        self.textUnderlineAction.setIcon(QIcon(os.path.join("images", "icons", "edit-underline.png")))

        self.textItalicAction = QAction("&Italic", self)
        self.textItalicAction.triggered.connect(self.FormatTextItalics)
        self.textItalicAction.setCheckable(True)
        self.textItalicAction.setIcon(QIcon(os.path.join("images", "icons", "edit-italic.png")))
        
    def InitObjects(self):
        self.fontComboBoxWidget = QFontComboBox(self)
        self.fontComboBoxWidget.currentFontChanged.connect(self.OnFontComboboxChanged)
        self.fontComboBoxWidget.setWritingSystem(QFontDatabase.WritingSystem.Latin) # for inital testing with english fonts
        #self.fontComboBoxWidget

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

        self.menubar.addAction(self.homePageAction)

        fileMenuButton = self.menubar.addMenu("File")
        # fileMenuButton.addAction(self.newPageAction)
        fileMenuButton.addAction(self.saveFileAction)
        fileMenuButton.addAction(self.saveAsFileAction)
        fileMenuButton.addAction(self.openFileAction)

    def InitToolbar(self):
        print("initalising tool bar", tag="init", tag_color="magenta", color="white")
        self.toolbar = QToolBar("main toolbar", self)
        # self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.newImageAction) # for image testing

        self.toolbar.addAction(self.textBoldAction)
        self.toolbar.addAction(self.textUnderlineAction)
        self.toolbar.addAction(self.textItalicAction)
        
        self.toolbar.addWidget(self.fontComboBoxWidget)

    #       editor functionality

    def AddPage(self, filePath=""):#pageName="New Document"):
        print("adding new page with path metadata:", str(filePath) or "None", tag="editor", tag_color="green", color="white")
        self.currentEditor = TextEditor(filePath)
        self.tabs.addTab(self.currentEditor, self.currentEditor.fileName)
        self.tabs.setCurrentWidget(self.currentEditor)

        self.currentEditor.currentCharFormatChanged.connect(self.OnSelectionChange)

    def OpenFile(self, selectedFile=""):
        CheckIfHistoryFilesExist()
        print("attempting to open from file", tag="info", tag_color="blue", color="white")
        if not selectedFile:
            selectedFile, selectedFilter = QFileDialog.getOpenFileName(self, "Open File")

        for tab in range(self.tabs.count()):
            # print(self.tabs.widget(tab).filePath)
            if selectedFile == self.tabs.widget(tab).filePath:
                print("file with path", selectedFile, "already open in editor, switching tabs" or "None", tag="editor", tag_color="green", color="white")
                self.tabs.setCurrentIndex(tab)
                return

        fileContent = None
        if selectedFile:
            try:
                with open(selectedFile, "r", encoding="utf-8") as tempFile:
                    fileContent = tempFile.read()
            except FileNotFoundError:
                pass
        if fileContent or (not fileContent and selectedFile): #if file selected but empty contents (no text)
            self.AddPage(selectedFile) #(os.path.basename(selectedFile))
            self.currentEditor.setText(fileContent)
            PrependRecentFileList(selectedFile)
        else:
            print("opened file does not exist or no content", tag="info", tag_color="blue", color="white")

    def SaveFile(self, saveAs=False):
        CheckIfHistoryFilesExist()
        print("attempting to save to file, new file:", saveAs, tag="info", tag_color="blue", color="white")

        tempFilePath = self.currentEditor.filePath
        selectedExtension = ".txt"
        fileContent = None
        if not tempFilePath or saveAs:
            supportedFileFilter = "Text File (*.txt);;Word Document (*.docx)"
            tempFilePath, selectedFilter = QFileDialog.getSaveFileName(self, "Save File", "", supportedFileFilter)
            selectedExtension = re.search(r'\((.+?)\)', selectedFilter or supportedFileFilter).group(1).replace('*',"") # add extension so file is saved with the selected extension
            # if not os.path.splitext(tempFilePath)[1]:
            if os.path.splitext(tempFilePath)[1] != selectedExtension:
                tempFilePath = tempFilePath + selectedExtension

        if tempFilePath:
            # successfully found file path to save to
            PrependRecentFileList(tempFilePath)
            if os.path.exists(tempFilePath):
                with open(tempFilePath, "r", encoding="utf-8") as tempFile: #save copy in memory before writing
                    fileContent = tempFile.read()
            try:
                with open(tempFilePath, "w", encoding="utf-8") as tempFile:
                    tempFile.write(self.currentEditor.toPlainText())
                    self.currentEditor.SetFilePath(tempFilePath)
                    self.tabs.setTabText(self.tabs.currentIndex(), self.currentEditor.fileName)
                    return True
            except:
                with open(tempFilePath, "w", encoding="utf-8") as tempFile: # replace with old content if possible
                    tempFile.write(fileContent)
                    print("error while trying to save", str(tempFilePath), str(fileContent), tag="error", tag_color="red", color="white")
        print("save unsuccessful", str(tempFilePath), tag="info", tag_color="blue", color="white")
        return False

    #   signals
    def OnSelectionChange(self): # check all qaction for continuity
        self.textBoldAction.setChecked(True if not self.currentEditor.fontWeight() == QFont.Weight.Normal else False)
        self.textUnderlineAction.setChecked(True if self.currentEditor.fontUnderline() else False)
        self.textItalicAction.setChecked(True if self.currentEditor.fontItalic() else False)
        with QSignalBlocker(self.fontComboBoxWidget): # block font combobox signal to prevent loop where upon selection change, font combobox changes font which changes font of selected text
            self.fontComboBoxWidget.setCurrentFont(self.currentEditor.currentFont())

    def OnTabChange(self):
        self.currentEditor = self.tabs.currentWidget()
        self.OnSelectionChange() # update text formatting qactions checked status upon changing tabs to preserve continuity between tabs
        print("tab changed to", self.currentEditor, tag="editor", tag_color="green", color="white")

    def OnTabClose(self, tabIndex):
        self.tabs.setCurrentIndex(tabIndex)
        print("prompting close ", self.currentEditor, tag="editor", tag_color="green", color="yellow")

        closeTabDialogAnswer = TabCloseDialog().exec()
        match closeTabDialogAnswer:
            case QMessageBox.StandardButton.Save:
                print("save", tag="info", tag_color="blue", color="white")
                if not self.SaveFile():
                    return
            case QMessageBox.StandardButton.Discard:
                print("discard", tag="info", tag_color="blue", color="white")
            case QMessageBox.StandardButton.Cancel:
                print("cancel", tag="info", tag_color="blue", color="white")
                return
            case _:
                print("data not saved", tag="info", tag_color="blue", color="white")
                return

        self.tabs.removeTab(tabIndex) # close tab

        if self.tabs.count() <= 0: # ensure always one editor page available
            self.AddPage()
            
    def OnFontComboboxChanged(self, newFont):
        self.currentEditor.OnFontChanged(newFont)

    #   actions
    def NewPageButton(self):
        print("new page prompted", tag="editor", tag_color="green", color="white")
        self.AddPage()

    def InsertTestImage(self):
        print("inserting test image", self.currentEditor, tag="editor", tag_color="green", color="white")
        self.currentEditor.InsertImage()

    def OpenHomePage(self):
        CheckIfHistoryFilesExist() # make sure the file exists before reading/writing
        self.homeWindow = HomeWindow()

        for filePath in FetchRecentFileList():
            print(filePath)
            self.homeWindow.recentTabVerticalLayout.addWidget(tempContainer := FileContainer(filePath))
            tempContainer.openFileButton.clicked.connect(partial(self.OpenFile, tempContainer.labelName)) # so the buttons have functionality

        self.homeWindow.show()

    # text formatting actions
    '''    def FormatTextBold(self):
        self.currentEditor.setFontWeight(QFont.Weight.Bold if self.currentEditor.fontWeight() == QFont.Weight.Normal else QFont.Weight.Normal)

    def FormatTextUnderline(self):
        self.currentEditor.setFontUnderline(not self.currentEditor.fontUnderline())

    def FormatTextItalics(self):
        self.currentEditor.setFontItalic(not self.currentEditor.fontItalic())'''

    def FormatTextBold(self):
        self.currentEditor.ToggleSelectedBold()

    def FormatTextUnderline(self):
        self.currentEditor.ToggleSelectedUnderline()

    def FormatTextItalics(self):
        self.currentEditor.ToggleSelectedItalics()
        
    def FormatTextFont(self, newFont):
        self.currentEditor.OnFontChanged(newFont)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
