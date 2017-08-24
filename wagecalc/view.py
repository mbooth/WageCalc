from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from model import ShiftTableModel
from model import PayRateTableModel
import traceback

class ShiftTableView(QtWidgets.QTableView):
    def __init__(self, master, showfrom, showto):
        QtWidgets.QTableView.__init__(self)
        self.requested_from=showfrom
        self.requested_to=showto
        self.requested_length=self.requested_to-self.requested_from
        self.setSortingEnabled(True)
        self.model = ShiftTableModel(master,self.requested_from, self.requested_to)
        self.sortmodel=QtCore.QSortFilterProxyModel()
        self.sortmodel.setSourceModel(self.model)
        self.setModel(self.sortmodel)
        self.sortByColumn(0,QtCore.Qt.AscendingOrder) #Initial sort by shift date (col 0)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.resizeRowsToContents()
        self.setCornerButtonEnabled(True)
        self.resizeColumnToContents(0) #Date
        self.setColumnWidth(0,120) #Date
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

class PayRateComboBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        self.shiftlist=parent.shiftlist
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        # This populates the combobox when editing a shift, with a list of pay rates
        # At the moment it populates with all pay rates
        # TODO, figure out how to only list payrates that match the shift start date
        editor = QtWidgets.QComboBox(parent)
        # if (index.column() == 7):
        #     for _ in range(len(self.payratelist)):
        #         editor.addItem(str(self.payratelist[_].dayrate))
        # elif (index.column() == 8):
        #     for _ in range(len(self.payratelist)):
        #         editor.addItem(str(self.payratelist[_].nightrate))
        return editor

    def setModelData(self, editor, model, index):
        if not index.isValid():
            return 0
        else:
            index.model().setData(index, editor.currentText(), QtCore.Qt.EditRole)
        return
class PayRateDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,parent):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        editor.setValidator(QtGui.QDoubleValidator(0.0001,9999.999999, 4))
        return editor
class CalendarDelegate(QtWidgets.QStyledItemDelegate):
    """ Allow editing of field by date only, assisted by calendar popup"""
    def __init__(self, parent):
        QtWidgets.QStyledItemDelegate.__init__(self,parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDateEdit(parent)
        editor.setCalendarPopup(True)
        return editor
class DateSortProxyModel(QtCore.QSortFilterProxyModel):
    """ Sort date columns by year, then month, then day"""
    def __init__(self):
        QtCore.QSortFilterProxyModel.__init__(self)

    def lessThan(self, QModelIndex1, QModelIndex2):
        if QModelIndex1.column() in [1,2]: # If column is DateFrom or DateTo
            left = QtCore.QDate.fromString(QModelIndex1.data(),'dd/MM/yyyy')
            right = QtCore.QDate.fromString(QModelIndex2.data(),'dd/MM/yyyy')
            return left < right
        else:
            return QModelIndex1.data() < QModelIndex2.data()
class PayRateTableView(QtWidgets.QTableView):
    """ Display table of editable pay rates"""
    def __init__(self, master):
        QtWidgets.QTableView.__init__(self)
        self.hideColumn(0)
        self.setSortingEnabled(True)
        self.model = PayRateTableModel(master)
        self.sortmodel=DateSortProxyModel()
        self.sortmodel.setSourceModel(self.model)
        self.setModel(self.sortmodel)
        self.sortByColumn(1,QtCore.Qt.AscendingOrder)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setItemDelegateForColumn(1, CalendarDelegate(master))
        self.setItemDelegateForColumn(2, CalendarDelegate(master))
        self.setItemDelegateForColumn(3, PayRateDelegate(master))
        self.setItemDelegateForColumn(4, PayRateDelegate(master))
        self.vhead=self.verticalHeader()
        self.vhead.setVisible(False)
        self.vhead.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.vhead.customContextMenuRequested.connect(self.contextMenuEvent)
    def sizeHintForRow(self, p_int):
        return 20

    def contextMenuEvent(self, event):
        index = self.currentIndex()
        menu=QtWidgets.QMenu(self)
        menu.popup(QtGui.QCursor.pos())
        deleteAction = menu.addAction("Delete Row")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == deleteAction:
            self.model.removeRow(index.row())
            self.model.submitAll()
            self.repaint()