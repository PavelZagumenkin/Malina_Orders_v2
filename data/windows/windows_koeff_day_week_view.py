import sys

from PyQt6 import QtWidgets, QtGui, QtCore
import textwrap
import pandas as pd
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox
from data.requests.db_requests import Database
from data.signals import Signals
from data.active_session import Session
from data.ui.autozakaz_table import Ui_autozakaz_table
import data.windows.windows_bakery


class WindowKoeffDayWeekView(QtWidgets.QMainWindow):
    def __init__(self, periodDay, category):
        super().__init__()
        self.ui = Ui_autozakaz_table()
        self.ui.setupUi(self)
        self.database = Database()
        self.signals = Signals()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.kod = ''
        self.name = ''
        self.periodDay = periodDay
        self.column_title = ['', '', 'Кф. товара', 'Выкладка', 'Квант поставки', 'Замес', 'Код блюда', 'Блюдо',
                             'Категория блюда']
        self.column_title = self.column_title + points
        self.column_title_for_excel = ['Код блюда', 'Блюдо', 'Категория блюда'] + points
        wb_OLAP_prodagi = wb_OLAP_prodagi[self.column_title_for_excel]
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)
        self.ui.tableWidget.setRowCount(wb_OLAP_prodagi.shape[0] + 1)
        self.ui.tableWidget.setColumnCount(len(self.column_title))
        self.wrap = []
        for header in self.column_title:
            wrap = textwrap.fill(header, width=10)
            self.wrap.append(wrap)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.wrap)
        self.font = QtGui.QFont("Times", 10, QFont.Weight.Bold)
        self.ui.tableWidget.horizontalHeader().setFont(self.font)
        # self.ui.tableWidget.setStyleSheet(open('data/css/QTableWidget.qss').read())
        for col in range(0, wb_OLAP_prodagi.shape[1]):
            for row in range(0, wb_OLAP_prodagi.shape[0]):
                if pd.isna(wb_OLAP_prodagi.iloc[row, col]):
                    item = QTableWidgetItem('0')
                else:
                    item = QTableWidgetItem(str(wb_OLAP_prodagi.iloc[row, col]))
                self.ui.tableWidget.setItem(row + 1, col + 6, item)
        global saveZnach
        saveZnach = {}
        for col in range(9, self.ui.tableWidget.columnCount()):
            saveZnach[col] = {}
            for row in range(1, self.ui.tableWidget.rowCount()):
                saveZnach[col][row] = float(self.ui.tableWidget.item(row, col).text())
        self.ui.tableWidget.setItem(0, 8, QTableWidgetItem("Кф. кондитерской"))
        self.ui.tableWidget.item(0, 8).setFont(self.font)
        for col_spin in range(9, self.ui.tableWidget.columnCount()):
            self.KFStoreSpin = QtWidgets.QDoubleSpinBox()
            self.KFStoreSpin.wheelEvent = lambda event: None
            self.ui.tableWidget.setCellWidget(0, col_spin, self.KFStoreSpin)
            self.ui.tableWidget.cellWidget(0, col_spin).setValue(1.00)
            self.ui.tableWidget.cellWidget(0, col_spin).setSingleStep(0.01)
            self.ui.tableWidget.cellWidget(0, col_spin).valueChanged.connect(self.raschetPrognoz)
        for row_spin in range(1, self.ui.tableWidget.rowCount()):
            if self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(),
                                              self.ui.tableWidget.item(row_spin, 7).text()) == 'Отмена':
                self.ui.tableWidget.removeRow(row_spin)
                for c in range(9, self.ui.tableWidget.columnCount()):
                    del saveZnach[c][row_spin]
                for c in range(9, self.ui.tableWidget.columnCount()):
                    counter = row_spin + 1
                    for r in range(row_spin, self.ui.tableWidget.rowCount()):
                        saveZnach[c][r] = saveZnach[c].pop(counter)
                        counter += 1
                continue
            self.ui.tableWidget.item(row_spin, 6).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.KFTovarDSpin = QtWidgets.QDoubleSpinBox()
            self.DisplaySpin = QtWidgets.QSpinBox()
            self.KvantSpin = QtWidgets.QSpinBox()
            self.BatchSpin = QtWidgets.QSpinBox()
            self.KFTovarDSpin.wheelEvent = lambda event: None
            self.DisplaySpin.wheelEvent = lambda event: None
            self.KvantSpin.wheelEvent = lambda event: None
            self.BatchSpin.wheelEvent = lambda event: None
            self.ui.tableWidget.setCellWidget(row_spin, 2, self.KFTovarDSpin)
            self.ui.tableWidget.cellWidget(row_spin, 2).setValue(1.00)
            self.ui.tableWidget.cellWidget(row_spin, 2).setSingleStep(0.01)
            self.ui.tableWidget.cellWidget(row_spin, 2).valueChanged.connect(self.raschetPrognoz)
            self.ui.tableWidget.setCellWidget(row_spin, 3, self.DisplaySpin)
            self.ui.tableWidget.cellWidget(row_spin, 3).setMaximum(1000)
            self.ui.tableWidget.cellWidget(row_spin, 3).setValue(
                self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(),
                                               self.ui.tableWidget.item(row_spin, 7).text())[4])
            self.ui.tableWidget.cellWidget(row_spin, 3).setSingleStep(1)
            self.ui.tableWidget.setCellWidget(row_spin, 4, self.KvantSpin)
            self.ui.tableWidget.cellWidget(row_spin, 4).setMaximum(1000)
            self.ui.tableWidget.cellWidget(row_spin, 4).setValue(
                self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(),
                                               self.ui.tableWidget.item(row_spin, 7).text())[5])
            self.ui.tableWidget.cellWidget(row_spin, 4).setSingleStep(1)
            self.ui.tableWidget.setCellWidget(row_spin, 5, self.BatchSpin)
            self.ui.tableWidget.cellWidget(row_spin, 5).setMaximum(1000)
            self.ui.tableWidget.cellWidget(row_spin, 5).setValue(
                self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(),
                                               self.ui.tableWidget.item(row_spin, 7).text())[6])
            self.ui.tableWidget.cellWidget(row_spin, 5).setSingleStep(1)
            self.ui.tableWidget.setItem(row_spin, 8, QTableWidgetItem(self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(), self.ui.tableWidget.item(row_spin, 7).text())[3]))
            self.ui.tableWidget.item(row_spin, 8).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.ui.tableWidget.setItem(row_spin, 7, QTableWidgetItem(self.sravnenie_name(self.ui.tableWidget.item(row_spin, 6).text(), self.ui.tableWidget.item(row_spin, 7).text())))
            self.ui.tableWidget.item(row_spin, 7).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        for row_button in range(1, self.ui.tableWidget.rowCount()):
            self.copyRowButton = QtWidgets.QPushButton()
            self.ui.tableWidget.setCellWidget(row_button, 0, self.copyRowButton)
            self.ui.tableWidget.cellWidget(row_button, 0).setText('')
            iconCopy = QtGui.QIcon()
            iconCopy.addPixmap(QtGui.QPixmap("data/images/copy.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.tableWidget.cellWidget(row_button, 0).setIcon(iconCopy)
            self.ui.tableWidget.cellWidget(row_button, 0).clicked.connect(self.copyRow)
            self.deleteRowButton = QtWidgets.QPushButton()
            self.ui.tableWidget.setCellWidget(row_button, 1, self.deleteRowButton)
            self.ui.tableWidget.cellWidget(row_button, 1).setText('')
            iconCross = QtGui.QIcon()
            iconCross.addPixmap(QtGui.QPixmap("data/images/cross.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.tableWidget.cellWidget(row_button, 1).setIcon(iconCross)
            self.ui.tableWidget.cellWidget(row_button, 1).clicked.connect(self.deleteRow)
        self.SaveAndClose = QtWidgets.QPushButton()
        self.ui.tableWidget.setCellWidget(0, 7, self.SaveAndClose)
        self.ui.tableWidget.cellWidget(0, 7).setText('Сохранить и закрыть')
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(12)
        font.bold()
        font.setWeight(50)
        self.ui.tableWidget.cellWidget(0, 7).setFont(font)
        self.ui.tableWidget.cellWidget(0, 7).setStyleSheet(open('data/css/QPushButton.qss').read())
        self.ui.tableWidget.cellWidget(0, 7).clicked.connect(self.saveAndCloseDef)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.cellChanged.connect(lambda row, col: self.on_cell_changed(row, col))

        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)

    def show_success_message(self, message):
        pass

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)

    def closeEvent(self, event):
        global WindowBakery
        if event.spontaneous():
            reply = QMessageBox()
            reply.setWindowTitle("Завершение работы с таблицой")
            reply.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
            reply.setText("Вы хотите завершить работу с таблицей?")
            reply.setIcon(QMessageBox.Icon.Question)
            reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            reply.setDefaultButton(QMessageBox.StandardButton.Cancel)
            otvet = reply.exec()
            if otvet == QMessageBox.StandardButton.Yes:
                event.accept()
                WindowBakery = data.windows.windows_bakery.WindowBakery()
                WindowBakery.show()
            else:
                event.ignore()
        else:
            event.accept()
            WindowBakery = data.windows.windows_bakery.WindowBakery()
            WindowBakery.show()