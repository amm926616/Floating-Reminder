import json
import os
from pathlib import Path


def load_config():
    """Load configuration and reminder text."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config, config.get("reminder_text", "Floating Reminder")
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")
        return {}, "Floating Reminder"


def get_config_path():
    """Ensure the config file's directory exists and return its path."""
    if os.name == "nt":
        config_folder = Path(os.getenv("APPDATA", "~")).expanduser()
    else:
        config_folder = Path("~/.config").expanduser()

    config_directory = config_folder / "Floating Reminder"
    config_directory.mkdir(parents=True, exist_ok=True)
    return config_directory


def get_config_file(config_folder: Path):
    """Ensure the config file exists and return its path."""
    config_file = config_folder / "config.json"
    if not config_file.exists():
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


# --- Paths and Config Initialization ---

# This file is inside src/, so .parent is src/, and .parent.parent is the project root
SRC_PATH = Path(__file__).resolve().parent
ROOT_PATH = SRC_PATH.parent

CONFIG_PATH = get_config_path()
CONFIG_FILE = CONFIG_PATH / "config.json"

# Asset tracking relative to the root folder
ASSETS_PATH = ROOT_PATH / "assets"
ICON_PATH = str(ASSETS_PATH / "resources" / "icon.png")

# Specific asset files based on your directory tree
FONT_FILE = str(ASSETS_PATH / "fonts" / "KOMIKAX_.ttf")
ALARM_FILE = str(ASSETS_PATH / "sounds" / "alarm.mp3")

# Executable entry points & helper utilities
EXE_PATH = SRC_PATH / "main.py"
DESKTOP_SCRIPT_PATH = SRC_PATH / "create_desktop_file.py"

CONFIGS, PREVIOUS_TEXT = load_config()