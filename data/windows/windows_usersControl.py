from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QInputDialog
from data.ui.tableWindow import Ui_tableWindow
from data.requests.db_requests import Database
from data.signals import Signals
import data.windows.windows_control


class WindowUsersControl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_tableWindow()
        self.ui.setupUi(self)
        self.signals = Signals()
        self.database = Database()
        self.ui.btn_back.clicked.connect(self.show_windowControl)
        self.ui.label_windowName.setText('Панель управления пользователями')
        self.create_table()
        self.create_form_registration()

        # Подключаем слоты к сигналам
        self.signals.register_success_signal.connect(self.show_success_message)
        self.signals.register_failed_signal.connect(self.show_error_registration)
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
        self.label_login_password.setObjectName("label_login_password")
        self.label_login_password.setText("Введите данные для регистрации")
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
        self.ui.tableWidget.setColumnCount(5)
        self.columnName = ['ЛОГИН', 'ПАРОЛЬ', 'УРОВЕНЬ ПРАВ', 'SAVE', 'DELETE']
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columnName)
        self.font_table = QtGui.QFont()
        self.font_table.setFamily("Trebuchet MS")
        self.font_table.setBold(False)
        self.font_table.setWeight(13)
        self.font_table.setPointSize(9)
        self.ui.tableWidget.horizontalHeader().setFont(self.font_table)
        self.ui.tableWidget.verticalHeader().setFont(self.font_table)
        self.ui.tableWidget.setColumnWidth(0, 240)
        self.ui.tableWidget.setColumnWidth(1, 235)
        self.ui.tableWidget.setColumnWidth(2, 230)
        self.ui.tableWidget.setColumnWidth(3, 70)
        self.ui.tableWidget.setColumnWidth(4, 70)
        self.add_data_in_table()

    def create_form_registration(self):
        # Создаем поле для ввода логина
        self.line_login = QtWidgets.QLineEdit(self.ui.centralwidget)
        self.line_login.setGeometry(QtCore.QRect(910, 120, 346, 51))
        self.font = QtGui.QFont()
        self.font.setFamily("Trebuchet MS")
        self.font.setBold(False)
        self.font.setWeight(50)
        self.font.setPointSize(14)
        self.line_login.setFont(self.font)
        self.line_login.setTabletTracking(False)
        self.line_login.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.line_login.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.line_login.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.line_login.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.line_login.setMaxLength(24)
        self.line_login.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.line_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.line_login.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.LogicalMoveStyle)
        self.line_login.setClearButtonEnabled(False)
        self.line_login.setObjectName("line_login")
        self.line_login.setPlaceholderText("Введите логин")

        # Создаем поле для ввода пароля
        self.line_password = QtWidgets.QLineEdit(self.ui.centralwidget)
        self.line_password.setGeometry(QtCore.QRect(910, 186, 346, 51))
        self.line_password.setFont(self.font)
        self.line_password.setTabletTracking(False)
        self.line_password.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.line_password.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.line_password.setInputMethodHints(
            QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
        self.line_password.setMaxLength(16)
        self.line_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.line_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.line_password.setObjectName("line_password")
        self.line_password.setPlaceholderText("Введите пароль")

        # Создаем поле для ввода уровня прав
        self.line_role = QtWidgets.QComboBox(self.ui.centralwidget)
        self.line_role.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.line_role.setGeometry(QtCore.QRect(910, 252, 346, 51))
        self.line_role.setObjectName("line_role")
        self.line_role.setStyleSheet(open('data/css/style.css').read())
        self.line_role.setFont(self.font)
        self.listRole = ['Логист', 'Супервайзер', 'Администратор', 'Супер Админ']
        self.line_role.addItems(self.listRole)

        # Создаем кнопку регистрации нового пользователя
        self.btn_reg = QtWidgets.QPushButton(self.ui.centralwidget)
        self.btn_reg.setGeometry(QtCore.QRect(910, 318, 346, 51))
        font_button = QtGui.QFont()
        font_button.setFamily("Trebuchet MS")
        font_button.setPointSize(16)
        font_button.setBold(False)
        font_button.setWeight(50)
        self.btn_reg.setFont(font_button)
        self.btn_reg.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.btn_reg.setStyleSheet(open('data/css/style.css').read())
        self.btn_reg.setObjectName("btn_reg")
        self.btn_reg.setCheckable(False)
        self.btn_reg.setText('РЕГИСТРАЦИЯ')
        self.btn_reg.clicked.connect(self.register)

    def register(self):
        # Получаем данные из полей ввода
        username = self.line_login.text()
        password = self.line_password.text()
        if self.line_role.currentText() == "Логист":
            role = 'logist'
        elif self.line_role.currentText() == "Супервайзер":
            role = 'admin_wage'
        elif self.line_role.currentText() == "Администратор":
            role = 'admin'
        elif self.line_role.currentText() == "Супер Админ":
            role = 'superadmin'
        else:
            role = ''

        if len(username) == 0:
            self.signals.register_failed_signal.emit("Введите логин")
        elif len(password) == 0:
            self.signals.register_failed_signal.emit("Введите пароль")
        elif len(role) == 0:
            self.signals.register_failed_signal.emit('Не заданы права пользователя')
        else:
            # Выполняем регистрацию в базе данных и отправляем соответствующий сигнал
            result = self.database.register(username, password, role)
            if "успешно зарегистрирован" in result:
                self.signals.register_success_signal.emit(result)
            else:
                if 'Ошибка работы' in result:
                    self.signals.error_DB_signal.emit(result)
                else:
                    self.signals.register_failed_signal.emit(result)

    def show_success_message(self, message):
        # Отображаем сообщение об успешной регистрации
        QtWidgets.QMessageBox.information(self, "Success", message)
        self.create_table()

    def show_error_message(self, message):
        # Отображаем сообщение об успешной регистрации
        QtWidgets.QMessageBox.information(self, "Error", message)

    def show_error_registration(self, message):
        # Отображаем сообщение об ошибке
        self.label_login_password.setText(message)
        self.label_login_password.setStyleSheet('color: rgba(228, 107, 134, 1)')

    def show_windowControl(self):
        # Отображаем главное окно приложения
        self.close()
        global windowControl
        windowControl = data.windows.windows_control.WindowControl()
        windowControl.show()

    def get_count_rows(self):
        count_rows = self.database.count_row_in_DB_user_role()
        if isinstance(count_rows, int):
            return count_rows
        else:
            self.signals.register_failed_signal.emit(count_rows)
            return 0

    def add_data_in_table(self):
        result = self.database.get_users_role()
        if len(result) >= 1:
            if isinstance(result, list):
                for row in range(len(result)):
                    font = QtGui.QFont()
                    font.setFamily("Trebuchet MS")
                    font.setBold(False)
                    font.setWeight(50)
                    font.setPointSize(10)
                    self.button_reset_password = QtWidgets.QPushButton()
                    self.button_save_changes = QtWidgets.QPushButton()
                    self.button_delete_user = QtWidgets.QPushButton()
                    self.line_role_table = QtWidgets.QComboBox()
                    self.line_role_table.setObjectName("line_role")
                    self.line_role_table.setStyleSheet(open('data/css/style.css').read())
                    self.line_role_table.setFont(font)
                    self.line_role_table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
                    self.line_role_table.setInputMethodHints(
                        QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
                    self.listRole_table = ['Логист', 'Супервайзер', 'Администратор', 'Супер Админ']
                    self.line_role_table.addItems(self.listRole_table)
                    self.line_role_table.wheelEvent = lambda event: None
                    role_in_DB = 'Логист'
                    if result[row][2] == 'logist':
                        role_in_DB = 'Логист'
                    elif result[row][2] == 'admin_wage':
                        role_in_DB = 'Супервайзер'
                    elif result[row][2] == 'admin':
                        role_in_DB = 'Администратор'
                    elif result[row][2] == 'superadmin':
                        role_in_DB = 'Супер Админ'
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(result[row][1]))
                    self.ui.tableWidget.setCellWidget(row, 1, self.button_reset_password)
                    self.ui.tableWidget.cellWidget(row, 1).setText('Сбросить пароль')
                    self.ui.tableWidget.cellWidget(row, 1).setStyleSheet(open('data/css/style.css').read())
                    self.ui.tableWidget.cellWidget(row, 1).clicked.connect(self.reset_password)
                    self.ui.tableWidget.setCellWidget(row, 2, self.line_role_table)
                    self.ui.tableWidget.cellWidget(row, 2).setCurrentText(role_in_DB)
                    self.ui.tableWidget.setCellWidget(row, 3, self.button_save_changes)
                    self.ui.tableWidget.cellWidget(row, 3).setText('Сохранить')
                    self.ui.tableWidget.cellWidget(row, 3).setStyleSheet(open('data/css/style.css').read())
                    self.ui.tableWidget.setCellWidget(row, 4, self.button_delete_user)
                    self.ui.tableWidget.cellWidget(row, 4).setText('Удалить')
                    self.ui.tableWidget.cellWidget(row, 4).setStyleSheet(open('data/css/style.css').read())
            else:
                self.signals.error_DB_signal.emit(result)
        else:
            self.signals.error_DB_signal.emit('Пользователей не найдено!')

    def reset_password(self):
        buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(buttonClicked.pos())
        username = self.ui.tableWidget.item(index.row(), 0).text()
        new_pass, ok = QInputDialog.getText(self, 'Сброс пароля', f'Введите новы пароль для пользователя {username}:')
        if ok:
            result = self.database.update_password(username, new_pass)
            if "успешно изменен" in result:
                self.signals.register_success_signal.emit(result)
            else:
                if 'Ошибка работы' in result:
                    self.signals.error_DB_signal.emit(result)
                else:
                    self.signals.error_DB_signal.emit(result)
        else:
            return


