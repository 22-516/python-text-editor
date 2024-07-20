import os
import shutil
import tempfile

from texteditor import *

def CreateFileDirectories():
    currentDir = os.getcwd()
    if not os.path.exists(dataDir := os.path.join(currentDir, "data")):
        os.makedirs(dataDir)
        
    if not os.path.exists(dataTempDir := os.path.join(currentDir, "data", "temp")):
        os.makedirs(dataTempDir)
        
def GetDataDirectoryPath():
    return os.path.join(os.getcwd(), "data")

def GetDataTempDirectoryPath():
    return os.path.join(os.getcwd(), "data", "temp")

def SaveFile(currentEditor : TextEditor, selectedSaveFilePath, selectedFileExtension):
    print(currentEditor, selectedSaveFilePath, selectedFileExtension)
    
    if not selectedSaveFilePath or not selectedFileExtension:
        print("no selected save file path or extension")
        return False

    fileBackup = None
    saveSuccess = False
    tempDirectoryPath = GetDataTempDirectoryPath()
    
    textEncoding = "utf-8"

    if os.path.exists(selectedSaveFilePath): # save backup of file in case of an error
        fileBackup = shutil.copy2(selectedSaveFilePath, tempDirectoryPath)
        print("created backup of selected file")
        
    try:
        match selectedFileExtension:
            case ".txt":
                print("txt")
                with open(selectedSaveFilePath, "w", encoding=textEncoding) as tempFile:
                    tempFile.write(currentEditor.toPlainText())
                    currentEditor.SetFilePath(selectedSaveFilePath)
                    #self.tabs.setTabText(self.tabs.currentIndex(), self.currentEditor.fileName)
            case ".docx":
                print("docx")
    except:
        print("save unsuccessful")
        if fileBackup: 
            shutil.move(fileBackup, selectedSaveFilePath) # replace original file with the backup of the original file
    else:
        print("save successful")
        saveSuccess = True
    finally: 
        try: # remove the backup
            os.remove(fileBackup)
            print("successfully deleted backup of selected file")
        except FileNotFoundError:
            pass
        
        return saveSuccess
