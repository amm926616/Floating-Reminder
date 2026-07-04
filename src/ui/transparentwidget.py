import json

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QFontDatabase, QGuiApplication, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
                               QPushButton, QSystemTrayIcon, QVBoxLayout,
                               QWidget)

from src.const import CONFIGS, ICON_PATH, load_config, CONFIG_FILE, FONT_FILE, ALARM_FILE
from src.ui.configwindow import ConfigWindow
from src.ui.traymenu import TrayMenuCustom


class TransparentWidget(QWidget):
    def __init__(self, text, desktop_app_file):
        super().__init__()

        self.config_window = None
        self.font_color = CONFIGS.get("font_color", [255, 0, 0])
        self.transparency = CONFIGS.get("transparency", 150)
        self.padding = CONFIGS.get(
            "padding", 10
        )  # Define padding value, 10 pixels as default

        QGuiApplication.setDesktopFileName(desktop_app_file)

        self.custom_font = self.load_custom_font()
        self.label = QLabel(text, self)
        # Apply padding to the QLabel using stylesheet
        self.label.setStyleSheet(
            f"color: rgba({self.font_color[0]}, {self.font_color[1]}, {self.font_color[2]}, {self.transparency}); "
            f"background: transparent; padding: {self.padding}px;"  # Added padding here
        )
        self.label.setFont(self.custom_font)
        self.label.setWordWrap(True)
        # --- MODIFICATION START ---
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )
        # --- MODIFICATION END ---

        self.position_text(text)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.adjustSize()
        # --- MODIFICATION START ---
        # Move the window to the bottom-right corner with padding
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.width() - self.padding,
            screen.height() - self.height() - self.padding,
        )
        # --- MODIFICATION END ---

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        print(ICON_PATH)
        self.tray_icon = QSystemTrayIcon(QIcon(ICON_PATH), self)
        self.tray_menu = TrayMenuCustom(
            self.tray_icon,
            self.update_text,
            self.quit_app,
            self.open_config_window,
            self.play_sound,
        )

    def play_sound(self):
        try:
            self.player.setSource(QUrl.fromLocalFile(ALARM_FILE))
            self.player.play()
            self.update_text()

        except FileNotFoundError:
            print("Sound file not found.")

    def show_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()

    def update_text(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Reminder Text")
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        btn = QPushButton("OK")
        layout.addWidget(btn)

        btn.clicked.connect(dialog.accept)

        if dialog.exec():
            new_text = input_field.text()
            if new_text.strip():
                self.position_text(new_text)
                self.save_text(new_text)

    def save_text(self, new_text):
        """Save the new text to the configuration file."""
        try:
            config, _ = load_config()
            config["reminder_text"] = new_text
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
        except IOError as e:
            print(f"Error saving reminder text: {e}")

    def position_text(self, new_text):
        self.label.setText(new_text.strip())
        self.label.adjustSize()
        self.adjustSize()
        # --- MODIFICATION START ---
        # Recalculate position for bottom-right when text is updated
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.width() - self.padding,
            screen.height() - self.height() - self.padding,
        )
        # --- MODIFICATION END ---

    def load_custom_font(self):
        font_id = QFontDatabase.addApplicationFont(FONT_FILE)
        if font_id == -1:
            print("Custom font not found, using default font.")
            return QFont("Arial", 24)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return QFont(font_family, 24)

    def open_config_window(self):
        self.config_window = ConfigWindow(
            self.font_color, self.transparency, self.apply_config_changes
        )
        self.config_window.show()

    def apply_config_changes(self, font_color, transparency):
        self.font_color = font_color
        self.transparency = transparency
        # Reapply stylesheet with potentially new padding (if you add padding to config)
        self.label.setStyleSheet(
            f"color: rgba({self.font_color[0]}, {self.font_color[1]}, {self.font_color[2]}, {self.transparency}); "
            f"background: transparent; padding: {self.padding}px;"  # Ensure padding is applied here too
        )
        self.save_config()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def save_config(self):
        config, _ = load_config()

        config["font_color"] = self.font_color
        config["transparency"] = self.transparency
        config["padding"] = self.padding

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)


