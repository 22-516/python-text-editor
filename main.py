import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import * #FileContainer

import random #testing

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Open File")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)
        
        recentTabPage = QScrollArea()
        recentTabPage.setAutoFillBackground(True)
        #recentTabPage.setSizeAdjustPolicy()
        recentTabPage.setWidgetResizable(True)
        
        scrollingFrame = QFrame()
        scrollingFrame.setAutoFillBackground(True)
        
        scrollingVLayout = QVBoxLayout()

        for i in range(10):
            tab1 = FileContainer(str(random.randrange(0,1000000)))
            scrollingVLayout.addWidget(tab1)
        
        scrollingFrame.setLayout(scrollingVLayout)
        recentTabPage.setWidget(scrollingFrame)
        
        tabs.addTab(recentTabPage, "Recent")
        self.setCentralWidget(tabs)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
