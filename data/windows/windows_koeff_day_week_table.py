import sys

from PyQt6 import QtWidgets, QtGui
import json
import textwrap
import pandas as pd
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QInputDialog
from data.requests.db_requests import Database
from data.signals import Signals
from data.active_session import Session
from data.ui.autozakaz_table import Ui_autozakaz_table
import data.windows.windows_bakery

class WindowKoeffDayWeek(QtWidgets.QMainWindow):
    def __init__(self, wb_OLAP_dayWeek, periodDay, points):
        super().__init__()
        self.ui = Ui_autozakaz_table()
        self.ui.setupUi(self)
        self.database = Database()
        self.signals = Signals()
        self.session = Session.get_instance()  # Получение экземпляра класса Session