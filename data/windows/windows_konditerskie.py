from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QInputDialog, QMessageBox
from data.ui.tableWindow import Ui_tableWindow
from data.requests.db_requests import Database
from data.signals import Signals
import data.windows.windows_logistics
from data.active_session import Session
import datetime

class WindowKonditerskie(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_tableWindow()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.ui.btn_back.clicked.connect(self.show_windowLogistik)
        self.ui.label_windowName.setText('Список кондитерских')

        self.create_table()
        # self.create_form_add_konditerskay()

        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_error_message)

        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

        # Текст с подсказкой о вводе логина и пароля
        self.font = QtGui.QFont()
        self.font.setFamily("Trebuchet MS")
        self.font.setBold(False)
        self.font.setWeight(50)
        self.font.setPointSize(14)
        self.label_login_password = QtWidgets.QLabel(self.ui.centralwidget)
        self.label_login_password.setGeometry(QtCore.QRect(897, 80, 372, 20))
        self.label_login_password.setFont(self.font)
        self.label_login_password.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_login_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_login_password.setObjectName("label_add_konditerskay")
        self.label_login_password.setText("Добавление кондитерской")
        self.label_login_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Распологаем кнопку "Назад"
        self.ui.btn_back.setGeometry(QtCore.QRect(910, 620, 346, 51))

    def create_table(self):
        self.ui.tableWidget.setMaximumWidth(887)
        self.ui.tableWidget.setMinimumWidth(887)
        self.ui.tableWidget.setMinimumHeight(590)
        self.ui.tableWidget.setMaximumHeight(590)
        self.ui.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.tableWidget.setRowCount(self.get_count_rows())
        self.ui.tableWidget.setColumnCount(8)
        self.columnName = ['НАЗВАНИЕ', 'ТИП', 'ПЕЧЬ', 'МОРОЗИЛЬНЫЙ СКЛАД', 'ТУАЛЕТ', 'СТОЛИКИ', 'РАБОТАЕТ', '']
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columnName)
        self.font_table = QtGui.QFont()
        self.font_table.setFamily("Trebuchet MS")
        self.font_table.setBold(False)
        self.font_table.setWeight(13)
        self.font_table.setPointSize(9)
        self.ui.tableWidget.horizontalHeader().setFont(self.font_table)
        self.ui.tableWidget.verticalHeader().setFont(self.font_table)
        self.ui.tableWidget.setColumnWidth(0, 120)
        self.ui.tableWidget.setColumnWidth(1, 100)
        self.ui.tableWidget.setColumnWidth(2, 20)
        self.ui.tableWidget.setColumnWidth(3, 20)
        self.ui.tableWidget.setColumnWidth(4, 20)
        self.ui.tableWidget.setColumnWidth(5, 20)
        self.ui.tableWidget.setColumnWidth(6, 20)
        self.ui.tableWidget.setColumnWidth(7, 80)
        # self.add_data_in_table()


    def get_count_rows(self):
        count_rows = self.database.count_row_in_DB_konditerskie()
        if isinstance(count_rows, int):
            return count_rows
        else:
            self.signals.failed_signal.emit(count_rows)
            return 0


    def show_windowLogistik(self):
        # Отображаем главное окно приложения
        self.close()
        global windowLogistik
        windowLogistik = data.windows.windows_logistics.WindowLogistics()
        windowLogistik.show()

    def show_success_message(self, message):
        if "успешно" in message:
            # Отображаем сообщение об успешной операции
            QtWidgets.QMessageBox.information(self, "Успешно", message)
        else:
            self.create_table()

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке в БД
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def closeEvent(self, event):
        if event.spontaneous():
            username = self.session.get_username()  # Получение имени пользователя из экземпляра класса Session
            logs_result = self.database.add_log(datetime.datetime.now().date(), datetime.datetime.now().time(),
                                            f"Пользователь {username} вышел из системы.")
            if "Лог записан" in logs_result:
                self.signals.success_signal.emit(logs_result)
            elif 'Ошибка работы' in logs_result:
                self.signals.error_DB_signal.emit(logs_result)
            else:
                self.signals.failed_signal.emit(logs_result)
        event.accept()