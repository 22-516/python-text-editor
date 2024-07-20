import os
from print_color import print

from PyQt6.QtCore import * #temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from filescontroller import CreateFileDirectories

def CheckIfHistoryFilesExist(): # make sure the file exists and all recent files exist before reading/writing
    CreateFileDirectories()
    
    if not os.path.isfile(recentFilePath := os.path.join("data", "recent.txt")):
        with open(recentFilePath, "x") as filePath:
            pass

    removedFiles = [] # remove all links that are no longer valid
    with open(recentFilePath, "r") as filePath:
        fileContent = filePath.readlines()
        for line in fileContent:
            #print(line.strip(), os.path.exists(line.strip()), color="green")
            if not os.path.isfile(line):
                removedFiles.append(line)
    print("removing files from recent file list", removedFiles, color="purple")
    for removedFilePath in removedFiles:
        RemoveFromRecentFileList(removedFilePath)

def FetchRecentFileList():
    fileList = []
    with open(os.path.join("data", "recent.txt"), "r") as recentFileList:
        while line := recentFileList.readline():
            #print(line.rstrip())
            fileList.append(line.rstrip())
            #print(line.strip(), color="magenta")
    #print(fileList, color="yellow")
    return fileList

def PrependRecentFileList(newFilePath=""):
    RemoveFromRecentFileList(newFilePath)  # remove previous entry

    recentFileList = FetchRecentFileList()
    recentFileList.insert(0, newFilePath)

    with open(os.path.join("data", "recent.txt"), "wt") as fileList:
        #for line in recentFileList:
        fileList.write("\n".join(str(line) for line in recentFileList))
        
    #print(FetchRecentFileList(), color="green")

    '''
    with open(os.path.join("data", "recent.txt"), "r+") as recentFileList:
        tempFile = recentFileList.read() # save file to memory so that we can prepend to the beginning of the file                
        recentFileList.seek(0,0)
        print(newFilePath, color="blue")
        print(tempFile, color="green")
        recentFileList.truncate(0)
        print(newFilePath.strip() + "\n" + tempFile, color="red")
        recentFileList.write(newFilePath + "\n" + tempFile)
        # recentFileList.write(newdata := filePath.strip() + "\n" + tempFile)
        # print(newdata, color="green")'''

def RemoveFromRecentFileList(removedFilePath=""):
    print("removing from recent file list", removedFilePath, tag="history", tag_color="yellow", color="white")

    fileList = FetchRecentFileList()
    if removedFilePath in fileList: # remove the path from file array
        fileList.remove(removedFilePath)

    with open(os.path.join("data", "recent.txt"), "w") as newFileList: # write array to recent file list
        newFileList.write("\n".join(str(line) for line in fileList))

    '''print(FetchRecentFileList(), color="red")

    with open(os.path.join("data", "recent.txt"), "r+") as recentFileList:
        fileContent = recentFileList.readlines()
        recentFileList.seek(0)
        recentFileList.truncate()
        for line in fileContent:
            if line.strip() != removedFilePath:
                recentFileList.write(line.strip())

    print(FetchRecentFileList(), color="red")'''
