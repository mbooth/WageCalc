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
    def __init__(self,parent, title="Default",):
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

class ShiftTableDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, master):
        QtWidgets.QStyledItemDelegate.__init__(self)

    def setEditorData(self, editor, index):
        value=index.model().data(index,QtCore.Qt.EditRole)
        if (index.column() == 0): #Date
            editor.setDate(value)
        elif (index.column() == 1) or (index.column() == 2): #Start / End
            editor.setEditText(value)
        elif (index.column() == 7) or (index.column() == 8):  #Day Rate / Night Rate
            editor.setEditText(value)

    def createEditor(self, parent, option, index, master):
        if not index.isValid():
            return 0
        if (index.column() == 0): #Date
            editor=QtWidgets.QDateEdit(parent)
        elif (index.column() == 1) or (index.column() == 2): #Start / End
            editor=QtWidgets.QLineEdit(parent)
            editor.setInputMask("hh:MM")
        elif (index.column() == 7): #Day Rate / Night Rate
            editor=QtWidgets.QComboBox(parent)
            for payrate in self.payrates:
                editor.addItem(master.payrates[payrate].dayrate)
        elif (index.column() == 8):
            editor=QtWidgets.QComboBox(parent)
        return editor

    def setModelData(self, editor, model, index):
        if not index.isValid():
            return 0
        if (index.column() == 1) or (index.column() == 2): #Date From or To
            index.model().setData(index, editor.date(), QtCore.Qt.EditRole)
        elif (index.column() == 3) or (index.column() == 4):  # Day or Night Rate
            index.model().setData(index, editor.text(), QtCore.Qt.EditRole)
        elif (index.column() == 5):
            index.model().setData(index, editor.text(), QtCore.Qt.EditRole)
        return


class ShiftTableView(QtWidgets.QTableView):
    def __init__(self, master, showfrom, showto):
        QtWidgets.QTableView.__init__(self)
        self.requested_from=showfrom
        self.requested_to=showto
        self.requested_length=self.requested_to-self.requested_from
        self.model = ShiftTableModel(master,self.requested_from, self.requested_to)
        self.setModel(self.model)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectItems)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setItemDelegate(ShiftTableDelegate(master))

        master.logbox.info('Viewing : ' + str(self.model.grantedall_shifts) + '/' + str(len(master.all_shifts)) + ' shifts')

    def sizeHintForRow(self, p_int):
        return 20

class TableCalendarWidget(QtWidgets.QDateEdit):
    def __init__(self, parent = None):
        super(TableCalendarWidget, self).__init__(parent)
        self.setCalendarPopup(True)

class PayRateTableDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        QtWidgets.QStyledItemDelegate.__init__(self)

    def setEditorData(self, editor, index):
        value=index.model().data(index,QtCore.Qt.EditRole)
        if (index.column() == 1) or (index.column() == 2): #Date From or To
            editor.setDate(value)
        elif (index.column() == 3) or (index.column() == 4):  # Day or Night Rate
            editor.setText(value)
        elif (index.column() == 5):
            editor.setText("")

    def createEditor(self, parent, option, index):
        if not index.isValid():
            return 0
        if (index.column() == 1) or (index.column() == 2): #Date From or To
            editor=QtWidgets.QDateEdit(parent)
        elif (index.column() == 3) or (index.column() == 4): #Day or Night Rate
            editor=QtWidgets.QLineEdit(parent)
            editor.setInputMask("00.0000")
        elif index.column() ==5: #Comments
            editor=QtWidgets.QLineEdit(parent)
        return editor

    def setModelData(self, editor, model, index):
        if not index.isValid():
            return 0
        if (index.column() == 1) or (index.column() == 2): #Date From or To
            index.model().setData(index, editor.date(), QtCore.Qt.EditRole)
        elif (index.column() == 3) or (index.column() == 4):  # Day or Night Rate
            index.model().setData(index, editor.text(), QtCore.Qt.EditRole)
        elif (index.column() == 5):
            index.model().setData(index, editor.text(), QtCore.Qt.EditRole)
        return
class PayRateTableView(QtWidgets.QTableView):
    def __init__(self, master):
        QtWidgets.QTableView.__init__(self)
        self.model = PayRateTableModel(master)
        self.verticalHeader().setVisible(False)
        self.setModel(self.model)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectItems)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setItemDelegate(PayRateTableDelegate())

    def sizeHintForRow(self, p_int):
        return 20
