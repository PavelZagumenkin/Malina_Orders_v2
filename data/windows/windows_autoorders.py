from PyQt6 import QtWidgets, QtGui
import data.windows.windows_logistics
import data.windows.windows_bakery
from data.ui.autoorders import Ui_WindowAutoOrders
from data.requests.db_requests import Database
from data.active_session import Session
from data.signals import Signals
import datetime


class WindowAutoorders(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAutoOrders()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.btn_bakery.clicked.connect(self.show_windowBakery)
        self.ui.btn_back.clicked.connect(self.show_windowLogistik)

    def show_windowBakery(self):
        self.close()
        global windowBakery
        windowBakery = data.windows.windows_bakery.WindowBakery()
        windowBakery.show()

    # Закрываем выбор раздела, открываем окно выбора раздела логистики
    def show_windowLogistik(self):
        self.close()
        global windowLogistik
        windowLogistik = data.windows.windows_logistics.WindowLogistics()
        windowLogistik.show()

    def closeEvent(self, event):
        if event.spontaneous():
            username = self.session.get_username()  # Получение имени пользователя из экземпляра класса Session
            logs_result = self.database.add_log(datetime.datetime.now().date(), datetime.datetime.now().time(),
                                            f"Пользователь {username} вышел из системы.")
            if "Лог записан" in logs_result:
                self.signals.login_success_signal.emit()
            elif 'Ошибка работы' in logs_result:
                self.signals.error_DB_signal.emit(logs_result)
            else:
                self.signals.login_failed_signal.emit(logs_result)
        event.accept()
