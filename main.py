import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from GUIController import * #FileContainer

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
'''
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()

        tab1 = FileContainer()
        tab2 = QWidget()

        label1 = QLabel("Recent")
        label2 = QLabel("Pinned")

        button1 = QPushButton("Open File")
        button2 = QPushButton(" File")

        button3 = QFontComboBox()
        layout2.addWidget(button3)
        button4 = QDial()
        layout2.addWidget(button4)

        tab1.layout = layout1
        tab1.layout.addWidget(label1)
        tab1.layout.addWidget(button1)
        tab1.setLayout(tab1.layout)

        tab2.layout = QVBoxLayout()
        tab2.layout.addWidget(label2)
        tab2.layout.addWidget(button2)
        tab2.setLayout(tab2.layout)

        layout1.addLayout(layout2)

        tabs.addTab(tab1, "Tab 1")
        tabs.addTab(tab2, "Tab 2")

        self.setCentralWidget(tabs)'''

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
