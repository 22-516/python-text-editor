from PyQt6.QtCore import * #temp
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from historycontroller import *
from usersettingsprofile import UserSettingsProfile

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
        
        self.open_file_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        self.remove_file_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        vertical_file_button_frame.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        file_name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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

        '''for file_path in FetchRecentFileList():
            print(file_path)
            scrollingVLayout.addWidget(FileContainer(file_path))'''

        self.recent_tab_scrolling_frame.setLayout(self.recent_tab_vertical_layout)
        self.recent_tab_page.setWidget(self.recent_tab_scrolling_frame)

        self.addTab(self.recent_tab_page, "Recent")

    def add_button(self, button : FileContainer):
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
    def __init__(self, user_settings_profile : UserSettingsProfile):
        super().__init__()
        self.setAutoFillBackground(True)
        self.new_palette = QPalette()
        self.new_palette.setColor(QPalette.ColorRole.Window, QColor().fromRgb(100,255,100))
        self.setPalette(self.new_palette)

class SettingsWindow(QWidget):
    def __init__(self, user_settings_profile : UserSettingsProfile):
        super().__init__()

        self.setWindowTitle("Settings")

        # self.frame = QFrame(self)

        self.form_layout = QFormLayout(self)        
        self.form_layout.setSpacing(10)

        print(user_settings_profile)
        for val in enumerate(user_settings_profile):
            print(val)

        # self.form_layout.addRow("Colour", ColourButtonWidget(user_settings_profile))
        # self.form_layout.addRow("Colou2r", ColourButtonWidget(user_settings_profile))

        self.setLayout(self.form_layout)


class TabCloseDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle("Confirmation")
        self.setText("Unsaved Changes")
        self.setInformativeText("There are unsaved changes. Would you like to save your changes or discard them?")

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
