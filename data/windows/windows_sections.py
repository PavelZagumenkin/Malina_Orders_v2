from PyQt6 import QtWidgets, QtGui
from data.ui.sections import Ui_WindowSections
from data.active_session import Session
import data.windows.windows_authorization
import data.windows.windows_control
import data.windows.windows_autoOrders
from data.requests.db_requests import Database
from data.signals import Signals
import datetime


class WindowSections(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowSections()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        role = self.session.get_role()  # Получение роли пользователя из экземпляра класса Session
        if role == 'operator':
            self.ui.btn_autoorders.setEnabled(True)
        elif role == 'logist':
            self.ui.btn_autoorders.setEnabled(True)
        elif role == 'supervisor':
            self.ui.btn_wage.setEnabled(True)
        elif role == 'manager':
            self.ui.btn_autoorders.setEnabled(True)
            self.ui.btn_wage.setEnabled(True)
            self.ui.btn_comingsoon.setEnabled(True)
            self.ui.btn_history.setEnabled(True)
        elif role == 'superadmin':
            self.ui.btn_autoorders.setEnabled(True)
            self.ui.btn_wage.setEnabled(True)
            self.ui.btn_comingsoon.setEnabled(True)
            self.ui.btn_history.setEnabled(True)
            self.ui.btn_control.setEnabled(True)
        self.ui.btn_exit.clicked.connect(self.logout)
        self.ui.btn_autoorders.clicked.connect(self.show_autoorders)
        self.ui.btn_control.clicked.connect(self.show_control)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

    # Обработка выхода пользователя
    def logout(self):
        username = self.session.get_username()  # Получение имени пользователя из экземпляра класса Session
        logs_result = self.database.add_log(datetime.datetime.now().date(), datetime.datetime.now().time(),
                                            f"Пользователь {username} вышел из системы.")
        if "Лог записан" in logs_result:
            self.signals.login_success_signal.emit()
        elif 'Ошибка работы' in logs_result:
            self.signals.error_DB_signal.emit(logs_result)
        else:
            self.signals.login_failed_signal.emit(logs_result)
        self.close()
        global windowLogin
        windowLogin = data.windows.windows_authorization.WindowAuthorization()
        windowLogin.show()
        windowLogin.ui.label_login_password.setFocus()  # Фокус по умолчанию на тексте
        windowLogin.ui.label_login_password.setStyleSheet("color: rgb(0, 0, 0)")
        windowLogin.ui.label_login_password.setText('Введите логин и пароль')
        windowLogin.ui.line_login.clear()
        windowLogin.ui.line_password.clear()

    # Закрываем выбор раздела, открываем выпечку
    def show_autoorders(self):
        self.close()
        global WindowAutoOrders
        WindowAutoOrders = data.windows.windows_autoOrders.WindowAutoOrders()
        WindowAutoOrders.show()

    # Закрываем выбор раздела, открываем выпечку
    def show_control(self):
        self.close()
        global WindowControl
        WindowControl = data.windows.windows_control.WindowControl()
        WindowControl.show()
