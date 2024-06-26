from src.logger import get_logger

log = get_logger()

import multiprocessing as mp

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from src.gui.bot_counters_window.bot_counters_window import BotCountersWindow
from src.gui.bot_logs_window.bot_logs_window import BotLogsWindow
from src.gui.main_window.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.setWindowTitle("Sadidauto")
        self.setFocus()
        self.setFocusPolicy(Qt.ClickFocus) # Make all widgets lose focus when clicking on the main window.
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint) # Set non resizable.
        self.bot_counters_window = BotCountersWindow()
        self.bot_logs_window = BotLogsWindow()
        self._connect_signals_and_slots()

    def _connect_signals_and_slots(self):
        # Start button.
        self.start_button.bot_started_signal.connect(self.stop_button.on_bot_started)
        self.start_button.bot_started_signal.connect(self.bot_logs_window.on_bot_started)
        self.start_button.bot_started_signal.connect(self.status_label.on_bot_started)
        self.start_button.bot_started_signal.connect(
            self.bot_counters_window.bot_counters_plain_text_edit.on_bot_started
        )
        self.start_button.bot_exited_due_to_exception_signal.connect(
            self.stop_button.on_bot_exited_due_to_exception
        )
        self.start_button.initialization_options_invalid_signal.connect(
            self.status_label.on_initialization_options_invalid
        ) 
        self.start_button.bot_stopped_signal.connect(self.status_label.on_bot_stopped)
        # Stop button.
        self.stop_button.bot_stopped_signal.connect(self.start_button.on_bot_stopped)
        # Bot logs window.
        self.bot_logs_window.log_file_line_read.connect(
            self.bot_counters_window.bot_counters_plain_text_edit.on_log_file_line_read
        )

    def closeEvent(self, _):
        log.info("Main window closed! Exiting ... ")
        for child_process in mp.active_children():
            child_process.terminate()

        self.bot_counters_window.fully_close_on_close_event = True
        self.bot_logs_window.fully_close_on_close_event = True
        for window in QApplication.topLevelWidgets():
            window.close()
