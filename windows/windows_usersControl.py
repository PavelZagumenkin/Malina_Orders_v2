from PyQt6 import QtWidgets, QtGui
from ui.usersControl import Ui_WindowUserControl
from requests.db_requests import Database
from handler.signals import Signals
import windows.windows_control

class WindowUsersControl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowUserControl()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.ui.btn_back.clicked.connect(self.show_windowControl)

        # Подключаем слоты к сигналам
        # self.signals.register_success_signal.connect(self.show_success_message)
        # self.signals.register_failed_signal.connect(self.show_error_message)

        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

    def register(self):
        pass
        # Получаем данные из полей ввода
        # username = self.ui.line_login.text()
        # password = self.ui.line_password.text()

        # Выполняем регистрацию в базе данных и отправляем соответствующий сигнал
    #     result = self.database.register(username, password)
    #     if "successfully" in result:
    #         self.signals.register_success_signal.emit(result)
    #     else:
    #         self.signals.register_failed_signal.emit(result)
    #
    # def show_success_message(self, message):
    #     # Отображаем сообщение об успешной регистрации
    #     QtWidgets.QMessageBox.information(self, "Success", message)
    #
    # def show_error_message(self, message):
    #     # Отображаем сообщение об ошибке
    #     QtWidgets.QMessageBox.critical(self, "Error", message)

    def show_windowControl(self):
        # Отображаем главное окно приложения
        self.close()
        global windowControl
        windowControl = windows.windows_control.WindowControl()
        windowControl.show()


