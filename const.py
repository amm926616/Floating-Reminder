# Paths and Config Initialization
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = get_config_path()
CONFIG_FILE = get_config_file(CONFIG_PATH)
ICON_PATH = os.path.join(SCRIPT_PATH, "icon.png")
EXE_PATH = os.path.join(SCRIPT_PATH, "main.py")
CONFIGS, PREVIOUS_TEXT = load_config()