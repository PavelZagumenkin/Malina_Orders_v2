from PyQt6 import QtWidgets, QtGui, QtCore
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

        # Подключаем кнопку НАЗАД к функции
        self.ui.btn_back.clicked.connect(self.show_windowControl)

        # Изменяем основной текст в окне
        self.ui.label_windowName.setText('Панель управления пользователями')

        # Задаем размеры таблицы
        self.ui.tableWidget.setMaximumWidth(887)
        self.ui.tableWidget.setMinimumWidth(887)

        # Устанавливаем количество столбцов и строк в таблице
        self.ui.tableWidget.setRowCount(2)
        self.ui.tableWidget.setColumnCount(5)

        # Даем название столбцам
        self.columnName = ['ЛОГИН', 'ПАРОЛЬ', 'УРОВЕНЬ ПРАВ', 'SAVE', 'DELETE']
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columnName)

        # Устанавливаем ширину столбцов
        self.ui.tableWidget.setColumnWidth(0, 250)
        self.ui.tableWidget.setColumnWidth(1, 250)
        self.ui.tableWidget.setColumnWidth(2, 250)
        self.ui.tableWidget.setColumnWidth(3, 60)
        self.ui.tableWidget.setColumnWidth(4, 60)

        # Располагаем кнопку НАЗАД
        self.ui.btn_back.setGeometry(QtCore.QRect(1030, 650, 231, 51))

        # Текст с подсказкой о вводе логина и пароля
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setBold(False)
        font.setWeight(50)
        font.setPointSize(14)
        self.label_login_password = QtWidgets.QLabel(self.ui.centralwidget)
        self.label_login_password.setGeometry(QtCore.QRect(897, 80, 372, 20))
        self.label_login_password.setFont(font)
        self.label_login_password.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_login_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_login_password.setObjectName("label_login_password")
        self.label_login_password.setText("Введите данные для регистрации")
        self.label_login_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Создаем поле для ввода логина
        self.line_login = QtWidgets.QLineEdit(self.ui.centralwidget)
        self.line_login.setGeometry(QtCore.QRect(1030, 300, 231, 51))
        self.line_login.setFont(font)
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
        self.line_password.setGeometry(QtCore.QRect(1030, 400, 231, 51))
        self.line_password.setFont(font)
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
        self.line_role.setGeometry(QtCore.QRect(1030, 470, 231, 51))
        self.line_role.setFont(font)
        self.line_role.setTabletTracking(False)
        self.line_role.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.line_role.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.line_role.setInputMethodHints(
            QtCore.Qt.InputMethodHint.ImhHiddenText | QtCore.Qt.InputMethodHint.ImhNoAutoUppercase | QtCore.Qt.InputMethodHint.ImhNoPredictiveText | QtCore.Qt.InputMethodHint.ImhSensitiveData)
        self.listRole = ['Логист', 'Супервайзер', 'Администратор', 'Супер Админ']
        self.line_role.addItems(self.listRole)
        self.line_role.setObjectName("line_role")
        self.line_role.setPlaceholderText('123')

        # Создаем кнопку регистрации нового пользователя
        self.btn_reg = QtWidgets.QPushButton(self.ui.centralwidget)

        # Распологаем кнопку Регистрация
        self.btn_reg.setGeometry(QtCore.QRect(1030, 550, 231, 51))

        # Настраиваем визуал кнопки регистрации
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btn_reg.setFont(font)
        self.btn_reg.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.btn_reg.setStyleSheet("QPushButton {\n"
                                   "background-color: rgb(228, 107, 134);\n"
                                   "border: none;\n"
                                   "border-radius: 10px}\n"
                                   "\n"
                                   "QPushButton:hover {\n"
                                   "border: 1px solid  rgb(0, 0, 0);\n"
                                   "background-color: rgba(228, 107, 134, 0.9)\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "border:3px solid  rgb(0, 0, 0);\n"
                                   "background-color: rgba(228, 107, 134, 1)\n"
                                   "}")
        self.btn_reg.setCheckable(False)
        self.btn_reg.setObjectName("btn_reg")

        # Меняем текст на кнопке регистрации
        self.btn_reg.setText('РЕГИСТРАЦИЯ')

        # Подключаем слоты к сигналам
        # self.signals.register_success_signal.connect(self.show_success_message)
        # self.signals.register_failed_signal.connect(self.show_error_message)

        # Устанавливаем иконку
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
        windowControl = data.windows.windows_control.WindowControl()
        windowControl.show()
