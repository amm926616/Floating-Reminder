class TrayMenuCustom:
    def __init__(
        self, tray_icon, update_text, quit_app, open_config_window, play_sound
    ):
        self.tray_icon = tray_icon
        self.tray_menu = QMenu()

        self.finish_task_action = QAction("Finish Task")
        self.update_text_action = QAction("Update Text")
        self.quit_action = QAction("Quit")
        self.configurations_action = QAction("Configurations")

        self.finish_task_action.triggered.connect(play_sound)
        self.update_text_action.triggered.connect(update_text)
        self.quit_action.triggered.connect(quit_app)
        self.configurations_action.triggered.connect(open_config_window)

        self.tray_menu.addAction(self.finish_task_action)
        self.tray_menu.addAction(self.update_text_action)
        self.tray_menu.addAction(self.configurations_action)
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.show_window)
        self.tray_icon.show()

    def show_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.tray_icon.show()

