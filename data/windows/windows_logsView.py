from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QInputDialog, QMessageBox
from data.ui.tableWindow import Ui_tableWindow
from data.requests.db_requests import Database
from data.signals import Signals
import data.windows.windows_control


class WindowLogsView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_tableWindow()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.ui.btn_back.clicked.connect(self.show_windowControl)
        self.ui.label_windowName.setText('Панель просмотра логов')
        self.create_table()

        # Подключаем слоты к сигналам
        self.signals.error_DB_signal.connect(self.show_error_message)

        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

        # Настройка стиля
        self.font = QtGui.QFont()
        self.font.setFamily("Trebuchet MS")
        self.font.setBold(False)
        self.font.setWeight(50)
        self.font.setPointSize(14)
        # Текст с подсказкой о периоде
        self.label_period_poisk = QtWidgets.QLabel(self.ui.centralwidget)
        self.label_period_poisk.setGeometry(QtCore.QRect(897, 80, 372, 20))
        self.label_period_poisk.setFont(self.font)
        self.label_period_poisk.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_period_poisk.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_period_poisk.setObjectName("label_period")
        self.label_period_poisk.setText("Укажите период")
        self.label_period_poisk.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Начальная дата периода
        self.start_day = QtWidgets.QDateEdit(self.ui.centralwidget)
        self.start_day.setGeometry(QtCore.QRect(910, 110, 150, 41))
        self.start_day.setObjectName("dateEdit_startDay")
        self.start_day.setStyleSheet(open('data/css/QDateEdit.qss').read())
        self.start_day.setFont(self.font)
        self.start_day.setCalendarPopup(True)
        self.start_day.setTimeSpec(QtCore.Qt.TimeSpec.LocalTime)
        self.start_day.setDate(QtCore.QDate.currentDate().addDays(-6))
        self.start_day.userDateChanged['QDate'].connect(self.setEndDay)
        # Тире между датами
        self.label_tire = QtWidgets.QLabel(self.ui.centralwidget)
        self.label_tire.setGeometry(QtCore.QRect(1060, 110, 46, 41))
        self.label_tire.setFont(self.font)
        self.label_tire.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_tire.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_tire.setObjectName("label_tire")
        self.label_tire.setText("-")
        self.label_tire.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Конечная дата периода
        self.end_day = QtWidgets.QDateEdit(self.ui.centralwidget)
        self.end_day.setGeometry(QtCore.QRect(1106, 110, 150, 41))
        self.end_day.setObjectName("dateEdit_endDay")
        self.end_day.setStyleSheet(open('data/css/QDateEdit.qss').read())
        self.end_day.setFont(self.font)
        self.end_day.setCalendarPopup(True)
        self.end_day.setTimeSpec(QtCore.Qt.TimeSpec.LocalTime)
        self.end_day.setDate(QtCore.QDate.currentDate())
        self.end_day.userDateChanged['QDate'].connect(self.setStartDay)
        # Текст с подсказкой о поиске
        self.label_period_poisk = QtWidgets.QLabel(self.ui.centralwidget)
        self.label_period_poisk.setGeometry(QtCore.QRect(897, 170, 372, 20))
        self.label_period_poisk.setFont(self.font)
        self.label_period_poisk.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_period_poisk.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_period_poisk.setObjectName("label_poisk")
        self.label_period_poisk.setText("Введите фразу для поиска")
        self.label_period_poisk.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Поле ввода текста для поиска
        self.line_find = QtWidgets.QLineEdit(self.ui.centralwidget)
        self.line_find.setGeometry(QtCore.QRect(910, 200, 346, 51))
        self.line_find.setFont(self.font)
        self.line_find.setTabletTracking(False)
        self.line_find.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.line_find.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.line_find.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.line_find.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.line_find.setMaxLength(24)
        self.line_find.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.line_find.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.line_find.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.LogicalMoveStyle)
        self.line_find.setClearButtonEnabled(False)
        self.line_find.setObjectName("line_find")
        self.line_find.setPlaceholderText("Что найти?")
        # Кнопка фильтра
        self.find_button = QtWidgets.QPushButton(self.ui.centralwidget)
        self.find_button.setGeometry(QtCore.QRect(910, 270, 346, 51))
        self.find_button.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.find_button.setFont(self.font)
        self.find_button.setStyleSheet(open('data/css/QPushButton.qss').read())
        self.find_button.setObjectName("find_button")
        self.find_button.setText("ФИЛЬТР")
        self.find_button.setCheckable(False)
        # self.find_button.clicked.connect(self.register)

        # Распологаем кнопку "Назад"
        self.ui.btn_back.setGeometry(QtCore.QRect(910, 620, 346, 51))

    def setEndDay(self):
        if self.start_day.date() > self.end_day.date():
            self.end_day.setDate(self.start_day.date())

    def setStartDay(self):
        if self.start_day.date() > self.end_day.date():
            self.start_day.setDate(self.end_day.date())

    def create_table(self):
        self.ui.tableWidget.setMaximumWidth(887)
        self.ui.tableWidget.setMinimumWidth(887)
        self.ui.tableWidget.setMinimumHeight(590)
        self.ui.tableWidget.setMaximumHeight(590)
        self.ui.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.tableWidget.setRowCount(self.get_count_rows())
        self.ui.tableWidget.setColumnCount(3)
        self.columnName = ['ДАТА', 'ВРЕМЯ', 'СОБЫТИЕ']
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columnName)
        self.font_table = QtGui.QFont()
        self.font_table.setFamily("Trebuchet MS")
        self.font_table.setBold(False)
        self.font_table.setWeight(13)
        self.font_table.setPointSize(9)
        self.ui.tableWidget.horizontalHeader().setFont(self.font_table)
        self.ui.tableWidget.verticalHeader().setFont(self.font_table)
        self.ui.tableWidget.setColumnWidth(0, 100)
        self.ui.tableWidget.setColumnWidth(1, 100)
        self.ui.tableWidget.setColumnWidth(2, 645)
        self.add_data_in_table()


    def add_data_in_table(self):
        result = self.database.get_logs()
        if len(result) >= 1:
            if isinstance(result, list):
                for row in range(len(result)):
                    font = QtGui.QFont()
                    font.setFamily("Trebuchet MS")
                    font.setBold(False)
                    font.setWeight(50)
                    font.setPointSize(10)
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(result[row][1])))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(result[row][2])))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(result[row][3]))
            else:
                self.signals.error_DB_signal.emit(result)
        else:
            self.signals.error_DB_signal.emit('Пользователей не найдено!')


    def show_error_message(self, message):
        # Отображаем сообщение об ошибке в БД
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_windowControl(self):
        # Отображаем главное окно приложения
        self.close()
        global windowControl
        windowControl = data.windows.windows_control.WindowControl()
        windowControl.show()


    def get_count_rows(self):
        count_rows = self.database.count_row_in_DB_logs()
        if isinstance(count_rows, int):
            return count_rows
        else:
            self.signals.register_failed_signal.emit(count_rows)
            return 0


    # def dialog_delete_user(self):
    #     buttonClicked = self.sender()
    #     index = self.ui.tableWidget.indexAt(buttonClicked.pos())
    #     username = self.ui.tableWidget.item(index.row(), 0).text()
    #     dialogBox = QMessageBox()
    #     dialogBox.setText(f"Вы действительно хотите пользователя {username}")
    #     dialogBox.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
    #     dialogBox.setWindowTitle('Удаление пользователя!')
    #     dialogBox.setIcon(QMessageBox.Icon.Critical)
    #     dialogBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    #     dialogBox.buttonClicked.connect(lambda button: self.delete_user(button, username))
    #     dialogBox.exec()
    #
    #
    # def delete_user(self, button_clicked, username):
    #     if button_clicked.text() == "OK":
    #         result = self.database.delete_user(username)
    #         if "успешно удален из БД" in result:
    #             self.signals.register_success_signal.emit(result)
    #         else:
    #             if 'Ошибка работы' in result:
    #                 self.signals.error_DB_signal.emit(result)
    #             else:
    #                 self.signals.error_DB_signal.emit(result)
    #             return
