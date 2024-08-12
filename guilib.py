from PyQt6.QtCore import *  # temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from historycontroller import *
from usersettingsprofile import UserSettingsProfile
from encodedtypes import ENCODING_TYPE, EncodeType


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


class ColourButtonWidget(QFrame):
    colour_signal = pyqtSignal(str, tuple)
    def __init__(self, value_type, rgb: tuple):
        if not rgb:
            rgb = (0, 0, 0)
            # show black as the colour to indicate no data
            # user can still select (0,0,0) to force black
            # as the selected colour - black is not the default
            # but a placeholder
        super().__init__()
        self.setAutoFillBackground(True)
        self.colour_dialog = QColorDialog()
        self.value_type = value_type
        self.new_palette = QPalette()
        self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(*rgb))
        self.setPalette(self.new_palette)

    def set_colour(self, rgb: tuple):
        if not rgb:
            self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(0,0,0))
        else:
            self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(*rgb))
        self.setPalette(self.new_palette)
        self.colour_signal.emit(self.value_type, rgb if rgb is not None else tuple())

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
    def __init__(self, user_settings_profile: UserSettingsProfile):
        super().__init__()

        self.setWindowTitle("Settings")

        # self.frame = QFrame(self)
        self.user_settings_profile = user_settings_profile
        self.form_layout = QFormLayout(self)
        self.form_layout.setSpacing(10)

        print(self.user_settings_profile)
        for val, key in enumerate(self.user_settings_profile):
            # if key in
            if key in ENCODING_TYPE:
                match ENCODING_TYPE[key]:
                    case EncodeType.HEX:
                        self.form_layout.addRow(
                            key,
                            new_widget := ColourButtonWidget(
                                key, self.user_settings_profile[key]
                            ),
                        )
                        new_widget.colour_signal.connect(self.update_settings_profile)

        # self.form_layout.addRow("Colour", ColourButtonWidget(user_settings_profile))
        # self.form_layout.addRow("Colou2r", ColourButtonWidget(user_settings_profile))

        self.setLayout(self.form_layout)

    #@pyqtSlot(str, tuple)
    def update_settings_profile(self,value_key, value):
        #print(value_key, value)
        if type(value) == tuple:
            if len(value) == 0:
                value = None
                # empty tuple is not allowed, set to None
        
        self.user_settings_profile[value_key] = value
        #print(self.user_settings_profile)
        #print(type(self.user_settings_profile))
        
        self.settings_changed_signal.emit(self.user_settings_profile)
        
        


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
