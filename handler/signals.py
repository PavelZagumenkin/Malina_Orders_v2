from PyQt6.QtCore import pyqtSignal

class Signals:
    login_success_signal = pyqtSignal(str)
    login_failed_signal = pyqtSignal(str)
    register_success_signal = pyqtSignal(str)
    register_failed_signal = pyqtSignal(str)
