from PyQt6 import QtWidgets
from ui.authorization import Ui_WindowAuthorization
from handler.signals import Signals
from requests.db_requests import Database
import windows.windows_sections

class WindowAuthorization(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAuthorization()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.ui.label_login_password.setFocus()  # Фокус по умолчанию на тексте
        self.ui.btn_login.clicked.connect(self.login)
        self.ui.btn_reg.clicked.connect(self.register)

        # Подключаем слоты к сигналам
        self.signals.register_success_signal.connect(self.show_success_message)
        self.signals.register_failed_signal.connect(self.show_error_message)
        self.signals.login_success_signal.connect(self.show_main_window)
        self.signals.login_failed_signal.connect(self.show_error_message)

    def register(self):
        # Получаем данные из полей ввода
        username = self.ui.line_login.text()
        password = self.ui.line_password.text()

        # Выполняем регистрацию в базе данных и отправляем соответствующий сигнал
        result = self.database.register(username, password)
        if "successfully" in result:
            self.signals.register_success_signal.emit(result)
        else:
            self.signals.register_failed_signal.emit(result)

    def login(self):
        # Получаем данные из полей ввода
        username = self.ui.line_login.text()
        password = self.ui.line_password.text()

        # Выполняем авторизацию в базе данных и отправляем соответствующий сигнал
        result = self.database.login(username, password)
        if "successful" in result:
            self.signals.login_success_signal.emit()
        else:
            self.signals.login_failed_signal.emit(result)

    def show_success_message(self, message):
        # Отображаем сообщение об успешной регистрации
        QtWidgets.QMessageBox.information(self, "Success", message)

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.critical(self, "Error", message)

    def show_main_window(self):
        # Отображаем главное окно приложения
        self.close()
        global windowSection
        windowSection = windows.windows_sections.WindowSections()
        windowSection.show()