from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        #layout = QVBoxLayout(self)
        
        
        #self.textArea = QTextEdit()
        
        for i in range(9):
            self.append("testing")
        
        #layout.addWidget(self.textArea)
        #print(self.textArea.document())
        
        

    '''def onClicked(self):
        print("clicked button", self.labelName)

    def onClicked2(self):
        print("clicked button 2", self.labelName)
        self.setParent(None)
        # self.hide()'''
