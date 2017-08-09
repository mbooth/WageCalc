from PyQt5 import QtWidgets,QtGui,QtCore
from datetime import date,datetime,timedelta
from data import ShiftTableModel
from data import PayRateTableModel
import logging
import tkinter
from tkinter import ttk
from wagecalc.modules.shift import refresh_view
from wagecalc.modules.payrate import refresh_view

class QtLogHandler(logging.Handler):
    def __init__(self,parent):
        logging.Handler.__init__(self)
        logging.Handler.setLevel(self,'INFO')
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setStyleSheet("background-color: #d0d0d0")
        self.widget.setMinimumWidth(800)
        self.widget.setReadOnly(True)

    def emit(self,record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
class LogBox(QtWidgets.QDockWidget):
    def __init__(self):
        QtWidgets.QDockWidget.__init__(self)
        self.setWindowTitle("Log")
        self.logTextBox=QtLogHandler(self)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s','%H:%M:%S'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel('INFO')
        self.setWidget(self.logTextBox.widget)

    def debug(self,errormessage):
        logging.debug(errormessage)
    def info(self,errormessage):
        logging.info(errormessage)
    def warning(self,errormessage):
        logging.warning(errormessage)
    def error(self,errormessage):
        logging.error(errormessage)
    def critical(self,errormessage):
        logging.critical(errormessage)
class LargeButton(QtWidgets.QPushButton):
    def __init__(self,parent,command,text="****"):
        QtWidgets.QPushButton.__init__(self)
        self.setFixedHeight(50)
        self.setText(text)
        self.clicked.connect(command)
        parent.layout.addWidget(self)
class ToolBar(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__()
        self.hframe=QtWidgets.QHBoxLayout()
        self.setLayout(self.hframe)
        parent.addWidget(self)
class Module(QtWidgets.QMainWindow):
    def __init__(self,parent, title="Default"):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.tbar=self.addToolBar("Toolbar")
        self.tbar.setMovable(False)
        parent.setCentralWidget(self)
class TAction(QtWidgets.QAction):
    def __init__(self, text, parent, callback):
        QtWidgets.QAction.__init__(self, text, parent)
        self.triggered.connect(callback)
        parent.addAction(self)
class TButton(QtWidgets.QPushButton):
    def __init__(self, text, parent, callback):
        QtWidgets.QPushButton.__init__(self,text,parent)
        self.setText(text)
        self.clicked.connect(callback)
        parentwindow=parent.parent()
        self.setStyle(parentwindow.style())
class TSpacer(QtWidgets.QWidget):
    def __init__(self,parent):
        QtWidgets.QWidget.__init__(self)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        parent.addWidget(self)
class TDateBar(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__()
        self.hframe=QtWidgets.QHBoxLayout()
        self.setLayout(self.hframe)
        parent.addWidget(self)
class TDatePicker(QtWidgets.QDialog):
    def __init__(self, master, parent, initialdate, text):
        super(TDatePicker, self).__init__(parent)
        layout=QtWidgets.QVBoxLayout(self)
        parentwindow=parent.parent()
        self.setStyle(parentwindow.style())
        date=QtCore.QDate(initialdate)
        label = QtWidgets.QLabel(text)
        self.datewidget = QtWidgets.QDateEdit(self)
        self.datewidget.setCalendarPopup(True)
        self.calendarwidget=QtWidgets.QCalendarWidget()
        self.calendarwidget.setFirstDayOfWeek(QtCore.Qt.Saturday)
        self.calendarwidget.setGridVisible(True)
        self.datewidget.setCalendarWidget(self.calendarwidget)
        self.datewidget.setDate(date)
        # self.datewidget.dateChanged.connect(lambda x: self.updated(master))
        parent.addWidget(label)
        parent.addWidget(self.datewidget)

    # def updated(self,master):
    #     refresh_view(master)

class PayRateComboBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        self.payratelist=parent.payratelist
        self.shiftlist=parent.shiftlist
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        # This populates the combobox when editing a shift, with a list of pay rates
        # At the moment it populates with all pay rates
        # TODO, figure out how to only list payrates that match the shift start date
        editor = QtWidgets.QComboBox(parent)
        if (index.column() == 7):
            for _ in range(len(self.payratelist)):
                editor.addItem(str(self.payratelist[_].dayrate))
        elif (index.column() == 8):
            for _ in range(len(self.payratelist)):
                editor.addItem(str(self.payratelist[_].nightrate))
        return editor

    def setModelData(self, editor, model, index):
        if not index.isValid():
            return 0
        else:
            index.model().setData(index, editor.currentText(), QtCore.Qt.EditRole)
        return

class ShiftTableView(QtWidgets.QTableView):
    def __init__(self, master, showfrom, showto):
        QtWidgets.QTableView.__init__(self)
        self.requested_from=showfrom
        self.requested_to=showto
        self.requested_length=self.requested_to-self.requested_from
        self.model = ShiftTableModel(master,self.requested_from, self.requested_to)
        self.setModel(self.model)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.resizeRowsToContents()
        self.setCornerButtonEnabled(True)
        self.setColumnWidth(0,140) #Date
        self.setColumnWidth(1,80) #Start
        self.setColumnWidth(2,80) #End
        self.setColumnWidth(3,80) #Total Length
        self.setColumnWidth(4,80) #Day Length
        self.setColumnWidth(5,80) #Night Length
        self.setColumnWidth(6,80) #Unpaid
        self.setAlternatingRowColors(True)
        self.setItemDelegateForColumn(7, PayRateComboBoxDelegate(master))
        self.setItemDelegateForColumn(8, PayRateComboBoxDelegate(master))
        master.logbox.info('Viewing : ' + str(self.model.grantedshiftlist) + '/' + str(len(master.shiftlist)) + ' shifts')

    def sizeHintForRow(self, p_int):
        return 20
class PayRateTableView(QtWidgets.QTableView):
    def __init__(self, master):
        QtWidgets.QTableView.__init__(self)
        self.model = PayRateTableModel(master)
        # self.verticalHeader().setVisible(False)
        self.setModel(self.model)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectItems)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def sizeHintForRow(self, p_int):
        return 20
