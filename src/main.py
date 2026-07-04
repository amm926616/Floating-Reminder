import sys

from PySide6.QtWidgets import (QApplication)

from const import *
from create_desktop_file import create_desktop_file
from src.ui.transparentwidget import TransparentWidget


def main():
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    desktop_app_file = create_desktop_file(ICON_PATH, EXE_PATH)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    reminder = TransparentWidget(PREVIOUS_TEXT, desktop_app_file)
    reminder.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
