from PyQt6 import QtWidgets, QtGui
from data.ui.control import Ui_WindowControl
import data.windows.windows_sections
import data.windows.windows_usersControl


class WindowControl(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowControl()
        self.ui.setupUi(self)
        self.ui.btn_back.clicked.connect(self.show_windowSection)
        self.ui.btn_control_users.clicked.connect(self.show_windowUserControl)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

    def show_windowSection(self):
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()

    def show_windowUserControl(self):
        self.close()
        global windowUserControl
        windowUserControl = data.windows.windows_usersControl.WindowUsersControl()
        windowUserControl.show()
