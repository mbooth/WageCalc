from PyQt5 import QtWidgets,QtGui,QtCore
from datetime import datetime, timedelta
import wagecalc.file
import gui

from data import Shift

def clear_shift_data(self):
    try:
        del self.shiftlist
    except Exception:
        return

def refresh_view(self):
    try:
        self.mod_shift.tv.close()
    except Exception:
        pass
    qnewdatefrom=self.mod_shift.datefrom_picker.datewidget.date()
    self.mod_shift.showfrom=qnewdatefrom.toPyDate()
    qnewdateto=self.mod_shift.dateto_picker.datewidget.date()
    self.mod_shift.showto=qnewdateto.toPyDate()
    self.mod_shift.tv = gui.ShiftTableView(self, self.mod_shift.showfrom, self.mod_shift.showto)
    self.mod_shift.setCentralWidget(self.mod_shift.tv)


def main(self):
    try:
        self.mod_shift.close()
    except Exception:
        pass

    init_gui(self)


def init_gui(self):
    self.mod_shift = gui.Module(self, "Shift Management")

    act_import = gui.TAction("Import", self.mod_shift.tbar, lambda: import_shifts(self))
    act_load = gui.TAction("Load All", self.mod_shift.tbar, lambda: load_shifts(self))
    act_save = gui.TAction("Save All", self.mod_shift.tbar, lambda: save_shifts(self))
    act_payrates = gui.TAction("Update All Pay Rates", self.mod_shift.tbar, lambda: update_payrates(self))
    act_sort = gui.TAction("Sort", self.mod_shift.tbar, lambda: sort_shifts(self))
    act_refresh = gui.TAction("Refresh", self.mod_shift.tbar, lambda: refresh_view(self))
    act_new = gui.TAction("New Shift", self.mod_shift.tbar, lambda: new_shift(self))
    self.act_filter = gui.TAction("Filter", self.mod_shift.tbar, lambda: filter(self))
    self.act_filter.setCheckable(True)
    self.act_filter.setChecked(False)

    self.mod_shift.addToolBarBreak()
    self.mod_shift.datebar=self.mod_shift.addToolBar("Date Ranges")
    self.mod_shift.datebar.setMovable(False)


    #set the initial values for the two date boxes to : From 56 days ago, To today
    twopayperiods = timedelta(days=56)
    self.mod_shift.showto=QtCore.QDate.currentDate().toPyDate()
    self.mod_shift.showfrom= self.mod_shift.showto - twopayperiods

    # continue with building the gui. Add the two date boxes
    gui.TSpacer(self.mod_shift.datebar)
    self.mod_shift.datefrom_picker = gui.TDatePicker(self, self.mod_shift.datebar, self.mod_shift.showfrom, "From : ")
    self.mod_shift.dateto_picker = gui.TDatePicker(self, self.mod_shift.datebar, self.mod_shift.showto, "To : ")
    gui.TSpacer(self.mod_shift.datebar)

    refresh_view(self)

def filter(self):
    if self.act_filter.isChecked():
        try:
            self.mod_shift.addToolBarBreak()
            self.mod_shift.filterbar = self.mod_shift.addToolBar("Filter")
            self.mod_shift.filterbar.label=QtWidgets.QLabel("Filters not implemented yet")
            self.mod_shift.filterbar.addWidget(self.mod_shift.filterbar.label)
            self.mod_shift.filterbar.setMovable(False)
        except:
            self.logbox.error("Unable to show filter bar")
    else:
        try:
            self.mod_shift.removeToolBar(self.mod_shift.filterbar)
        except:
            self.logbox.error("Unable to remove filter bar")
    return

def insert_shift(self):
    input_date = datetime.strptime(self.newshift_date.text(),'%d/%m/%Y')
    input_start = datetime.strptime(self.newshift_start.text(),'%H:%M')
    input_end = datetime.strptime(self.newshift_end.text(),'%H:%M')
    newshift_start = datetime.combine(input_date.date(),input_start.time())
    newshift_end = datetime.combine(input_date.date(),input_end.time())
    shift_obj=Shift(newshift_start,newshift_end,0)
    self.shiftlist.append(shift_obj)
    self.win_newshift.close()
    refresh_view(self)
def new_shift(self):
    self.win_newshift=QtWidgets.QDialog(self.mod_shift)
    self.win_newshift.setModal(True)
    self.win_newshift.setContentsMargins(0,0,0,0)
    self.win_newshift.setWindowModality(QtCore.Qt.WindowModal)

    newshift_group=QtWidgets.QGroupBox("Add a new shift")
    self.newshift_date=QtWidgets.QDateEdit()
    self.newshift_start=QtWidgets.QTimeEdit()
    self.newshift_end=QtWidgets.QTimeEdit()

    newshift_accept=QtWidgets.QPushButton("Accept")
    newshift_accept.clicked.connect(lambda: insert_shift(self)) #now to get this to update self.shiftlist
    newshift_cancel=QtWidgets.QPushButton("Cancel")
    newshift_cancel.clicked.connect(self.win_newshift.close)
    button_layout=QtWidgets.QHBoxLayout()
    button_layout.setSpacing(20)
    button_layout.addWidget(newshift_accept)
    button_layout.addWidget(newshift_cancel)

    newshift_layout=QtWidgets.QFormLayout()
    newshift_layout.addRow("Date : ",self.newshift_date)
    newshift_layout.addRow("Start Time : ",self.newshift_start)
    newshift_layout.addRow("End Time : ",self.newshift_end)

    win_layout=QtWidgets.QGridLayout()
    win_layout.addWidget(newshift_group,0,0)
    win_layout.addItem(button_layout,1,0)

    newshift_group.setLayout(newshift_layout)
    self.win_newshift.setLayout(win_layout)

    self.win_newshift.show()

def update_payrates(self):
    for _shift in range(len(self.shiftlist)):
        date = self.shiftlist[_shift].start.date()
        for _payrate in range(len(self.payratelist)):
            if date >= self.payratelist[_payrate].datefrom and date <= self.payratelist[_payrate].dateto:
                self.shiftlist[_shift].nightrate = self.payratelist[_payrate].nightrate
                result="Match : " + str(_shift)
            else:
                result="No match"
            print("Checking shift :",date,"PayRate FROM :",self.payratelist[_payrate].datefrom,"TO: ",self.payratelist[_payrate].dateto,"Result :",result)

def import_shifts(self):
    filename=QtWidgets.QFileDialog.getOpenFileName(initialFilter=".csv", directory=".",options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
    if filename:
        self.shiftlist = wagecalc.file.import_shiftlist(filename)
        self.logbox.info("Shifts imported from file")
        refresh_view(self)
def load_shifts(self):
    try:
        return wagecalc.file.load_shiftlist()
    except:
        self.logbox.error("Shifts Failed to Load")
def save_shifts(self):
    try:
        wagecalc.file.save_shiftlist(self.shiftlist)
        self.logbox.info("Shifts Saved")
    except:
        self.logbox.error("Shifts Failed to Save")
def sort_shifts(self):
    if hasattr(self, "shiftlist") and len(self.shiftlist) > 0:
        shiftlist_sorted = sorted(self.shiftlist, key=lambda k: k.start)
        self.shiftlist = shiftlist_sorted
        refresh_view(self)
        self.logbox.info("Data sorted")
    else:
        self.logbox.info("No data to sort")



