import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import *  # FileContainer
from texteditor import *

import random  # testing


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor")
        #self.setGeometry(0, 0, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.setCentralWidget(self.tabs)
        
        self.currentEditor = TextEditor()

        self.tabs.addTab(self.currentEditor, "testing")
        self.setCentralWidget(self.tabs)
        

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


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
