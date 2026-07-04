from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QColorDialog, QDialog, QLabel,
                               QPushButton, QSlider, QVBoxLayout)


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
