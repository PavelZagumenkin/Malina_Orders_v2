from PyQt6.QtCore import QObject, pyqtSignal

class Signals(QObject):
    login_success_signal = pyqtSignal()
    login_failed_signal = pyqtSignal(str)
    register_success_signal = pyqtSignal(str)
    register_failed_signal = pyqtSignal(str)
    error_DB_signal = pyqtSignal(str)