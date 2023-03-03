from PyQt6 import QtWidgets, QtGui
from ui.control import Ui_WindowControl
from session.ActiveSession import Session
import windows.windows_sections
from handler.signals import Signals
from requests.db_requests import Database

class WindowControl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowControl()
        self.ui.setupUi(self)
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        role = self.session.get_role()  # Получение роли пользователя из экземпляра класса Session
        self.ui.btn_back.clicked.connect(self.back)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

    def back(self):
        self.close()
        global windowSection
        windowSection = windows.windows_sections.WindowSections()
        windowSection.show()


