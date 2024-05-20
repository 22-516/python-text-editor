from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import random

class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        # self.setMaximumWidth(1000)

        randomTestingPageId = str(random.randint(1, 100)) #testing new tabs
        for i in range(9):
            self.append("testing " + randomTestingPageId)

    def insertImage(self): #testing
        cursor = QTextCursor(self.textCursor())
        imageFormat = QTextImageFormat()
        imageFormat.setName(".\images.png")
        cursor.insertImage(imageFormat)

    '''def onClicked(self):
        print("clicked button", self.labelName)

    def onClicked2(self):
        print("clicked button 2", self.labelName)
        self.setParent(None)
        # self.hide()'''
