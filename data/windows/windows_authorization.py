from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from data.ui.authorization import Ui_WindowAuthorization
from data.requests.db_requests import Database
from data.signals import Signals
from data.active_session import Session
import data.windows.windows_sections

class WindowAuthorization(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAuthorization()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.ui.label_login_password.setFocus()  # Фокус по умолчанию на тексте
        self.ui.btn_login.clicked.connect(self.login)
        self.ui.btn_reg.clicked.connect(self.register)

        # Подключаем слоты к сигналам
        self.signals.register_success_signal.connect(self.show_success_message)
        self.signals.register_failed_signal.connect(self.show_error_message)
        self.signals.login_success_signal.connect(self.show_windowSection)
        self.signals.login_failed_signal.connect(self.show_error_message)

        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

        # Добавляем картинку
        self.label_logo_721 = QtWidgets.QLabel(parent=self.ui.centralwidget)
        self.label_logo_721.setGeometry(QtCore.QRect(0, 0, 731, 721))
        self.label_logo_721.setText("")
        self.label_logo_721.setPixmap(QtGui.QPixmap("data/images/logo_721.png"))
        self.label_logo_721.setScaledContents(False)
        self.label_logo_721.setObjectName("label_logo_721")

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
        login_result = self.database.login(username, password)
        if isinstance(login_result, tuple) and len(login_result) == 2:
            result, role = login_result
            if "Авторизация успешна" in result:
                self.session.set_role(role)  # сохраняем роль пользователя в объекте UserSession
                self.signals.login_success_signal.emit()
            else:
                self.signals.login_failed_signal.emit(result)
        else:
            self.signals.login_failed_signal.emit("Error occurred while logging in.")

    def show_success_message(self, message):
        # Отображаем сообщение об успешной регистрации
        QtWidgets.QMessageBox.information(self, "Success", message)

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.critical(self, "Error", message)

    def show_windowSection(self):
        # Отображаем главное окно приложения
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.ui.btn_login.click()  # Имитируем нажатие кнопки btn_login


