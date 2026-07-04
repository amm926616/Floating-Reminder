import json
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QColorDialog, QDialog, QLabel,
                               QMenu, QPushButton, QSlider, QSystemTrayIcon,
                               QVBoxLayout)

from create_desktop_file import create_desktop_file
from transparent_widget import TransparentReminder
from const import *


def get_config_path():
    """Ensure the config file's directory exists and return its path."""
    config_folder = str(
        os.getenv("APPDATA")
        if os.name == "nt"
        else os.path.join(os.path.expanduser("~"), ".config")
    )
    config_directory = os.path.join(config_folder, "Focus-F*cker")
    os.makedirs(config_directory, exist_ok=True)
    return config_directory


def get_config_file(config_folder):
    """Ensure the config file exists and return its path."""
    config_file = os.path.join(config_folder, "config.json")
    if not os.path.exists(config_file):
        default_config = {
            "font_color": [100, 255, 255],
            "transparency": 150,
            "reminder_text": "Floating Reminder",
        }
        try:
            with open(config_file, "w") as f:
                json.dump(default_config, f)
        except IOError as e:
            print(f"Error writing to config file: {e}")
    return config_file


def load_config():
    """Load configuration and reminder text."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config, config.get("reminder_text", "Floating Reminder")
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")
        return {}, "Floating Reminder"


class ConfigWindow(QDialog):
    def __init__(
        self, current_font_color, current_transparency, apply_changes_callback
    ):
        super().__init__()
        self.setWindowTitle("Configuration")
        self.apply_changes_callback = apply_changes_callback
        self.font_color = current_font_color
        self.transparency = current_transparency

        self.color_button = QPushButton("Choose Font Color", self)
        self.color_button.clicked.connect(self.choose_color)

        self.transparency_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.transparency_slider.setRange(0, 255)
        self.transparency_slider.setValue(self.transparency)
        self.transparency_slider.setTickInterval(10)
        self.transparency_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.transparency_label = QLabel(f"Transparency: {self.transparency}", self)

        self.transparency_slider.valueChanged.connect(self.update_transparency_label)

        self.apply_button = QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.apply_changes)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.color_button)
        layout.addWidget(self.transparency_slider)
        layout.addWidget(self.transparency_label)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def update_transparency_label(self):
        self.transparency_label.setText(
            f"Transparency: {self.transparency_slider.value()}"
        )

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color.getRgb()[:3]

    def apply_changes(self):
        transparency = self.transparency_slider.value()
        self.apply_changes_callback(self.font_color, transparency)
        self.accept()


def main():
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    desktop_app_file = create_desktop_file(ICON_PATH, EXE_PATH)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    reminder = TransparentReminder(PREVIOUS_TEXT, desktop_app_file)
    reminder.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
