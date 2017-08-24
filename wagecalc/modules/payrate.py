from PyQt5 import QtWidgets,QtCore, QtSql
import gui, view
from data import PayRate

def refresh_view(self):
    """ Close currently open table view (if applicable) then attach a new table view to Main Window as Central Widget """
    try:
        self.mod_payrate.tv.close()
    except Exception:
        pass
    self.mod_payrate.tv = view.PayRateTableView(self)
    self.mod_payrate.setCentralWidget(self.mod_payrate.tv)

def main(self):
    init_gui(self)

def init_gui(self):
    """ Create the GUI. Create Main Window and Toolbar"""
    self.mod_payrate = gui.Module(self, "Pay Rate Management")
    gui.TAction("Load", self.mod_payrate.tbar, lambda: load_data_payrate(self))
    gui.TAction("Save", self.mod_payrate.tbar, lambda: save_data_payrate(self))
    gui.TAction("New Pay Rate", self.mod_payrate.tbar, lambda: new_payrate(self))
    gui.TAction("Refresh", self.mod_payrate.tbar, lambda: refresh_view(self))

    refresh_view(self)

def convert_payrates(self):
    """ Temp method for importing list payratelist into Database """
    for _ in self.payratelist:
        self.db.insert("INSERT INTO payrates VALUES (?,?,?,?,?,?,?)", (_.id, _.datefrom, _.dateto, _.dayrate, _.nightrate, _.description, 0))
        print(str(_.datefrom))


def insert_payrate(self):
    """ Insert the newly entered data from new_payrate() into the model """

    query = QtSql.QSqlQuery(db=self.db)
    query.prepare("INSERT INTO payrates (datefrom, dateto, dayrate, nightrate, description) "
                  "VALUES (:datefrom, :dateto, :dayrate, :nightrate, :description)")
    query.bindValue(":datefrom", QtCore.QDate.fromString(self.newpayrate_datefrom.text(), 'dd/MM/yyyy')) #Reformat entered date
    query.bindValue(":dateto", QtCore.QDate.fromString(self.newpayrate_dateto.text(), 'dd/MM/yyyy')) #and store in this format
    query.bindValue(":dayrate", float(self.newpayrate_dayrate.text())) #Entered text is a validated string. Convert to actual float
    query.bindValue(":nightrate", float(self.newpayrate_nightrate.text())) #As above
    query.bindValue(":description", self.newpayrate_description.text())
    query.exec_();

    self.win_newpayrate.close()
    refresh_view(self)

def new_payrate(self):
    """ Open window and accept input of values for a new pay rate """

    self.win_newpayrate=QtWidgets.QDialog(self)
    self.win_newpayrate.setWindowModality(QtCore.Qt.WindowModal) #Modal Window
    newpayrate_group=QtWidgets.QGroupBox("Add a new Pay Rate")
    newpayrate_group.setAlignment(4) #Centred

    self.newpayrate_datefrom=QtWidgets.QDateEdit(calendarPopup=True) #Date From, Input Box
    self.newpayrate_dateto=QtWidgets.QDateEdit(calendarPopup=True) #Date To, Input Box

    self.newpayrate_dayrate=gui.InputPayRate() #Day Rate Input
    self.newpayrate_nightrate=gui.InputPayRate() #Night Rate Input
    self.newpayrate_description=QtWidgets.QLineEdit() #Description Input
    self.newpayrate_description.setMinimumWidth(400)

    newpayrate_accept=QtWidgets.QPushButton("Accept")
    newpayrate_accept.clicked.connect(lambda: insert_payrate(self))
    newpayrate_cancel=QtWidgets.QPushButton("Cancel")
    newpayrate_cancel.clicked.connect(self.win_newpayrate.close)
    button_layout=QtWidgets.QHBoxLayout()
    button_layout.setSpacing(100)
    button_layout.addWidget(newpayrate_accept)
    button_layout.addWidget(newpayrate_cancel)

    newpayrate_layout=QtWidgets.QFormLayout()
    newpayrate_layout.addRow("Date From : ", self.newpayrate_datefrom)
    newpayrate_layout.addRow("Date To : ", self.newpayrate_dateto)
    newpayrate_layout.addRow("Day Rate : ", self.newpayrate_dayrate)
    newpayrate_layout.addRow("Night Rate : ", self.newpayrate_nightrate)
    newpayrate_layout.addRow("Description : ", self.newpayrate_description)

    win_layout=QtWidgets.QGridLayout()
    win_layout.addWidget(newpayrate_group,0,0)
    win_layout.addItem(button_layout,1,0)

    newpayrate_group.setLayout(newpayrate_layout)
    self.win_newpayrate.setLayout(win_layout)
    self.win_newpayrate.show()