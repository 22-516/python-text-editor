from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        # self.setMaximumWidth(1000)

        for i in range(9):
            self.append("testing")


    def insertImage(self):
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
