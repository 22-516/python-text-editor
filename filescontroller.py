import os
import shutil
from docx import Document

from docxparser import *
from texteditor import *

def create_file_directories():
    currentDir = os.getcwd()
    if not os.path.exists(data_dir := os.path.join(currentDir, "data")):
        os.makedirs(data_dir)
        
    if not os.path.exists(data_temp_dir := os.path.join(currentDir, "data", "temp")):
        os.makedirs(data_temp_dir)
        
    if not os.path.isfile(recent_files := os.path.join("data", "recent.txt")):
        with open(recent_files, "x") as _:
            pass

def get_data_directory_path():
    return os.path.join(os.getcwd(), "data")

def get_data_temp_directory_path():
    return os.path.join(os.getcwd(), "data", "temp")

def get_recent_file_path():
    return os.path.join(os.getcwd(), "data", "recent.txt")

def file_controller_open_file(selected_file_path, selected_file_extension):
    if not selected_file_path or not os.path.exists(selected_file_path):
        print("no file to open")
        return False

    text_encoding = "utf-8"
    file_content = None

    try:
        match selected_file_extension:
            case ".txt":
                print("txt")
                with open(selected_file_path, "r", encoding=text_encoding) as temp_file:
                    file_content = temp_file.read()
            case ".docx":
                print("docx")
                file_content = parse_docx_file_to_html(selected_file_path)
    except Exception as exception:
        print("file open unsuccessful", exception)
    else:
        print("file open successful")
    finally: 
        return file_content


def file_controller_save_file(current_editor : TextEditor, selected_save_file_path, selected_file_extension):
    print(current_editor, selected_save_file_path, selected_file_extension)
    
    if not selected_save_file_path or not selected_file_extension:
        print("no selected save file path or extension")
        return False

    file_backup = ""
    save_success_state = False
    
    text_encoding = "utf-8"

    if os.path.exists(selected_save_file_path): # sometimes the file may not exist yet (save as)
        file_backup = shutil.copy2(selected_save_file_path, get_data_temp_directory_path()) # save backup of file in case of an error
        print("created backup of selected file")
        
    try:
        match selected_file_extension:
            case ".txt":
                print("txt")
                with open(selected_save_file_path, "w", encoding=text_encoding) as temp_file:
                    temp_file.write(current_editor.toPlainText())
                    current_editor.set_file_path(selected_save_file_path)
            case ".docx":
                print("docx")
                parsed_docx = parse_editor_document_to_docx(current_editor.document())
                #print(selected_save_file_path)
                parsed_docx.save(selected_save_file_path)
    except Exception as exception:
        print("save unsuccessful ", exception)
        if file_backup: 
            shutil.move(file_backup, selected_save_file_path) # replace original file with the backup of the original file
    else:
        print("save successful")
        save_success_state = True
    finally: 
        try: # remove the backup
            os.remove(file_backup)
            print("successfully deleted backup of selected file")
        except FileNotFoundError:
            pass
        
        return save_success_state
