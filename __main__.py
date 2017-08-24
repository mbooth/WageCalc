import os
import sys
from PyQt5 import QtCore,QtGui,QtWidgets, QtSql

import database
from modules import shift,rota,payperiod,payrate,wage,contract
import gui
import file
from pprint import pprint
import traceback

class WageCalcApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 1200)
        self.move(800, 100)
        self.setWindowTitle("Wage Calculator")
        self.create_gui()
        self.show()
        self.setStyle(QtWidgets.QStyleFactory.create('Macintosh'))
        self.initialise_data()

    def create_gui(self):
        self.main=QtWidgets.QMdiArea()
        self.main.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.setCentralWidget(self.main)
        self.module_selector=QtWidgets.QDockWidget("Module Selector")
        self.module_selector.setFixedWidth(150)
        self.module_selector.setFloating(False)
        self.module_selector.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.module_selector.frame = QtWidgets.QFrame()
        self.module_selector.layout = QtWidgets.QVBoxLayout()
        self.module_selector.frame.setLayout(self.module_selector.layout)
        self.module_selector.setWidget(self.module_selector.frame)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.module_selector)

        self.btn_shift= gui.LargeButton(self.module_selector, text="Shifts", command=lambda: self.callback_shift())
        self.btn_rota = gui.LargeButton(self.module_selector, text="Rotas", command=lambda: self.callback_rota())
        self.btn_wage = gui.LargeButton(self.module_selector, text="Wages", command=lambda: self.callback_wage())
        self.btn_payperiod = gui.LargeButton(self.module_selector, text="Pay Periods", command=lambda: self.callback_payperiod())
        self.btn_contract = gui.LargeButton(self.module_selector, text="Contract", command=lambda: self.callback_contract())
        self.btn_payrate = gui.LargeButton(self.module_selector, text="Pay Rates", command=lambda: self.callback_payrate())
        self.module_selector.layout.addStretch()
        self.btn_exit = gui.LargeButton(self.module_selector, text="Exit", command=lambda: self.callback_exit())
        self.logbox = gui.LogBox()
        self.logbox.setFeatures(QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self.logbox)

    def initialise_data(self):
        try:
            self.shiftlist = shift.load_shifts(self)
            self.logbox.info("All Data Loaded")
        except Exception:
            self.logbox.error("Not All Data is Loaded")

        self.db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('wagecalc/data/wagecalc.db')

        if self.db.isValid():
            self.logbox.info("Database is Valid")
        else:
            self.logbox.error("Database is not Valid")
        if not self.db.open():
            self.logbox.error("Could not open database.")
            self.logbox.error("Text: " + self.db.lastError().text())
            self.logbox.error("Type: " + str(self.db.lastError().type()))
            self.logbox.error("Number: " + str(self.db.lastError().number()))

    def callback_shift(self):
        shift.main(self)

    def callback_rota(self):
        rota.main(self)

    def callback_wage(self):
        wage.main(self)

    def callback_payperiod(self):
        payperiod.main(self)

    def callback_contract(self):
        contract.main(self)

    def callback_payrate(self):
        payrate.main(self)

    def callback_exit(self):
        database.close_db(self)
        print("Exiting")
        exit()


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    app = WageCalcApp()
    font=app.font()
    application.exec()
