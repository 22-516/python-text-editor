"""This file contains the main window of the editor."""

import sys
from pathlib import Path

# import re
from functools import partial
from print_color import print

from PyQt6.QtCore import QSignalBlocker
from PyQt6.QtGui import QFontDatabase, QIcon, QAction, QFont
from PyQt6.QtWidgets import (
    QMainWindow,
    QFontComboBox,
    QPushButton,
    # QStatusBar,
    QTabWidget,
    QFileDialog,
    QMenuBar,
    QToolBar,
    QMessageBox,
    QApplication,
)

from guicontroller import *  # FileContainer, TabCloseDialog
from texteditor import *
from historycontroller import *
from filescontroller import *


class MainWindow(QMainWindow):
    """The main window of the text editor."""

    def __init__(self):
        super().__init__()

        # initalise actions and objects
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
        self.text_bold_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-bold.png"))
        )

        self.text_underline_action = QAction("&Underline", self)
        self.text_underline_action.triggered.connect(self.format_text_underline)
        self.text_underline_action.setCheckable(True)
        self.text_underline_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-underline.png"))
        )

        self.text_italic_action = QAction("&Italic", self)
        self.text_italic_action.triggered.connect(self.format_text_italics)
        self.text_italic_action.setCheckable(True)
        self.text_italic_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-italic.png"))
        )
        # objects
        self.font_combo_box_widget = QFontComboBox(self)
        self.font_combo_box_widget.setEditable(False)
        self.font_combo_box_widget.currentFontChanged.connect(self.format_text_font)
        # set to latin for inital testing with english fonts
        self.font_combo_box_widget.setWritingSystem(QFontDatabase.WritingSystem.Latin)

        # initalise tabs
        # print("initalising tabs", tag="init", tag_color="magenta", color="white")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabsClosable(True)

        new_tab_button = QPushButton(self)  # the plus button
        new_tab_button.setText("+")
        self.tabs.setCornerWidget(new_tab_button)

        new_tab_button.clicked.connect(self.new_page_button_pressed)
        self.tabs.currentChanged.connect(self.on_tab_change)
        self.tabs.tabCloseRequested.connect(self.request_tab_close)

        # initalise menubar
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.menubar.addAction(self.home_page_action)

        file_menu_button = self.menubar.addMenu("File")
        file_menu_button.addAction(self.save_file_action)
        file_menu_button.addAction(self.save_as_file_action)
        file_menu_button.addAction(self.open_file_action)

        # initalise toolbar
        self.toolbar = QToolBar("main toolbar", self)
        # self.toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.insert_image_action)  # for image testing
        self.toolbar.addAction(self.text_bold_action)
        self.toolbar.addAction(self.text_underline_action)
        self.toolbar.addAction(self.text_italic_action)
        self.toolbar.addWidget(self.font_combo_box_widget)

        # initalise editor
        self.current_editor = None
        self.home_window = None

        create_file_directories()
        self.setWindowTitle("Editor")
        # self.setGeometry(0, 0, 800, 600)
        self.add_editor_page()

        # self.status_bar = QStatusBar()
        # self.setStatusBar(self.status_bar)
        # self.status_bar.showMessage("Ready", 5000)

    # methods
    #       editor functionality

    def add_editor_page(self, file_path=""):
        print(
            "adding new page with path metadata:",
            str(file_path) or "None",
            tag="editor",
            tag_color="green",
            color="white",
        )
        self.current_editor = TextEditor(file_path)
        self.tabs.addTab(self.current_editor, self.current_editor.file_name)
        self.tabs.setCurrentWidget(self.current_editor)

        self.current_editor.currentCharFormatChanged.connect(
            self.on_editor_selection_change
        )
        self.current_editor.document().modificationChanged.connect(self.update_tab_name)

    def open_file(self, selected_file=""):
        print(
            "attempting to open from file", tag="info", tag_color="blue", color="white"
        )
        selected_file_extension = ".txt"

        if not selected_file:
            supported_file_filter = "Text File (*.txt);;Word Document (*.docx)"
            selected_file, selected_filter = QFileDialog.getOpenFileName(
                self, "Open File", "", supported_file_filter
            )

        selected_file_extension = os.path.splitext(selected_file)[1]

        for tab in range(self.tabs.count()):
            if selected_file == self.tabs.widget(tab).file_path:
                prepend_recent_file_list(selected_file)
                print(
                    "file with path",
                    selected_file,
                    "already open in editor, switching tabs" or "None",
                    tag="editor",
                    tag_color="green",
                    color="white",
                )
                self.tabs.setCurrentIndex(tab)
                return

        file_content = file_controller_open_file(selected_file, selected_file_extension)
        if file_content:
            self.add_editor_page(selected_file)
            self.current_editor.setText(file_content)
            self.current_editor.document().setModified(False)
            # self.current_editor.set_file_path(selected_file)
            prepend_recent_file_list(selected_file)
        else:
            print(
                "opened file does not exist or no content",
                tag="info",
                tag_color="blue",
                color="white",
            )

    def save_file(self, save_as=False):
        print(
            "attempting to save to file, new file? :",
            save_as,
            tag="info",
            tag_color="blue",
            color="white",
        )

        selected_save_file_path = self.current_editor.file_path
        selected_file_extension = self.current_editor.file_extension

        if not selected_save_file_path or save_as:
            supported_file_filter = "Text File (*.txt);;Word Document (*.docx)"
            selected_save_file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", supported_file_filter
            )
            # grab extension from file path 
            # so that the user can enter any extension without selecting the specific filter
            selected_file_extension = Path(selected_save_file_path).suffix
            # if (
            #     selected_save_file_path # if file path is not empty
            #     # and file extension does not match
            #     and Path(selected_save_file_path).suffix != selected_file_extension 
            # ):
            #     # add extension to file path if it does not exist
            #     selected_save_file_path += selected_file_extension
            #     selected_save_file_path.strip()
            #     print(selected_save_file_path, tag="info", tag_color="blue", color="white")

        if file_controller_save_file(
            self.current_editor, selected_save_file_path, selected_file_extension
        ):
            self.current_editor.set_file_path(selected_save_file_path)
            self.current_editor.document().setModified(False)
            prepend_recent_file_list(selected_save_file_path)
            # self.update_tab_name() # prompt name change so it instantly updates the tab name
            print(
                "file saved to",
                selected_save_file_path,
                tag="editor",
                tag_color="green",
                color="white",
            )
            return True
        else:
            print("file not saved", tag="editor", tag_color="green", color="white")
            return False

    def update_tab_name(self, new_modification_status):
        if not new_modification_status:
            new_modification_status = self.current_editor.document().isModified()
        self.tabs.setTabText(
            self.tabs.currentIndex(),
            (
                (self.current_editor.file_name + "*")
                if new_modification_status
                else self.current_editor.file_name
            ),
        )

    #   signals
    def on_editor_selection_change(
        self,
    ):  # when the cursor selection is changed (eg if the user clicks on bolded text)
        # check all qactions for continuity
        if (
            self.current_editor
        ):  # if the editor exists (prevents issues when tab is closed)
            self.text_bold_action.setChecked(
                True
                if not self.current_editor.fontWeight() == QFont.Weight.Normal
                else False
            )
            self.text_underline_action.setChecked(
                True if self.current_editor.fontUnderline() else False
            )
            self.text_italic_action.setChecked(
                True if self.current_editor.fontItalic() else False
            )
            with QSignalBlocker(
                self.font_combo_box_widget
            ):  # block font combobox signal to prevent loop where upon selection change,
                # the font combobox changes font which changes font of selected text
                self.font_combo_box_widget.setCurrentFont(
                    self.current_editor.currentFont()
                )

    def on_tab_change(self):
        self.current_editor = self.tabs.currentWidget()
        self.on_editor_selection_change()  # update text formatting qactions checked status upon
        # changing tabs to preserve continuity between tabs
        print(
            "tab changed to",
            self.current_editor,
            tag="editor",
            tag_color="green",
            color="white",
        )

    def request_tab_close(self, tab_index):
        self.tabs.setCurrentIndex(tab_index)
        print(
            "prompting close ",
            self.current_editor,
            tag="editor",
            tag_color="green",
            color="yellow",
        )

        if (
            self.current_editor.document().isModified()
        ):  # only prompt user if the document is modiifed
            close_tab_dialog_answer = TabCloseDialog().exec()
            match close_tab_dialog_answer:
                case QMessageBox.StandardButton.Save:
                    print("save", tag="info", tag_color="blue", color="white")
                    if not self.save_file():
                        return False
                case QMessageBox.StandardButton.Discard:
                    print("discard", tag="info", tag_color="blue", color="white")
                case QMessageBox.StandardButton.Cancel:
                    print("cancel", tag="info", tag_color="blue", color="white")
                    return False
                case _:
                    print("data not saved", tag="info", tag_color="blue", color="white")
                    return False

        self.tabs.removeTab(tab_index)  # close tab
        if self.tabs.count() <= 0:  # ensure always one editor page available
            self.add_editor_page()
        return True

    def closeEvent(self, event):
        """override the QMainWindow close event to ensure tabs are saved or discarded on exit"""
        for tab_index in range(0, self.tabs.count()):
            if not self.request_tab_close(
                tab_index
            ):  # if a tab is not saved or discarded, and the cancel button is pressed instead
                event.ignore()
                return
        event.accept()

    #   actions
    def new_page_button_pressed(self):
        print("new page prompted", tag="editor", tag_color="green", color="white")
        self.add_editor_page()

    def insert_image_button_pressed(self):
        print(
            "inserting test image",
            self.current_editor,
            tag="editor",
            tag_color="green",
            color="white",
        )
        self.current_editor.InsertImage()

    def open_home_page(self):
        self.home_window = HomeWindow()

        for file_path in fetch_recent_file_list():
            print(file_path)
            self.home_window.AddButton(temp_container := FileContainer(file_path))
            temp_container.open_file_button.clicked.connect(
                partial(self.open_file, temp_container.label_name)
            )  # so the buttons have functionality

        self.home_window.show()

    # text formatting actions
    def format_text_bold(self):
        self.current_editor.toggle_selected_bold()

    def format_text_underline(self):
        self.current_editor.toggle_selected_underline()

    def format_text_italics(self):
        self.current_editor.toggle_selected_italics()

    def format_text_font(self, new_font):
        self.current_editor.setFocus()
        self.current_editor.change_font(new_font)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
