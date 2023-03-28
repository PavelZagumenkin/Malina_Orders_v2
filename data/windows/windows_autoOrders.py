from PyQt6 import QtWidgets, QtGui
import data.windows.windows_sections
from data.ui.autoOrders import Ui_WindowAutoOrders


class WindowAutoOrders(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowAutoOrders()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.btn_back.clicked.connect(self.show_windowSection)

    # Закрываем выбор раздела, открываем выпечку
    def show_windowSection(self):
        self.close()
        global windowSection
        windowSection = data.windows.windows_sections.WindowSections()
        windowSection.show()
