from PyQt6.QtCore import * #temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import random
from historycontroller import *

class FileContainer(QWidget):
    def __init__(self, filePath=""):
        super().__init__()

        self.labelName = filePath

        HButtonLayout = QHBoxLayout()
        fileNameLabel = QLabel(self.labelName)

        VFileButtonLayout = QVBoxLayout()
        VFileButtonFrame = QFrame()

        self.openFileButton = QPushButton("Open File", self)
        #self.openFileButton.clicked.connect(self.OpenFileButton)

        self.removeFileButton = QPushButton("Remove File", self)
        self.removeFileButton.clicked.connect(self.RemoveFileButton)

        VFileButtonLayout.addWidget(self.openFileButton)
        VFileButtonLayout.addWidget(self.removeFileButton)
        VFileButtonFrame.setLayout(VFileButtonLayout)

        HButtonLayout.addWidget(fileNameLabel)
        HButtonLayout.addWidget(VFileButtonFrame)

        self.setLayout(HButtonLayout)

    def RemoveFileButton(self):
        #print("clicked remove file button", self.labelName)
        RemoveFromRecentFileList(self.labelName)
        self.setParent(None)
        # self.hide()

class HomeWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home")

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)
        
        #print(FetchRecentFileList())
        
        self.recentTabPage = QScrollArea()
        self.recentTabPage.setAutoFillBackground(True)
        self.recentTabPage.setWidgetResizable(True)
        
        self.recentTabScrollingFrame = QFrame()
        self.recentTabScrollingFrame.setAutoFillBackground(True)
        
        self.recentTabVerticalLayout = QVBoxLayout()
        
        '''for filePath in FetchRecentFileList():
            print(filePath)
            scrollingVLayout.addWidget(FileContainer(filePath))'''
            
        self.recentTabScrollingFrame.setLayout(self.recentTabVerticalLayout)
        self.recentTabPage.setWidget(self.recentTabScrollingFrame)
        
        self.addTab(self.recentTabPage, "Recent")


'''class TabCloseDialog(QDialog):
    def __init__(self, documentName="testing"):
        super().__init__()

        self.setWindowTitle("Confirmation")

        QBtn = (
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Discard | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Close tab \"" + documentName + "\"")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)'''


class TabCloseDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle("Confirmation")
        self.setText("Unsaved Changes")
        self.setInformativeText("There are unsaved changes. Would you like to save your changes or discard them?")

        self.setStandardButtons(
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel
        )
        self.setDefaultButton(QMessageBox.StandardButton.Save)
        self.setEscapeButton(QMessageBox.StandardButton.Cancel)

#def OpenFileFromHomePage():
#    def 