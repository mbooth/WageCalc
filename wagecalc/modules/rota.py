from PyQt5 import QtWidgets,QtGui,QtCore
from datetime import datetime, timedelta
import wagecalc.file
import gui

from data import Shift



def clear_rotalist_view(self):
    try:
        self.mod_rota.tv.close()
    except:
        return
def init_rotalist_view(self):
    self.mod_shift.tv = gui.ShiftTableView(self, self.mod_shift.showfrom, self.mod_shift.showto)
    self.mod_shift.setCentralWidget(self.mod_shift.tv)

def refresh_rotalist_view(self):
    ''' Clears the table on screen (if there is one) then reads the date widgets (from and to),
    and uses those to create a new table'''
    clear_shiftlist_view(self)

    qnewdatefrom=self.mod_shift.datefrom_picker.datewidget.date()
    self.mod_shift.showfrom=qnewdatefrom.toPyDate()
    qnewdateto=self.mod_shift.dateto_picker.datewidget.date()
    self.mod_shift.showto=qnewdateto.toPyDate()

    init_shiftlist_view(self)

def main(self):
    try:
        self.mod_rota.close()
        init_gui(self)
    except:
        init_gui(self)
    # load_rota_data(self)

def init_gui(self):
    self.mod_rota = gui.Module(self, "Rota Management")

def test(self):
    pass

def insert_shift(self):
    input_date = datetime.strptime(self.newshift_date.text(),'%d/%m/%Y')
    input_start = datetime.strptime(self.newshift_start.text(),'%H:%M')
    input_end = datetime.strptime(self.newshift_end.text(),'%H:%M')
    newshift_start = datetime.combine(input_date.date(),input_start.time())
    newshift_end = datetime.combine(input_date.date(),input_end.time())
    shift_obj=Shift(newshift_start,newshift_end,0)
    self.all_shifts.append(shift_obj)
    self.win_newshift.close()
    refresh_shiftlist_view(self)

def new_shift(self):
    self.win_newshift=QtWidgets.QDialog(self.mod_shift)
    self.win_newshift.setModal(True)
    self.win_newshift.setContentsMargins(0,0,0,0)
    self.win_newshift.setWindowModality(QtCore.Qt.WindowModal)

    newshift_group=QtWidgets.QGroupBox("Add a new shift")
    self.newshift_date=QtWidgets.QLineEdit()
    self.newshift_date.setInputMask('00/00/0000')
    self.newshift_date.setAlignment(QtCore.Qt.AlignCenter)
    self.newshift_start=QtWidgets.QLineEdit()
    self.newshift_start.setInputMask('00:00')
    self.newshift_start.setAlignment(QtCore.Qt.AlignCenter)

    self.newshift_end=QtWidgets.QLineEdit()
    self.newshift_end.setInputMask('00:00')
    self.newshift_end.setAlignment(QtCore.Qt.AlignCenter)

    newshift_accept=QtWidgets.QPushButton("Accept")
    newshift_accept.clicked.connect(lambda: insert_shift(self)) #now to get this to update self.all_shifts
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




def import_shift_data(self):
    filename=QtWidgets.QFileDialog.getOpenFileName(initialFilter=".csv", directory=".",options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
    if filename:
        self.all_shifts = wagecalc.file.file_import_shifts(filename)
        self.logbox.info("Shifts imported from file")
        refresh_shiftlist_view(self)
