from PyQt6 import QtWidgets, QtGui
from ui.sections import Ui_WindowSections
from session.ActiveSession import Session
import windows.windows_authorization
import windows.windows_control

class WindowSections(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowSections()
        self.ui.setupUi(self)
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        role = self.session.get_role()  # Получение роли пользователя из экземпляра класса Session
        if role == 'logist':
            self.ui.btn_autoorders.setEnabled(True)
        if role == 'admin_wage':
            self.ui.btn_wage.setEnabled(True)
        elif role == 'admin':
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
        self.ui.btn_autoorders.clicked.connect(self.autoordersOpen)
        self.ui.btn_control.clicked.connect(self.controlOpen)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

    # Обработка выхода пользователя
    def logout(self):
        self.close()
        global windowLogin
        windowLogin = windows.windows_authorization.WindowAuthorization()
        windowLogin.show()
        windowLogin.ui.label_login_password.setFocus()  # Фокус по умолчанию на тексте
        windowLogin.ui.label_login_password.setStyleSheet("color: rgb(0, 0, 0)")
        windowLogin.ui.label_login_password.setText('Введите логин и пароль')
        windowLogin.ui.line_login.clear()
        windowLogin.ui.line_password.clear()


    # Закрываем выбор раздела, открываем выпечку
    def autoordersOpen(self):
        pass
        # self.close()
        # global WindowBakery
        # WindowBakery = Windows.WindowsBakery.WindowBakery()
        # WindowBakery.show()

    # Закрываем выбор раздела, открываем выпечку
    def controlOpen(self):
        self.close()
        global WindowControl
        WindowControl = windows.windows_control.WindowControl()
        WindowControl.show()