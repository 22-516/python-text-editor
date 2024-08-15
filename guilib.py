from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from historycontroller import *
from usersettingsprofile import UserSettingsProfile
from encodedtypes import ENCODING_TYPE, EncodeType, DEFAULT_FONT_SIZE_COLLECTION, DEFAULT_FONT_SIZE
from encodingcontroller import check_type_validity

class FileContainer(QWidget):
    def __init__(self, file_path=""):
        super().__init__()

        self.label_name = file_path

        horizontal_button_layout = QHBoxLayout()
        file_name_label = QLabel(self.label_name)

        vertical_file_button_layout = QVBoxLayout()
        vertical_file_button_frame = QFrame()

        self.open_file_button = QPushButton("Open File", self)
        # self.open_file_button.clicked.connect(self.OpenFileButton)

        self.remove_file_button = QPushButton("Remove File", self)
        self.remove_file_button.clicked.connect(self.remove_file_button_pressed)

        self.open_file_button.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding
        )
        self.remove_file_button.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding
        )
        vertical_file_button_frame.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        file_name_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        vertical_file_button_layout.addWidget(self.open_file_button)
        vertical_file_button_layout.addWidget(self.remove_file_button)
        vertical_file_button_frame.setLayout(vertical_file_button_layout)

        horizontal_button_layout.addWidget(file_name_label)
        horizontal_button_layout.addWidget(vertical_file_button_frame)

        self.setLayout(horizontal_button_layout)

    def remove_file_button_pressed(self):
        # print("clicked remove file button", self.label_name)
        remove_path_from_recent_file_list(self.label_name)
        self.setParent(None)
        # self.hide()


class HomeWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home")

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)

        # print(FetchRecentFileList())

        self.recent_tab_page = QScrollArea()
        self.recent_tab_page.setAutoFillBackground(True)
        self.recent_tab_page.setWidgetResizable(True)

        self.recent_tab_scrolling_frame = QFrame()
        self.recent_tab_scrolling_frame.setAutoFillBackground(True)

        self.recent_tab_vertical_layout = QVBoxLayout()

        """for file_path in FetchRecentFileList():
            print(file_path)
            scrollingVLayout.addWidget(FileContainer(file_path))"""

        self.recent_tab_scrolling_frame.setLayout(self.recent_tab_vertical_layout)
        self.recent_tab_page.setWidget(self.recent_tab_scrolling_frame)

        self.addTab(self.recent_tab_page, "Recent")

    def add_button(self, button: FileContainer):
        self.recent_tab_vertical_layout.addWidget(button)


# class SettingsWidget(QWidget):
#     def __init__(self, widget_name):
#         super().__init__()
#         self.vertical_layout = QVBoxLayout()
#         self.setLayout(self.vertical_layout)

#         self.title_label = QLabel()
#         self.title_label.setText(widget_name)
#         self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.vertical_layout.addWidget(self.title_label)

#         self.setLayout(self.vertical_layout)

class StringWidget(QLineEdit):
    values_changed_signal = pyqtSignal(str, str)
    def __init__(self, value_type, string_value : str):
        super().__init__()
        self.value_type = value_type
        
        self.setText(string_value)
        
        self.setPlaceholderText("Enter Text:")
        self.editingFinished.connect(self.editing_finished)
        
    def editing_finished(self):
        print(self.text())
        self.values_changed_signal.emit(self.value_type, self.text())

class HashStringWidget(StringWidget):
    def __init__(self, value_type, string_value : str):
        super().__init__(value_type, None)
        super().setEchoMode(QLineEdit.EchoMode.Password)

class StringListWidget(QWidget):
    values_changed_signal = pyqtSignal(str, list)
    def __init__(self, value_type, input_list):
        super().__init__()
        self.value_type = value_type
        #self.inital_numbers_list = []

        self.horizontal_layout = QHBoxLayout(self)

        self.list_widget = QListWidget()
        
        self.vertical_layout = QVBoxLayout()
        
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        # self.list_widget.setDragEnabled(True)
        # self.list_widget.setDropIndicatorShown(True)
        # self.list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)

        self.move_up_button = QPushButton(QIcon(os.path.join("images", "icons", "arrow-up.png")), "Move Up")
        self.move_up_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.move_down_button = QPushButton(QIcon(os.path.join("images", "icons", "arrow-down.png")), "Move Down")
        self.move_down_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.new_item_button = QPushButton(QIcon(os.path.join("images", "icons", "plus.png")), "New Item")
        self.new_item_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.remove_item_button = QPushButton(QIcon(os.path.join("images", "icons", "minus.png")), "Remove Item")
        self.remove_item_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.move_up_button.clicked.connect(self.move_list_item_up)
        self.move_down_button.clicked.connect(self.move_list_item_down)
        self.new_item_button.clicked.connect(self.add_list_item)
        self.remove_item_button.clicked.connect(self.remove_list_item)

        self.vertical_layout.addWidget(self.move_up_button)
        self.vertical_layout.addWidget(self.move_down_button)
        self.vertical_layout.addWidget(self.new_item_button)
        self.vertical_layout.addWidget(self.remove_item_button)

        self.horizontal_layout.addWidget(self.list_widget)
        self.horizontal_layout.addLayout(self.vertical_layout)

        if not input_list:
            input_list = DEFAULT_FONT_SIZE_COLLECTION
        for _, value in enumerate(input_list):
            item = QListWidgetItem()
            #self.inital_numbers_list.append(item)
            item.setText(str(value))
            self.list_widget.addItem(item)
            self.list_widget.openPersistentEditor(item)

        self.list_widget.itemChanged.connect(self.send_list_signal)

    def get_list_items_as_list(self):
        temp_list = []
        for index in range(self.list_widget.count()):
            item_widget = self.list_widget.item(index)
            font_size = item_widget.text()
            temp_list.append(font_size)
            # self.list_widget.closePersistentEditor(self.list_widget.item(index))

        print(temp_list)
        return temp_list

    def move_list_item_up(self):
        current_index = self.list_widget.currentRow()
        if current_index > 0:
            item = self.list_widget.takeItem(current_index)
            self.list_widget.insertItem(current_index - 1, item)
            self.list_widget.setCurrentRow(current_index - 1)
            self.send_list_signal()

    def move_list_item_down(self):
        current_index = self.list_widget.currentRow()
        if current_index < self.list_widget.count() - 1:
            item = self.list_widget.takeItem(current_index)
            self.list_widget.insertItem(current_index + 1, item)
            self.list_widget.setCurrentRow(current_index + 1)
            self.send_list_signal()

    def add_list_item(self):
        new_item = QListWidgetItem()
        new_item.setText(str(0))
        # self.integers.append(new_item)
        self.list_widget.addItem(new_item)
        self.list_widget.openPersistentEditor(new_item)
        self.list_widget.setCurrentItem(new_item)
        self.send_list_signal()

    def remove_list_item(self):
        current_index = self.list_widget.currentRow()
        if current_index >= 0:
            self.list_widget.takeItem(current_index)
            # self.integers.remove(current_index)
            self.send_list_signal()

    def send_list_signal(self):
        self.values_changed_signal.emit(self.value_type, self.get_list_items_as_list())

class NumberWidget(QDoubleSpinBox):
    values_changed_signal = pyqtSignal(str, float)
    def __init__(self, value_type, number_value : float):
        super().__init__()
        self.value_type = value_type
        
        if not number_value:
            number_value = DEFAULT_FONT_SIZE
        
        self.setMinimum(0)
        self.setMaximum(8192)
        self.setSingleStep(0.5)
        self.setValue(number_value)
        
        self.valueChanged.connect(self.editing_finished)
        
    def editing_finished(self):
        print(self.value())
        self.values_changed_signal.emit(self.value_type, self.value())

class FontWidget(QFontComboBox):
    values_changed_signal = pyqtSignal(str, QFont)
    def __init__(self, value_type, font : QFont):
        super().__init__()
        self.value_type = value_type
        
        self.setEditable(False)
        # set to latin for english fonts
        self.setWritingSystem(QFontDatabase.WritingSystem.Latin)
        self.currentFontChanged.connect(self.font_selected)
    
    def font_selected(self, new_font):
        self.values_changed_signal.emit(self.value_type, new_font)

class ColourButtonWidget(QFrame):
    values_changed_signal = pyqtSignal(str, tuple)
    def __init__(self, value_type, rgb_value: tuple):
        if not rgb_value:
            rgb_value = (0, 0, 0)
            # show black as the colour to indicate no data
            # user can still select (0,0,0) to force black
            # as the selected colour - black is not the default
            # but a placeholder
        super().__init__()
        self.setAutoFillBackground(True)
        self.colour_dialog = QColorDialog()
        self.value_type = value_type
        self.new_palette = QPalette()
        self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(*rgb_value))
        self.setPalette(self.new_palette)

    def set_colour(self, rgb_value: tuple):
        if not rgb_value:
            self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(0,0,0))
        else:
            self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(*rgb_value))
        self.setPalette(self.new_palette)
        self.values_changed_signal.emit(self.value_type, rgb_value if rgb_value is not None else tuple())

    # overwrite mouse press event to open colour dialog
    def mousePressEvent(self, mouse_event: QMouseEvent):
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            print("left")
            self.colour_dialog.setCurrentColor(QColor().fromRgb(*self.new_palette.color(QPalette.ColorRole.Window).getRgb()))
            self.colour_dialog.currentColorChanged.connect(lambda color: self.set_colour(color.getRgb()))
            self.colour_dialog.show()
        elif mouse_event.button() == Qt.MouseButton.RightButton:
            print("right")
            self.set_colour(None)

        # self.colour_button_clicked_signal.emit(self.new_palette, self.new_palette.color(QPalette.ColorRole.Window).getRgb())


class SettingsWindow(QWidget):
    settings_changed_signal = pyqtSignal(UserSettingsProfile)
    settings_saved_signal = pyqtSignal(UserSettingsProfile)
    settings_deleted_signal = pyqtSignal(str)
    def __init__(self, all_profiles):
        super().__init__()

        self.setWindowTitle("Settings")

        self.vertical_layout = QVBoxLayout(self)
        self.combo_box_horizontal_layout = QHBoxLayout()

        self.username_combo_box = QComboBox()
        self.username_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.username_combo_box.setEditable(True)
        self.username_combo_box.setDuplicatesEnabled(False)
        self.username_combo_box.setInsertPolicy(QComboBox.InsertPolicy.InsertAfterCurrent)
        current_profile_username = None
        # if the database contains user data
        if all_profiles:
            for current, username in all_profiles:
                # print(current, username)
                self.username_combo_box.addItem(username)
                if current:
                    current_profile_username = username
        else:
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            current_profile_username = "Default"
            self.username_combo_box.addItem(current_profile_username)
            #self.user_settings_profile["username"] = current_profile_username
        # set index to current username

        if current_profile_username:
            self.username_combo_box.setCurrentText(current_profile_username)
        else:
            self.username_combo_box.setCurrentIndex(0)

        #self.user_settings_profile = UserSettingsProfile(current_profile_username)
        self.user_settings_profile = None

        self.username_combo_box.activated.connect(self.profile_name_changed)
        self.profile_title_label = QLabel("Select a Profile:")

        self.profile_delete_button = QPushButton(QIcon(os.path.join("images", "icons", "minus.png")), "Delete Profile")
        self.profile_delete_button.clicked.connect(self.delete_profile)

        self.combo_box_horizontal_layout.addWidget(self.profile_title_label)
        self.combo_box_horizontal_layout.addWidget(self.username_combo_box)
        self.combo_box_horizontal_layout.addWidget(self.profile_delete_button)
        self.vertical_layout.addLayout(self.combo_box_horizontal_layout)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)

        self.error_message = QErrorMessage(self)

        self.vertical_layout.addLayout(self.form_layout)
        self.setLayout(self.vertical_layout)
        
        self.change_profile(current_profile_username)
        
    def change_profile(self, username):
        self.user_settings_profile = UserSettingsProfile(username)
        self.user_settings_profile["username"] = username
        self.settings_saved_signal.emit(self.user_settings_profile)
    
    def load_profile(self, username):
        self.change_profile(username)
        self.reset_settings_page()
        self.populate_form_layout()
            
    def profile_name_changed(self, row_int):
        # check if new username is valid
        success = self.update_settings_profile("username", current_username := self.username_combo_box.currentText())
        if not success:
            self.username_combo_box.removeItem(row_int)
            self.username_combo_box.setCurrentText(self.user_settings_profile["username"])
        else:
            self.load_profile(current_username)

    def delete_profile(self):
        self.settings_deleted_signal.emit(self.user_settings_profile["username"])

        self.username_combo_box.removeItem(self.username_combo_box.currentIndex())
        if self.username_combo_box.count() > 0:
            self.username_combo_box.setCurrentIndex(0)
            self.user_settings_profile = UserSettingsProfile(self.username_combo_box.currentText())
        else:
            self.user_settings_profile = UserSettingsProfile("Default")
            self.username_combo_box.addItem("Default")
            self.user_settings_profile["username"] = "Default"

        self.settings_saved_signal.emit(self.user_settings_profile)
        self.reset_settings_page()
        self.populate_form_layout()
        
    def rename_profile(self, old_name, new_name):
        if old_name == new_name:
            # unneeded renaming
            return
        
        self.username_combo_box.setCurrentText(new_name)
        
        for index in range(self.username_combo_box.count()):
            if self.username_combo_box.itemText(index) == old_name:
                self.username_combo_box.setItemText(index, new_name)
        self.username_combo_box.setCurrentText(new_name)
        # save settings to db (so when user clicks on the username in the combobox,
        # the saved settings are shown (otherwise erases progress))
        self.settings_saved_signal.emit(self.user_settings_profile)

    def reset_settings_page(self):
        for i in reversed(range(self.form_layout.count())): 
            self.form_layout.itemAt(i).widget().setParent(None)

    def populate_form_layout(self):
        #print(self.user_settings_profile)
        for _, key in enumerate(self.user_settings_profile):
            if not key in ENCODING_TYPE:
                return False
            widget_class = None
            
            match ENCODING_TYPE[key]:
                case EncodeType.HEX:
                    widget_class = ColourButtonWidget
                case EncodeType.STR:
                    widget_class = StringWidget
                case EncodeType.HASH:
                    widget_class = HashStringWidget
                case EncodeType.LIST:
                    widget_class = StringListWidget
                case EncodeType.INT:
                    widget_class = NumberWidget
                case EncodeType.FONT:
                    widget_class = FontWidget
                case _:
                    print("setting exists but does not have a widget")
                    continue
                
            self.form_layout.addRow(key,
                new_widget := widget_class(
                    key, self.user_settings_profile[key]
                ),
            )
            new_widget.values_changed_signal.connect(self.signal_update_settings)
            
            # match ENCODING_TYPE[key]:
            #     case EncodeType.HEX:
            #         self.form_layout.addRow(
            #             key,
            #             new_widget := ColourButtonWidget(
            #                 key, self.user_settings_profile[key]
            #             ),
            #         )
            #         new_widget.colour_signal.connect(self.signal_update_settings)
            #     case EncodeType.STR:
            #         self.form_layout.addRow(
            #             key,
            #             new_widget := StringWidget(
            #                 key, self.user_settings_profile[key]
            #             ),
            #         )
            #         new_widget.string_signal.connect(self.signal_update_settings)
            #     case EncodeType.HASH:
            #         self.form_layout.addRow(
            #             key,
            #             new_widget := HashStringWidget(
            #                 key, self.user_settings_profile[key]
            #             ),
            #         )
            #         new_widget.string_signal.connect(self.signal_update_settings)
            #     case EncodeType.LIST:
            #         self.form_layout.addRow(
            #             key,
            #             new_widget := StringListWidget(
            #                 key, self.user_settings_profile[key]
            #             ),
            #         )
            #         new_widget.string_signal.connect(self.signal_update_settings)
            #     case EncodeType.INT:
            #         self.form_layout.addRow(
            #             key,                        
            #             new_widget := NumberWidget(
            #                 key, self.user_settings_profile[key]
            #             ),
            #         )
            #         new_widget.number_signal.connect(self.signal_update_settings)

    def signal_update_settings(self, value_type, value):
        self.update_settings_profile(value_type, value)
        # prevents issues with crashing when updating settings (with return into a PyQt signal)
        # ( may not be the root cause, but is a good change regardless )

    def update_settings_profile(self, value_type, value):
        print(value_type, value)
        validity_state, temp_value = check_type_validity(value_type, value)
        print(validity_state, temp_value)
        if validity_state is not None:
            print(validity_state)
            self.error_message.showMessage(validity_state)
            # print("alkdkawda")
            
            # self.reset_settings_page()
            # self.populate_form_layout()
            return False

        self.user_settings_profile[value_type] = temp_value
        
        self.rename_profile(self.username_combo_box.currentText(), self.user_settings_profile["username"])
        # self.username_combo_box.setCurrentText(self.user_settings_profile["username"])
        # print(value_type, temp_value)
        # print(self.user_settings_profile)
        # print(type(self.user_settings_profile))

        self.settings_changed_signal.emit(self.user_settings_profile)
        return True

    def closeEvent(self, event):
        print("settings window closed")
        self.settings_saved_signal.emit(self.user_settings_profile)
        event.accept()

class TabCloseDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle("Confirmation")
        self.setText("Unsaved Changes")
        self.setInformativeText(
            "There are unsaved changes. Would you like to save your changes or discard them?"
        )

        self.setStandardButtons(
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel
        )
        self.setDefaultButton(QMessageBox.StandardButton.Save)
        self.setEscapeButton(QMessageBox.StandardButton.Cancel)


# def OpenFileFromHomePage():
#    def

# testing settings window
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = SettingsWindow(UserSettingsProfile("test1"))
    window.show()

    app.exec()
