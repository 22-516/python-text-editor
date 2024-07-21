import sys
import re
from functools import partial
from print_color import print

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from guicontroller import *  # FileContainer, TabCloseDialog
from texteditor import *
from historycontroller import *
from filescontroller import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor")
        # self.setGeometry(0, 0, 800, 600)

        self.initalise_editor_window()
        self.add_editor_page()

        '''self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready", 5000)'''

    #   functions
    #       initalisation
    def initalise_editor_window(self):
        print("initalising editor window", tag="init", tag_color="magenta", color="white")
        self.init_actions()
        self.init_objects()
        self.init_tabs()
        self.init_menubar()
        self.init_toolbar()
        
        create_file_directories()

    def init_actions(self):
        print("initalising actions", tag="init", tag_color="magenta", color="white")
        self.new_page_action = QAction("&New Page", self) 
        # self.button_action.setToolTip("tooltip")
        self.new_page_action.triggered.connect(self.new_page_button_pressed)

        self.open_file_action = QAction("&Open", self)
        self.open_file_action.triggered.connect(self.open_file)

        self.save_file_action = QAction("&Save", self)
        self.save_file_action.triggered.connect(self.save_file)

        self.save_as_file_action = QAction("&Save As", self)
        self.save_as_file_action.triggered.connect(partial(self.save_file, True))

        self.home_page_action = QAction("&Home", self)
        self.home_page_action.triggered.connect(self.open_home_page)

        self.insert_image_action = QAction("&Insert Test Image", self)
        self.insert_image_action.triggered.connect(self.insert_image_button_pressed)
        # text formatting actions
        self.text_bold_action = QAction("&Bold", self)
        self.text_bold_action.triggered.connect(self.format_text_bold)
        self.text_bold_action.setCheckable(True)
        self.text_bold_action.setIcon(QIcon(os.path.join("images", "icons", "edit-bold.png")))

        self.text_underline_action = QAction("&Underline", self)
        self.text_underline_action.triggered.connect(self.format_text_underline)
        self.text_underline_action.setCheckable(True)
        self.text_underline_action.setIcon(QIcon(os.path.join("images", "icons", "edit-underline.png")))

        self.text_italic_action = QAction("&Italic", self)
        self.text_italic_action.triggered.connect(self.format_text_italics)
        self.text_italic_action.setCheckable(True)
        self.text_italic_action.setIcon(QIcon(os.path.join("images", "icons", "edit-italic.png")))
        
    def init_objects(self):
        self.font_combo_box_widget = QFontComboBox(self)
        self.font_combo_box_widget.currentFontChanged.connect(self.format_text_font)
        self.font_combo_box_widget.setWritingSystem(QFontDatabase.WritingSystem.Latin) # for inital testing with english fonts
        #self.font_combo_box_widget

    def init_tabs(self):
        print("initalising tabs", tag="init", tag_color="magenta", color="white")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabsClosable(True)

        new_tab_button = QPushButton(self) # the plus button
        new_tab_button.setText("+")
        self.tabs.setCornerWidget(new_tab_button)

        new_tab_button.clicked.connect(self.new_page_button_pressed)
        self.tabs.currentChanged.connect(self.on_tab_change)
        self.tabs.tabCloseRequested.connect(self.on_tab_close)

    def init_menubar(self):
        print("initalising menu bar", tag="init", tag_color="magenta", color="white")
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.menubar.addAction(self.home_page_action)

        file_menu_button = self.menubar.addMenu("File")
        # file_menu_button.addAction(self.new_page_action)
        file_menu_button.addAction(self.save_file_action)
        file_menu_button.addAction(self.save_as_file_action)
        file_menu_button.addAction(self.open_file_action)

    def init_toolbar(self):
        print("initalising tool bar", tag="init", tag_color="magenta", color="white")
        self.toolbar = QToolBar("main toolbar", self)
        # self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.insert_image_action) # for image testing

        self.toolbar.addAction(self.text_bold_action)
        self.toolbar.addAction(self.text_underline_action)
        self.toolbar.addAction(self.text_italic_action)
        
        self.toolbar.addWidget(self.font_combo_box_widget)

    #       editor functionality

    def add_editor_page(self, file_path=""):#pageName="New Document"):
        print("adding new page with path metadata:", str(file_path) or "None", tag="editor", tag_color="green", color="white")
        self.current_editor = TextEditor(file_path)
        self.tabs.addTab(self.current_editor, self.current_editor.file_name)
        self.tabs.setCurrentWidget(self.current_editor)

        self.current_editor.currentCharFormatChanged.connect(self.on_editor_selection_change)

    def open_file(self, selected_file=""):
        print("attempting to open from file", tag="info", tag_color="blue", color="white")
        if not selected_file:
            selected_file, selected_filter = QFileDialog.getOpenFileName(self, "Open File")

        for tab in range(self.tabs.count()):
            if selected_file == self.tabs.widget(tab).file_path:
                prepend_recent_file_list(selected_file)
                print("file with path", selected_file, "already open in editor, switching tabs" or "None", tag="editor", tag_color="green", color="white")
                self.tabs.setCurrentIndex(tab)
                return

        file_content = None
        if selected_file:
            try:
                with open(selected_file, "r", encoding="utf-8") as temp_file:
                    file_content = temp_file.read()
            except FileNotFoundError:
                pass
        if file_content or (not file_content and selected_file): #if file selected but empty contents (no text)
            self.add_editor_page(selected_file) #(os.path.basename(selected_file))
            self.current_editor.setText(file_content)
            prepend_recent_file_list(selected_file)
        else:
            print("opened file does not exist or no content", tag="info", tag_color="blue", color="white")

    def save_file(self, save_as=False):
        print("attempting to save to file, new file:", save_as, tag="info", tag_color="blue", color="white")

        selected_save_file_path = self.current_editor.file_path
        selected_file_extension = ".txt"
        
        if not selected_save_file_path or save_as:
            supported_file_filter = "Text File (*.txt);;Word Document (*.docx)"
            selected_save_file_path, selected_filter = QFileDialog.getSaveFileName(self, "Save File", "", supported_file_filter)
            selected_file_extension = re.search(r'\((.+?)\)', selected_filter or supported_file_filter).group(1).replace('*',"") # add extension so file is saved with the selected extension
            # if not os.path.splitext(selected_save_file_path)[1]:
            if selected_save_file_path and os.path.splitext(selected_save_file_path)[1] != selected_file_extension:
                selected_save_file_path = (selected_save_file_path + selected_file_extension).strip()
                
        if file_controller_save_file(self.current_editor, selected_save_file_path, selected_file_extension):
            self.tabs.setTabText(self.tabs.currentIndex(), self.current_editor.file_name)

        # if selected_save_file_path and selected_save_file_path != selected_file_extension: # if the string is not selected extension (checks if the user selected something to save as)
        #     # successfully found file path to save to
        #     PrependRecentFileList(selected_save_file_path)
        #     if os.path.exists(selected_save_file_path):
        #         with open(selected_save_file_path, "r", encoding="utf-8") as temp_file: #save copy in memory before writing
        #             file_content = temp_file.read()
        #     try:
        #         with open(selected_save_file_path, "w", encoding="utf-8") as temp_file:
        #             temp_file.write(self.current_editor.toPlainText())
        #             self.current_editor.SetFilePath(selected_save_file_path)
        #             self.tabs.setTabText(self.tabs.currentIndex(), self.current_editor.file_name)
        #             return True
        #     except:
        #         with open(selected_save_file_path, "w", encoding="utf-8") as temp_file: # replace with old content if possible
        #             temp_file.write(file_content)
        #             print("error while trying to save", str(selected_save_file_path), str(file_content), tag="error", tag_color="red", color="white")
        # print("save unsuccessful", str(selected_save_file_path), tag="info", tag_color="blue", color="white")
        # return False

    #   signals
    def on_editor_selection_change(self): # check all qaction for continuity
        if self.current_editor: # if the editor exists (prevents issues when tab is closed)
            self.text_bold_action.setChecked(True if not self.current_editor.fontWeight() == QFont.Weight.Normal else False)
            self.text_underline_action.setChecked(True if self.current_editor.fontUnderline() else False)
            self.text_italic_action.setChecked(True if self.current_editor.fontItalic() else False)
            with QSignalBlocker(self.font_combo_box_widget): # block font combobox signal to prevent loop where upon selection change, font combobox changes font which changes font of selected text
                self.font_combo_box_widget.setCurrentFont(self.current_editor.currentFont())

    def on_tab_change(self):
        self.current_editor = self.tabs.currentWidget()
        self.on_editor_selection_change() # update text formatting qactions checked status upon changing tabs to preserve continuity between tabs
        print("tab changed to", self.current_editor, tag="editor", tag_color="green", color="white")

    def on_tab_close(self, tab_index):
        self.tabs.setCurrentIndex(tab_index)
        print("prompting close ", self.current_editor, tag="editor", tag_color="green", color="yellow")

        close_tab_dialog_answer = TabCloseDialog().exec()
        match close_tab_dialog_answer:
            case QMessageBox.StandardButton.Save:
                print("save", tag="info", tag_color="blue", color="white")
                if not self.save_file():
                    return
            case QMessageBox.StandardButton.Discard:
                print("discard", tag="info", tag_color="blue", color="white")
            case QMessageBox.StandardButton.Cancel:
                print("cancel", tag="info", tag_color="blue", color="white")
                return
            case _:
                print("data not saved", tag="info", tag_color="blue", color="white")
                return

        self.tabs.removeTab(tab_index) # close tab

        if self.tabs.count() <= 0: # ensure always one editor page available
            self.add_editor_page()

    #   actions
    def new_page_button_pressed(self):
        print("new page prompted", tag="editor", tag_color="green", color="white")
        self.add_editor_page()

    def insert_image_button_pressed(self):
        print("inserting test image", self.current_editor, tag="editor", tag_color="green", color="white")
        self.current_editor.InsertImage()

    def open_home_page(self):
        home_window = HomeWindow()

        for file_path in fetch_recent_file_list():
            print(file_path)
            home_window.AddButton(temp_container := FileContainer(file_path))
            temp_container.openFileButton.clicked.connect(partial(self.open_file, temp_container.labelName)) # so the buttons have functionality

        home_window.show()

    # text formatting actions
    def format_text_bold(self):
        self.current_editor.ToggleSelectedBold()

    def format_text_underline(self):
        self.current_editor.ToggleSelectedUnderline()

    def format_text_italics(self):
        self.current_editor.ToggleSelectedItalics()
        
    def format_text_font(self, newFont):
        self.current_editor.OnFontChanged(newFont)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
