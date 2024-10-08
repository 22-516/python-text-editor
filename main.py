"""This file contains the main window of the editor."""

import builtins
import sys
from pathlib import Path

import re
from functools import partial
from print_color import print

from PyQt6.QtCore import QSignalBlocker
from PyQt6.QtGui import QFontDatabase, QIcon, QAction, QKeySequence
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
    QComboBox,
)

from guilib import *  # FileContainer, TabCloseDialog
from encodedtypes import *
from encodingcontroller import tuple_rgb_to_hex
from texteditor import *
from historycontroller import *
from filescontroller import *
from profilesmanager import *


class MainWindow(QMainWindow):
    """The main window of the text editor."""

    def __init__(self):
        super().__init__()

        # initalise editor
        self.current_editor = TextEditor()
        self.home_window = None
        self.settings_window = None

        # load the user settings from the current profile
        self.user_settings_profile = get_current_user_profile()

        # initalise actions and objects
        self.new_page_action = QAction("&New Page", self)
        self.new_page_action.triggered.connect(self.new_page_button_pressed)

        self.open_file_action = QAction("&Open", self)
        self.open_file_action.triggered.connect(self.open_file)
        self.open_file_action.setShortcut(QKeySequence("Ctrl+O"))

        self.save_file_action = QAction("&Save", self)
        self.save_file_action.triggered.connect(self.save_file)
        self.save_file_action.setShortcut(QKeySequence("Ctrl+S"))

        self.save_as_file_action = QAction("&Save As", self)
        self.save_as_file_action.triggered.connect(partial(self.save_file, True))
        self.save_as_file_action.setShortcut(QKeySequence("Ctrl+Shift+S"))

        self.home_page_action = QAction("&Home", self)
        self.home_page_action.triggered.connect(self.open_home_page)

        self.settings_action = QAction("&Settings", self)
        self.settings_action.triggered.connect(self.open_settings_page)

        self.insert_image_action = QAction("&Insert Image", self)
        self.insert_image_action.triggered.connect(self.insert_image_button_pressed)

        # text formatting actions
        self.text_bold_action = QAction("&Bold", self)
        self.text_bold_action.triggered.connect(self.format_text_bold)
        self.text_bold_action.setCheckable(True)
        self.text_bold_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-bold.png"))
        )
        self.text_bold_action.setShortcut(QKeySequence("Ctrl+B"))

        self.text_underline_action = QAction("&Underline", self)
        self.text_underline_action.triggered.connect(self.format_text_underline)
        self.text_underline_action.setCheckable(True)
        self.text_underline_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-underline.png"))
        )
        self.text_underline_action.setShortcut(QKeySequence("Ctrl+U"))

        self.text_italic_action = QAction("&Italic", self)
        self.text_italic_action.triggered.connect(self.format_text_italics)
        self.text_italic_action.setCheckable(True)
        self.text_italic_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-italic.png"))
        )
        self.text_italic_action.setShortcut(QKeySequence("Ctrl+I"))

        self.font_size_increase_action = QAction(
            "&+", self
        )  # the small buttons on the side of the font size widget
        # to increment or decrement the font size in small amounts easily
        self.font_size_increase_action.triggered.connect(self.increase_font_size)
        self.font_size_increase_action.setCheckable(False)
        self.font_size_increase_action.setText("+")

        self.font_size_decrease_action = QAction("&-", self)
        self.font_size_decrease_action.triggered.connect(self.decrease_font_size)
        self.font_size_decrease_action.setCheckable(False)
        self.font_size_decrease_action.setText("-")

        self.text_colour_change_action = QAction("&Text Colour", self)
        self.text_colour_change_action.setCheckable(False)
        self.text_colour_change_action.triggered.connect(self.format_text_colour)
        self.text_colour_change_action.setIcon(
            QIcon(os.path.join("images", "icons", "edit-color.png"))
        )

        self.text_colour_selection_action = QAction("&Text Colour Selection", self)
        self.text_colour_selection_action.setCheckable(False)
        self.text_colour_selection_action.triggered.connect(self.change_text_colour)
        self.text_colour_selection_action.setIcon(
            QIcon(os.path.join("images", "icons", "color.png"))
        )

        self.highlight_colour_change_action = QAction("&Highlight Colour", self)
        self.highlight_colour_change_action.setCheckable(False)
        self.highlight_colour_change_action.triggered.connect(
            self.format_highlight_colour
        )
        self.highlight_colour_change_action.setIcon(
            QIcon(os.path.join("images", "icons", "highlighter-color.png"))
        )

        self.highlight_colour_selection_action = QAction(
            "&Highlight Colour Selection", self
        )
        self.highlight_colour_selection_action.setCheckable(False)
        self.highlight_colour_selection_action.triggered.connect(
            self.change_highlight_colour
        )
        self.highlight_colour_selection_action.setIcon(
            QIcon(os.path.join("images", "icons", "color.png"))
        )

        # objects
        self.font_combo_box_widget = QFontComboBox(self)
        self.font_combo_box_widget.setEditable(False)
        self.font_combo_box_widget.currentFontChanged.connect(self.format_text_font)
        # set to latin for inital testing with english fonts
        self.font_combo_box_widget.setWritingSystem(QFontDatabase.WritingSystem.Latin)

        self.font_size_combo_box_widget = QComboBox(self)
        self.font_size_combo_box_widget.setEditable(True)
        self.font_size_combo_box_widget.setDuplicatesEnabled(False)
        self.font_size_combo_box_widget.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.font_size_combo_box_widget.textActivated.connect(
            self.format_text_font_size
        )

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
        self.menubar.addAction(self.settings_action)

        file_menu_button = self.menubar.addMenu("File")
        file_menu_button.addAction(self.save_file_action)
        file_menu_button.addAction(self.save_as_file_action)
        file_menu_button.addAction(self.open_file_action)

        insert_menu_button = self.menubar.addMenu("Insert")
        insert_menu_button.addAction(self.insert_image_action)

        # initalise toolbar
        self.toolbar = QToolBar("main toolbar", self)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.insert_image_action)
        self.toolbar.addAction(self.text_bold_action)
        self.toolbar.addAction(self.text_underline_action)
        self.toolbar.addAction(self.text_italic_action)
        self.toolbar.addWidget(self.font_combo_box_widget)
        self.toolbar.addWidget(self.font_size_combo_box_widget)
        self.toolbar.addAction(self.font_size_increase_action)
        self.toolbar.addAction(self.font_size_decrease_action)
        self.toolbar.addAction(self.text_colour_change_action)
        self.toolbar.addAction(self.text_colour_selection_action)
        self.toolbar.addAction(self.highlight_colour_change_action)
        self.toolbar.addAction(self.highlight_colour_selection_action)

        # personalisation
        self.default_editor_palette = self.current_editor.palette()
        self.text_colour = QColor()
        self.text_colour_dialog = None
        self.highlight_colour = QColor().fromRgb(255, 255, 0) # yellow
        self.highlight_colour_dialog = None

        create_file_directories()
        self.setWindowTitle("Editor")
        self.add_editor_page()
        self.update_editor_from_settings()

    # methods
    #       editor functionality

    def add_editor_page(self, file_path=""):
        """adds a new editor into a new tab"""
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

        # add a connection to currentCharFormatChanged to detect when the user selected text
        # formatting changes, to update QAction checked status (bold button, underline, etc)
        self.current_editor.currentCharFormatChanged.connect(
            self.on_editor_selection_change
        )

    def open_file(self, selected_file=""):
        """attempts to a file of the users choice into the editor"""
        print(
            "attempting to open from file", tag="info", tag_color="blue", color="white"
        )
        selected_file_extension = ".txt"

        if not selected_file:
            supported_file_filter = "Text File (*.txt);;Word Document (*.docx)"
            selected_file, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", supported_file_filter
            )

        selected_file_extension = os.path.splitext(selected_file)[1]

        # check if the file is already open in the editor
        for tab in range(self.tabs.count()):
            if selected_file == self.tabs.widget(tab).file_path:
                # count it as opening the file, so add to history
                prepend_recent_file_list(selected_file)
                print(
                    "file with path",
                    selected_file,
                    "already open in editor, switching tabs" or "None",
                    tag="editor",
                    tag_color="green",
                    color="white",
                )
                # then swap tabs to the file
                self.tabs.setCurrentIndex(tab)
                return

        file_content = file_controller_open_file(selected_file, selected_file_extension)

        try:
            match type(file_content):
                case builtins.str:
                    # if the returned file_content is string, set immediately
                    self.add_editor_page(selected_file)
                    # print(file_content)
                    self.current_editor.setText(file_content)
                case builtins.list:
                    self.add_editor_page(selected_file)
                    self.current_editor.setText("")
                    new_cursor = self.current_editor.textCursor()
                    for format_list in file_content:
                        # print(format_list)
                        if isinstance(format_list, str):
                            # the formatted item is a string (which is an encoded image in this context)
                            new_cursor.insertHtml(format_list)
                        else:
                            # stored as a tuple with the text and the text formatting as two different indexes
                            new_cursor.insertText(str(format_list[0]), format_list[1])
        except Exception as exception:
            print("error occured during opening file", exception)
        else:
            # we set the metadata again just to be double sure
            self.current_editor.document().setModified(False)
            self.current_editor.set_file_path(selected_file)
            # prepend to history so the user can see the file from the home window
            prepend_recent_file_list(selected_file)

    def save_file(self, save_as=False):
        """attempts to save the current editor to a file of the users choice"""
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
            # file filter so that only text files and word documents are shown within the file dialog
            # ( to discourage the user from picking an unrelated file type )
            supported_file_filter = "Text File (*.txt);;Word Document (*.docx)"
            selected_save_file_path, selected_filter = QFileDialog.getSaveFileName(
                self, "Save File", "", supported_file_filter
            )
            # grab extension from file path
            # so that the user can enter any extension without selecting the specific filter
            if (
                selected_save_file_path  # if file path is not empty
                # and if file extension does not match (or not exist)
                and not selected_file_extension
            ):
                # add extension to file path if it does not exist
                # use regex to capture between the brackets in the filter to get current file type
                # (this is why filters are separated, for ease of use for user when they input a file name)
                selected_file_extension = (
                    re.search(r"\((.+?)\)", selected_filter or supported_file_filter)
                    .group(1)
                    .replace("*", "")
                )
                selected_save_file_path += selected_file_extension
                selected_save_file_path.strip()
                print(
                    selected_save_file_path, tag="info", tag_color="blue", color="white"
                )

        if file_controller_save_file(
            self.current_editor, selected_save_file_path, selected_file_extension
        ):
            self.current_editor.set_file_path(selected_save_file_path)
            self.current_editor.document().setModified(False)
            prepend_recent_file_list(selected_save_file_path)
            # prompt name change so it instantly updates the tab name
            # with the new file name (fixes issue where tab name does not update
            # if modification state is same)
            # such as if file is not edited before saving
            self.update_current_tab_name()
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

    def update_current_tab_name(self, new_modification_status=None):
        """this method is called whenever the current_editor.document().isModified() changes
        so when the user types something in, etc, change tab name to reflect"""
        if not new_modification_status:
            new_modification_status = self.current_editor.document().isModified()
        self.tabs.setTabText(
            self.tabs.currentIndex(),
            (
                (self.current_editor.file_name + "*")
                if new_modification_status  # if file is modified, add asterisk to tab name
                else self.current_editor.file_name
            ),
        )

    def update_editor_from_settings(self):
        """update the editor with all the settings from the currently selected user profile"""
        temp_window_colour_string = self.user_settings_profile[
            "editor_background_colour"
        ]
        if temp_window_colour_string:
            # editor colour within the UserSettingsProfile class is saved as a tuple with rgb values
            # so we need to convert into a hex to use in the stylesheet (only accepts hex)
            temp_window_colour = tuple_rgb_to_hex(*temp_window_colour_string)

            self.setStyleSheet(
                f"""
                                * {{
                                    background-color: '{temp_window_colour}';
                                }};
                            """
            )
        else:
            # this sets to the default stylesheet if there's no user selected colour
            self.setStyleSheet("")

        # update editor colour [editor_color]
        temp_editor_colour_string = self.user_settings_profile["editor_colour"]
        if temp_editor_colour_string:
            # editor colour within the UserSettingsProfile class is saved as a tuple with rgb values
            # so we need to convert into a hex to use in the stylesheet (only accepts hex)
            temp_editor_colour = tuple_rgb_to_hex(*temp_editor_colour_string)

            self.current_editor.setStyleSheet(
                f"""
                                                background-color: '{temp_editor_colour}';
                                                """
            )
        else:
            # this sets to the default stylesheet if there's no user selected colour
            self.current_editor.setStyleSheet("")

        # update font size collection (the list of sizes available) [font_size_collection]
        self.font_size_combo_box_widget.clear()
        if not (font_collection := self.user_settings_profile["font_size_collection"]):
            # if there is no font_size_collection within the currently selected profile, use default
            # from constants set in encode_type
            font_collection = DEFAULT_FONT_SIZE_COLLECTION
        for index, font_size_value in enumerate(font_collection):
            self.font_size_combo_box_widget.insertItem(index, str(font_size_value))

        # update default font and font size [default_font, default_font_size]
        temp_font = self.user_settings_profile["default_font"] or QFont(
            DEFAULT_FONT_FAMILY
        )
        # PointSizeF is a float value
        temp_font.setPointSizeF(
            self.user_settings_profile["default_font_size"] or DEFAULT_FONT_SIZE
        )
        self.current_editor.document().setDefaultFont(temp_font)

        # prompt editor to show new formatting changes
        self.on_editor_selection_change()

    #   signals
    def on_editor_selection_change(
        self,
    ):
        """when the cursor selection is changed (eg if the user clicks on bolded text)
        check all qactions for continuity"""
        if (
            self.current_editor
        ):  # if the editor exists (prevents issues when tab is closed)
            self.text_bold_action.setChecked(self.current_editor.font_bold())
            self.text_underline_action.setChecked(self.current_editor.fontUnderline())
            self.text_italic_action.setChecked(self.current_editor.fontItalic())

            with QSignalBlocker(self.font_combo_box_widget):
                # block font combobox signal to prevent loop where upon selection change,
                # the font combobox changes font which changes font of selected text
                self.font_combo_box_widget.setCurrentFont(
                    self.current_editor.currentFont()
                )

            with QSignalBlocker(self.font_size_combo_box_widget):
                # just to be safe
                self.font_size_combo_box_widget.setCurrentText(
                    self.current_editor.font_size()
                )

    def on_tab_change(self):
        """when a tab changes, we set the current editor to the editor within the tab we changed to"""
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
        """when a tab is about to be closed, check for any unsaved changes before allowing the tab to be closed if the user allows it"""
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
        """override the QMainWindow class close event to ensure tabs are saved or discarded on exit"""
        for tab_index in range(0, self.tabs.count()):
            if not self.request_tab_close(
                tab_index
            ):  # if a tab is not saved or discarded, and the cancel button is pressed instead
                event.ignore()
                return
        event.accept()

    def settings_updated_slot(self, temp_settings_profile):
        """this connection is fired when the settings window profile changes, allowing the editor to update its settings in real time for a cool effect"""
        self.user_settings_profile = temp_settings_profile
        self.update_editor_from_settings()

    def save_settings_slot(self, temp_settings_profile):
        """this connection is fired when the settings window closes, and prompts the save of its settings. It is also fired when the settings window changes profiles."""
        self.user_settings_profile = temp_settings_profile
        save_settings_profile_to_db(self.user_settings_profile)
        self.update_editor_from_settings()

    #   actions
    def new_page_button_pressed(self):
        """add a new editor page"""
        print("new page prompted", tag="editor", tag_color="green", color="white")
        self.add_editor_page()

    def insert_image_button_pressed(self):
        """inserts an image by prompting the user to select an image through a file dialog"""
        supported_file_filter = "Image Files (*.jpg *.jpeg *.png)"
        selected_file, selected_filter = QFileDialog.getOpenFileName(
            self, "Open Image File", "", supported_file_filter
        )

        if not selected_file:
            return

        selected_file_extension = Path(selected_file).suffix
        if selected_file_extension not in supported_file_filter:
            return

        self.current_editor.user_insert_image(selected_file)

    def change_text_colour(self):
        """changes the saved text colour as well as any currently selected text through a dialog"""
        self.text_colour_dialog = QColorDialog()
        self.text_colour_dialog.setCurrentColor(self.text_colour)

        def set_color(colour):
            self.text_colour = QColor(colour)
            print(self.text_colour)
            self.format_text_colour()

        self.text_colour_dialog.currentColorChanged.connect(set_color)

        self.text_colour_dialog.show()

    def change_highlight_colour(self):
        """changes the saved highlight colour as well as any currently selected text through a dialog"""
        self.highlight_colour_dialog = QColorDialog()
        self.highlight_colour_dialog.setCurrentColor(self.highlight_colour)

        def set_color(colour):
            self.highlight_colour = QColor(colour)
            print(self.highlight_colour)
            self.format_highlight_colour()

        self.highlight_colour_dialog.currentColorChanged.connect(set_color)

        self.highlight_colour_dialog.show()

    def open_home_page(self):
        """opens the home page and load all recent files. Creates buttons for each recently opened file and connects their clicked call to open the file within the editor"""
        self.home_window = HomeWindow()

        confirm_history_files_exist()
        for file_path in fetch_recent_file_list():
            print(file_path)
            self.home_window.add_button(temp_container := FileContainer(file_path))
            temp_container.open_file_button.clicked.connect(
                partial(self.open_file, temp_container.label_name)
            )  # so the buttons have functionality

        self.home_window.show()

    def open_settings_page(self):
        """opens the setting page and loads all user profiles into it"""
        self.settings_window = SettingsWindow(get_current_and_username_columns())

        # self.settings_window.settings_changed_signal.connect
        self.settings_window.settings_changed_signal.connect(self.settings_updated_slot)
        self.settings_window.settings_saved_signal.connect(self.save_settings_slot)
        self.settings_window.settings_deleted_signal.connect(delete_profile)

        self.settings_window.show()

    # text formatting actions
    def format_text_bold(self):
        """for signal slot purposes, redirects the function call (chanigng text boldness) to the current editor"""
        self.current_editor.toggle_selected_bold()

    def format_text_underline(self):
        """for signal slot purposes, redirects the function call (chanigng text underline) to the current editor"""
        self.current_editor.toggle_selected_underline()

    def format_text_italics(self):
        """for signal slot purposes, redirects the function call (chanigng text italics) to the current editor"""
        self.current_editor.toggle_selected_italics()

    def format_text_font(self, new_font):
        """for signal slot purposes, redirects the function call (chanigng text font) to the current editor"""
        self.current_editor.setFocus()
        self.current_editor.change_font(new_font)

    def format_text_font_size(self, new_size):
        """for signal slot purposes, redirects the function call (chanigng font size) to the current editor"""
        self.current_editor.setFocus()
        self.current_editor.change_font_size(new_size)

    def increase_font_size(self):
        """increment the font size by 0.5"""
        temp_font_size = (
            f"{float(self.font_size_combo_box_widget.currentText()) + 0.5:g}"
        )
        self.font_size_combo_box_widget.setCurrentText(temp_font_size)
        self.format_text_font_size(temp_font_size)

    def decrease_font_size(self):
        """decrement the font size by 0.5"""
        temp_font_size = (
            f"{float(self.font_size_combo_box_widget.currentText()) - 0.5:g}"
        )
        self.font_size_combo_box_widget.setCurrentText(temp_font_size)
        self.format_text_font_size(temp_font_size)

    def format_text_colour(self):
        """for signal slot purposes, redirects the function call (chanigng text colour) to the current editor"""
        self.current_editor.change_color(self.text_colour)

    def format_highlight_colour(self):
        """for signal slot purposes, redirects the function call (highlighting text) to the current editor"""
        self.current_editor.change_highlight(self.highlight_colour)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
