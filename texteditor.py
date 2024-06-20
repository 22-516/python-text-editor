import os
import random

from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class TextEditor(QTextEdit):
    def __init__(self, filePath=""):
        super().__init__()

        self.SetFilePath(filePath)

        # print(self.filePath, self.fileName, self.fileExtension)

        randomTestingPageId = str(random.randint(1, 100)) #testing new tabs
        for i in range(9):
            self.append("testing " + randomTestingPageId)

    def InsertImage(self): #testing
        cursor = QTextCursor(self.textCursor())
        imageFormat = QTextImageFormat()
        imageFormat.setName(".\images.png")
        cursor.insertImage(imageFormat)

    def SetFilePath(self, filePath=""):
        self.filePath = filePath      
        _1, fileExtension = os.path.splitext(filePath)
        self.fileName = os.path.basename(filePath) or "New Document"
        self.fileExtension = fileExtension or None

    # text formatting

    def ToggleSelectedBold(self):
        print(self.fontWeight())
        self.setFontWeight(newFontWeight := QFont.Weight.Bold if self.fontWeight() == QFont.Weight.Normal else QFont.Weight.Normal)
        print(newFontWeight)
        return newFontWeight

    def ToggleSelectedUnderline(self):
        print(self.fontUnderline())
        self.setFontUnderline(newFontUnderline := not self.fontUnderline())
        print(newFontUnderline)
        return newFontUnderline

    def ToggleSelectedItalics(self):
        print(self.fontItalic())
        self.setFontItalic(newFontItalics := not self.fontItalic())
        print(newFontItalics)
        return newFontItalics
    
    def OnFontChanged(self, newFont : QFont):
        self.setCurrentFont(newFont)

'''def onClicked(self):
        print("clicked button", self.labelName)

    def onClicked2(self):
        print("clicked button 2", self.labelName)
        self.setParent(None)
        # self.hide()'''
