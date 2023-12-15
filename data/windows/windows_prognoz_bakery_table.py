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
from data.ui.prognoz_table import Ui_prognoz_table
import data.windows.windows_bakery

class WindowPrognozBakeryTablesSet(QtWidgets.QMainWindow):
    def __init__(self, wb_OLAP_prodagi, periodDay, points):
        super().__init__()
        self.ui = Ui_prognoz_table()
        self.ui.setupUi(self)
        self.database = Database()
        self.signals = Signals()
        self.session = Session.get_instance()  # Получение экземпляра класса Session
        self.periodDay = periodDay
        self.column_title = ['', '', 'Кф. товара', 'Выкладка', 'Квант поставки', 'Замес', 'Код блюда', 'Блюдо', 'Категория блюда']
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
            if self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(), self.ui.tableWidget.item(row_spin, 7).text(), self.ui.tableWidget.item(row_spin, 8).text()) == 'Отмена':
                self.ui.tableWidget.removeRow(row_spin)
                for c in range(9, self.ui.tableWidget.columnCount()):
                    del saveZnach[c][row_spin]
                for c in range(9, self.ui.tableWidget.columnCount()):
                    counter = row_spin + 1
                    for r in range(row_spin, self.ui.tableWidget.rowCount()):
                        saveZnach[c][r] = saveZnach[c].pop(counter)
                        counter += 1
                continue
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
            self.ui.tableWidget.cellWidget(row_spin, 3).setValue(self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(), self.ui.tableWidget.item(row_spin, 7).text(), self.ui.tableWidget.item(row_spin, 8).text())[4])
            self.ui.tableWidget.cellWidget(row_spin, 3).setSingleStep(1)
            self.ui.tableWidget.setCellWidget(row_spin, 4, self.KvantSpin)
            self.ui.tableWidget.cellWidget(row_spin, 4).setMaximum(1000)
            self.ui.tableWidget.cellWidget(row_spin, 4).setValue(self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(), self.ui.tableWidget.item(row_spin, 7).text(), self.ui.tableWidget.item(row_spin, 8).text())[5])
            self.ui.tableWidget.cellWidget(row_spin, 4).setSingleStep(1)
            self.ui.tableWidget.setCellWidget(row_spin, 5, self.BatchSpin)
            self.ui.tableWidget.cellWidget(row_spin, 5).setMaximum(1000)
            self.ui.tableWidget.cellWidget(row_spin, 5).setValue(self.poisk_display_kvant_batch(self.ui.tableWidget.item(row_spin, 6).text(), self.ui.tableWidget.item(row_spin, 7).text(), self.ui.tableWidget.item(row_spin, 8).text())[6])
            self.ui.tableWidget.cellWidget(row_spin, 5).setSingleStep(1)
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
    #     self.ui.tableWidget.cellWidget(0, 7).clicked.connect(self.saveAndCloseDef)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.cellChanged.connect(lambda row, col: self.on_cell_changed(row, col))
    #     self.addPeriod(self.periodDay)

        # Подключаем слоты к сигналам
        self.signals.success_signal.connect(self.show_success_message)
        self.signals.failed_signal.connect(self.show_error_message)
        self.signals.error_DB_signal.connect(self.show_DB_error_message)

    def on_cell_changed(self, row, col):
        if row >= 1 and col >= 9:
        # Получаем содержимое ячейки и проверяем, является ли оно числом
            try:
                value = float(self.ui.tableWidget.item(row, col).text())
            except ValueError:
                value = None
        # Если содержимое не является числом, то заменяем его на 0.0
            if value is None:
                self.signals.failed_signal.emit('Вы ввели не число!')
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(0.0)))
        else:
            return


    def raschetPrognoz(self):
        buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(buttonClicked.pos())
        if index.row() == 0:
            for i in range(1, self.ui.tableWidget.rowCount()):
                result = round(float(saveZnach[index.column()][i]) * float(self.ui.tableWidget.cellWidget(0, index.column()).value()) * float(self.ui.tableWidget.cellWidget(i, 2).value()), 2)
                self.ui.tableWidget.setItem(i, index.column(), QTableWidgetItem(str(result)))
        else:
            for i in range(9, self.ui.tableWidget.columnCount()):
                result = round(float(saveZnach[i][index.row()]) * float(self.ui.tableWidget.cellWidget(index.row(), 2).value()) * float(self.ui.tableWidget.cellWidget(0, i).value()), 2)
                self.ui.tableWidget.setItem(index.row(), i, QTableWidgetItem(str(result)))

    # def saveAndCloseDef(self):
    #     savePeriod = self.periodDay
    #     saveNull = saveZnach.copy()
    #     headers = self.columnLables.copy()
    #     del headers[0:2]
    #     saveHeaders = headers
    #     saveDB = {}
    #     for col in range(2, self.ui.tableWidget.columnCount()):
    #         saveDB[col] = {}
    #         for row in range(0, self.ui.tableWidget.rowCount()):
    #             if col == 2 or col == 3 or row == 0:
    #                 if self.ui.tableWidget.cellWidget(row, col) == None:
    #                     saveDB[col][row] = 0
    #                 elif (row == 0 and col == 4) or (row == 0 and col == 5):
    #                     saveDB[col][row] = 0
    #                 else:
    #                     saveDB[col][row] = float(self.ui.tableWidget.cellWidget(row, col).value())
    #             elif col == 4 or col == 5 or col == 6:
    #                 saveDB[col][row] = self.ui.tableWidget.item(row, col).text()
    #             else:
    #                 saveDB[col][row] = float(self.ui.tableWidget.item(row, col).text())
    #     self.insertInDB(savePeriod, json.dumps(saveHeaders, ensure_ascii=False), json.dumps(saveDB, ensure_ascii=False), json.dumps(saveNull, ensure_ascii=False))
    #     for i in range(1, self.ui.tableWidget.rowCount()):
    #         self.saveLayoutInDB(self.ui.tableWidget.item(i, 4).text(), self.ui.tableWidget.item(i, 5).text(), int(self.ui.tableWidget.cellWidget(i, 3).value()))
    #     self.close()
    #
    def copyRow(self):
        buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(buttonClicked.pos())
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        self.copyRowButton = QtWidgets.QPushButton()
        self.ui.tableWidget.setCellWidget(rowPosition, 0, self.copyRowButton)
        self.ui.tableWidget.cellWidget(rowPosition, 0).setText('')
        iconCopy = QtGui.QIcon()
        iconCopy.addPixmap(QtGui.QPixmap("data/images/copy.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.tableWidget.cellWidget(rowPosition, 0).setIcon(iconCopy)
        self.ui.tableWidget.cellWidget(rowPosition, 0).clicked.connect(self.copyRow)
        self.deleteRowButton = QtWidgets.QPushButton()
        self.ui.tableWidget.setCellWidget(rowPosition, 1, self.deleteRowButton)
        self.ui.tableWidget.cellWidget(rowPosition, 1).setText('')
        iconCross = QtGui.QIcon()
        iconCross.addPixmap(QtGui.QPixmap("data/images/cross.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.tableWidget.cellWidget(rowPosition, 1).setIcon(iconCross)
        self.ui.tableWidget.cellWidget(rowPosition, 1).clicked.connect(self.deleteRow)
        self.KFTovarDSpin = QtWidgets.QDoubleSpinBox()
        self.DisplaySpin = QtWidgets.QSpinBox()
        self.KvantSpin = QtWidgets.QSpinBox()
        self.BatchSpin = QtWidgets.QSpinBox()
        self.KFTovarDSpin.wheelEvent = lambda event: None
        self.DisplaySpin.wheelEvent = lambda event: None
        self.KvantSpin.wheelEvent = lambda event: None
        self.BatchSpin.wheelEvent = lambda event: None
        self.ui.tableWidget.setCellWidget(rowPosition, 2, self.KFTovarDSpin)
        self.ui.tableWidget.cellWidget(rowPosition, 2).setValue(1.00)
        self.ui.tableWidget.cellWidget(rowPosition, 2).setSingleStep(0.01)
        self.ui.tableWidget.cellWidget(rowPosition, 2).valueChanged.connect(self.raschetPrognoz)
        self.ui.tableWidget.setCellWidget(rowPosition, 3, self.DisplaySpin)
        self.ui.tableWidget.cellWidget(rowPosition, 3).setMaximum(1000)
        self.ui.tableWidget.cellWidget(rowPosition, 3).setSingleStep(1)
        self.ui.tableWidget.setCellWidget(rowPosition, 4, self.KvantSpin)
        self.ui.tableWidget.cellWidget(rowPosition, 4).setMaximum(1000)
        self.ui.tableWidget.cellWidget(rowPosition, 4).setSingleStep(1)
        self.ui.tableWidget.setCellWidget(rowPosition, 5, self.BatchSpin)
        self.ui.tableWidget.cellWidget(rowPosition, 5).setMaximum(1000)
        self.ui.tableWidget.cellWidget(rowPosition, 5).setSingleStep(1)
        for c in range(6, 8):
            if c == 6:
                self.ui.tableWidget.setItem(rowPosition, c, QTableWidgetItem('Код'))
            elif c == 7:
                self.ui.tableWidget.setItem(rowPosition, c, QTableWidgetItem('Введите название блюда'))
        for c in range(8, 9):
            self.ui.tableWidget.setItem(rowPosition, c, QTableWidgetItem(self.ui.tableWidget.item(index.row(), c).text()))
        for c in range(9, self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.setItem(rowPosition, c, QTableWidgetItem(str(round(saveZnach[c][index.row()] * float(self.ui.tableWidget.cellWidget(0, c).value()), 2))))
        for c in range(9, self.ui.tableWidget.columnCount()):
            saveZnach[c][rowPosition] = round(float(self.ui.tableWidget.item(rowPosition, c).text()) / float(self.ui.tableWidget.cellWidget(0, c).value()), 2)


    def deleteRow(self):
        buttonClicked = self.sender()
        index = self.ui.tableWidget.indexAt(buttonClicked.pos())
        self.ui.tableWidget.removeRow(index.row())
        for c in range(9, self.ui.tableWidget.columnCount()):
            del saveZnach[c][index.row()]
        for c in range(9, self.ui.tableWidget.columnCount()):
            counter = index.row() + 1
            for r in range(index.row(), self.ui.tableWidget.rowCount()):
                saveZnach[c][r] = saveZnach[c].pop(counter)
                counter += 1
    #
    # def signal_layout(self, value):
    #     global layout
    #     if value != 'Код отсутствует в БД':
    #         layout = value
    #     else:
    #         layout = self.dialogAddLayout()
    #
    # Поиск кода в базе данных
    def poisk_display_kvant_batch(self, kod, name, category):
        result = self.database.poisk_data_tovar(kod)
        if not result:
            result_request = self.dialog_add_display_kvant_batch(kod, name, category)
            if result_request == 'Отмена':
                return 'Отмена'
            elif result_request == 'Товар успешно зарегистрирован':
                result = self.database.poisk_data_tovar(kod)
                return result[0]
            elif 'Ошибка' in result_request:
                self.signals.error_DB_signal.emit(result_request)
                return 'Отмена'
        else:
            return result[0]

    def dialog_add_display_kvant_batch(self, kod, name, category):
        # Создаем диалоговое окно
        dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()
        display_line_edit = QtWidgets.QLineEdit(dialog)
        display_line_edit.setValidator(QtGui.QIntValidator())
        kvant_line_edit = QtWidgets.QLineEdit(dialog)
        kvant_line_edit.setValidator(QtGui.QIntValidator())
        batch_line_edit = QtWidgets.QLineEdit(dialog)
        batch_line_edit.setValidator(QtGui.QIntValidator())
        kf_ice_sklad_line_edit = QtWidgets.QLineEdit(dialog)
        kf_ice_sklad_line_edit.setValidator(QtGui.QDoubleValidator())
        button_ok = QtWidgets.QPushButton('Добавить', dialog)
        button_ok.clicked.connect(dialog.accept)
        layout.addWidget(QtWidgets.QLabel(f'Установите необходимые значения для товара\nотсутствующего в БД, код: {kod}, наименование: {name}'))
        layout.addWidget(QtWidgets.QLabel('Выкладка:'))
        layout.addWidget(display_line_edit)
        display_line_edit.setText('1')
        layout.addWidget(QtWidgets.QLabel('Квант поставки:'))
        layout.addWidget(kvant_line_edit)
        kvant_line_edit.setText('1')
        layout.addWidget(QtWidgets.QLabel('Минимальный замес:'))
        layout.addWidget(batch_line_edit)
        batch_line_edit.setText('1')
        layout.addWidget(QtWidgets.QLabel('Коэффициент для пекарни:'))
        layout.addWidget(kf_ice_sklad_line_edit)
        kf_ice_sklad_line_edit.setText('1')
        layout.addWidget(button_ok)
        dialog.setLayout(layout)
        dialog.setWindowTitle('Добавление нового товара в БД')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/images/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dialog.setWindowIcon(icon)
        # Открываем диалоговое окно и ждем его завершения
        request = dialog.exec()
        # Проверям результат обращения к БД
        otvet_DB = "Отмена"
        if request == 1:
            display = display_line_edit.text()
            kvant = kvant_line_edit.text()
            batch = batch_line_edit.text()
            kf_ice_sklad = kf_ice_sklad_line_edit.text()
            otvet_DB = self.database.insert_data_tovar(kod, name, category, display, kvant, batch, kf_ice_sklad)
        return otvet_DB


    #
    # def addPeriod(self, period):
    #     self.check_db.thr_addPeriod(period)
    #
    # def proverkaPerioda(self, period):
    #     self.check_db.thr_proverkaPerioda(period)
    #     return otvetPeriod
    #
    # def signal_period(self, value):
    #     global otvetPeriod
    #     if value == 'Пусто':
    #         otvetPeriod = 0
    #     elif value == 'За этот период есть сформированный прогноз':
    #         otvetPeriod = 1
    #     elif value == 'Есть и то и то':
    #         otvetPeriod = 2
    #
    def show_success_message(self, message):
        pass

    def show_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def show_DB_error_message(self, message):
        # Отображаем сообщение об ошибке
        QtWidgets.QMessageBox.information(self, "Ошибка", message)


    def closeEvent(self, event):
        reply = QMessageBox()
        reply.setWindowTitle("Завершение работы с таблицой")
        reply.setWindowIcon(QtGui.QIcon("data/images/icon.png"))
        reply.setText("Вы хотите завершить работу с таблицей?")
        reply.setIcon(QMessageBox.Icon.Question)
        reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply.setDefaultButton(QMessageBox.StandardButton.Cancel)
        otvet = reply.exec()
        if otvet == QMessageBox.StandardButton.Yes:
            # event.accept()
            # if self.proverkaPerioda(self.periodDay) == 0:
            #     self.delPeriodInDB(self.periodDay)
            global WindowBakery
            WindowBakery = data.windows.windows_bakery.WindowBakery()
            WindowBakery.show()
        else:
            event.ignore()