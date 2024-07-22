from PyQt6.QtCore import * #temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import random
from historycontroller import *

class FileContainer(QWidget):
    def __init__(self, file_path=""):
        super().__init__()

        self.label_name = file_path

        horizontal_button_layout = QHBoxLayout()
        file_name_label = QLabel(self.label_name)

        vertical_file_button_layout = QVBoxLayout()
        vertical_file_button_frame = QFrame()

        self.open_file_button = QPushButton("Open File", self)
        #self.open_file_button.clicked.connect(self.OpenFileButton)

        self.remove_file_button = QPushButton("Remove File", self)
        self.remove_file_button.clicked.connect(self.remove_file_button_pressed)

        vertical_file_button_layout.addWidget(self.open_file_button)
        vertical_file_button_layout.addWidget(self.remove_file_button)
        vertical_file_button_frame.setLayout(vertical_file_button_layout)

        horizontal_button_layout.addWidget(file_name_label)
        horizontal_button_layout.addWidget(vertical_file_button_frame)

        self.setLayout(horizontal_button_layout)

    def remove_file_button_pressed(self):
        #print("clicked remove file button", self.label_name)
        remove_path_from_recent_file_list(self.label_name)
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
        
        '''for file_path in FetchRecentFileList():
            print(file_path)
            scrollingVLayout.addWidget(FileContainer(file_path))'''
            
        self.recentTabScrollingFrame.setLayout(self.recentTabVerticalLayout)
        self.recentTabPage.setWidget(self.recentTabScrollingFrame)
        
        self.addTab(self.recentTabPage, "Recent")
        
    def AddButton(self, button : FileContainer):
        self.recentTabVerticalLayout.addWidget(button)


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