from PyQt6.QtCore import * #temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class FileContainer(QWidget):
    def __init__(self, filePath):
        super().__init__()

        print(filePath)
        self.labelName = filePath

        boxlayout = QHBoxLayout()
        fileNameLabel = QLabel(self.labelName)

        self.openFileButton = QPushButton("Open File", self)
        self.openFileButton.clicked.connect(self.onClicked)

        boxlayout.addWidget(fileNameLabel)
        boxlayout.addWidget(self.openFileButton)

        self.setLayout(boxlayout)

    def onClicked(self):
        print("clicked button", self.labelName)
