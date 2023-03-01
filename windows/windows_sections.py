from PyQt6 import QtWidgets
from ui.sections import Ui_WindowSections
import windows.windows_authorization

class WindowSections(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowSections()
        self.ui.setupUi(self)
        self.ui.btn_exit.clicked.connect(self.logout)
        self.ui.btn_bakery.clicked.connect(self.bakeryOpen)

    # Обработка логаута
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
    def bakeryOpen(self):
        pass
        # self.close()
        # global WindowBakery
        # WindowBakery = Windows.WindowsBakery.WindowBakery()
        # WindowBakery.show()