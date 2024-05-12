from PyQt6.QtCore import * #temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class FileContainer(QWidget):
    def __init__(self, filePath):
        super().__init__()

        print(filePath)
        self.labelName = filePath

        HButtonLayout = QHBoxLayout()
        fileNameLabel = QLabel(self.labelName)
        
        VFileButtonLayout = QVBoxLayout()
        VFileButtonFrame = QFrame()

        self.openFileButton = QPushButton("Open File", self)
        self.openFileButton.clicked.connect(self.onClicked)
        
        self.openFileButton2 = QPushButton("Open File", self)
        self.openFileButton2.clicked.connect(self.onClicked)

        VFileButtonLayout.addWidget(self.openFileButton)
        VFileButtonLayout.addWidget(self.openFileButton2)
        VFileButtonFrame.setLayout(VFileButtonLayout)

        HButtonLayout.addWidget(fileNameLabel)
        HButtonLayout.addWidget(VFileButtonFrame)

        self.setLayout(HButtonLayout)

    def onClicked(self):
        print("clicked button", self.labelName)
