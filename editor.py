import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import *  # FileContainer
from texteditor import *

import random  # testing
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor")
        # self.setGeometry(0, 0, 800, 600)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.AddToolbar()

        self.currentEditor = TextEditor()

        self.tabs.addTab(self.currentEditor, "testing")
        self.setCentralWidget(self.tabs)
        

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

    def AddToolbar(self):
        self.toolbar = QToolBar("main toolbar", self)
        self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addWidget(QLabel("toolbar test"))
        self.toolbar.addWidget(QCheckBox("checkbox"))
        
        button_action = QAction("&Button", self)
        button_action.setStatusTip("a button")
        button_action.triggered.connect(self.buttonClick)
        #button_action.setCheckable(True)
        self.toolbar.addAction(button_action)
        #self.toolbar.addSeparator()
        
    def buttonClick(self, string1):
        print(string1)
        self.currentEditor.insertImage()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
