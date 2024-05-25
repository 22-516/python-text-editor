import os

from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import random

class TextEditor(QTextEdit):
    def __init__(self, filePath=""):
        super().__init__()

        self.filePath = filePath      
        _1, fileExtension = os.path.splitext(filePath)
        self.fileName = os.path.basename(filePath) or "New Document"
        self.fileExtension = fileExtension or None
        
        #print(self.filePath, self.fileName, self.fileExtension)

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
