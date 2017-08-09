from PyQt5 import QtWidgets,QtGui,QtCore
from datetime import datetime, timedelta
from decimal import Decimal
import wagecalc.file
import gui

from data import PayRate

def refresh_view(self):
    try:
        self.mod_payrate.tv.close()
    except Exception:
        pass
    self.mod_payrate.tv = gui.PayRateTableView(self)
    self.mod_payrate.setCentralWidget(self.mod_payrate.tv)

def main(self):
    init_gui(self)

def init_gui(self):
    self.mod_payrate = gui.Module(self, "Pay Rate Management")
    act_load = gui.TAction("Load", self.mod_payrate.tbar, lambda: load_data_payrate(self))
    act_save = gui.TAction("Save", self.mod_payrate.tbar, lambda: save_data_payrate(self))
    act_new = gui.TAction("New Pay Rate", self.mod_payrate.tbar, lambda: new_payrate(self))
    refresh_view(self)

def insert_payrate(self):
    input_id = int(self.newpayrate_id.text())
    input_datefrom = self.newpayrate_datefrom.date()
    input_dateto = self.newpayrate_dateto.date()
    input_dayrate = Decimal(self.newpayrate_dayrate.text())
    input_nightrate = Decimal(self.newpayrate_nightrate.text())
    input_description = self.newpayrate_description.toPlainText()

    payrate_obj=PayRate(input_id,input_datefrom,input_dateto,input_dayrate,input_nightrate,input_description)
    self.payratelist.append(payrate_obj)
    self.win_newpayrate.close()
    refresh_view(self)

def new_payrate(self):
    self.win_newpayrate=QtWidgets.QDialog(self.mod_payrate)
    self.win_newpayrate.setModal(True)
    self.win_newpayrate.setMinimumWidth(400)
    self.win_newpayrate.setContentsMargins(0,0,0,0)
    self.win_newpayrate.setWindowModality(QtCore.Qt.WindowModal)


    newpayrate_group=QtWidgets.QGroupBox("Add a new Pay Rate")

    self.newpayrate_newid=len(self.payratelist)+1
    self.newpayrate_id=QtWidgets.QLineEdit()
    self.newpayrate_id.setText(str(self.newpayrate_newid))
    self.newpayrate_id.setReadOnly(True)
    self.newpayrate_datefrom=QtWidgets.QDateEdit()
    self.newpayrate_dateto=QtWidgets.QDateEdit()

    self.newpayrate_dayrate=QtWidgets.QLineEdit()
    self.newpayrate_dayrate.setInputMask('00.0000')
    self.newpayrate_dayrate.setAlignment(QtCore.Qt.AlignCenter)

    self.newpayrate_nightrate=QtWidgets.QLineEdit()
    self.newpayrate_nightrate.setInputMask('00.0000')
    self.newpayrate_nightrate.setAlignment(QtCore.Qt.AlignCenter)

    self.newpayrate_description=QtWidgets.QTextEdit()

    newpayrate_accept=QtWidgets.QPushButton("Accept")
    newpayrate_accept.clicked.connect(lambda: insert_payrate(self))
    newpayrate_cancel=QtWidgets.QPushButton("Cancel")
    newpayrate_cancel.clicked.connect(self.win_newpayrate.close)
    button_layout=QtWidgets.QHBoxLayout()
    button_layout.setSpacing(20)
    button_layout.addWidget(newpayrate_accept)
    button_layout.addWidget(newpayrate_cancel)

    newpayrate_layout=QtWidgets.QFormLayout()
    newpayrate_layout.addRow("ID : ", self.newpayrate_id)
    newpayrate_layout.addRow("Date From : ", self.newpayrate_datefrom)
    newpayrate_layout.addRow("Date To : ",self.newpayrate_dateto)
    newpayrate_layout.addRow("Day Rate : ",self.newpayrate_dayrate)
    newpayrate_layout.addRow("Night Rate : ",self.newpayrate_nightrate)
    newpayrate_layout.addRow("Description : ",self.newpayrate_description)

    win_layout=QtWidgets.QGridLayout()
    win_layout.addWidget(newpayrate_group,0,0)
    win_layout.addItem(button_layout,1,0)

    newpayrate_group.setLayout(newpayrate_layout)
    self.win_newpayrate.setLayout(win_layout)
    self.win_newpayrate.show()

def load_data_payrate(self):
    try:
        return wagecalc.file.load_payratelist()
    except:
        self.logbox.error("Pay Rates Failed to Load")

def save_data_payrate(self):
    try:
        wagecalc.file.save_payratelist(self.payratelist)
        self.logbox.info("Pay Rates Saved")
    except:
        self.logbox.error("Pay Rates Failed to Save")