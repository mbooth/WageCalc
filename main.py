import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from modules import shift,rota,payperiod,payrate,wage,contract,setup
import gui
from options import APPTITLE,APPHEIGHT,APPWIDTH


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(APPWIDTH, APPHEIGHT)
        self.move(1000, 100)
        self.setWindowTitle(APPTITLE)
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
        self.btn_setup = gui.LargeButton(self.module_selector, text="Setup", command=lambda: self.callback_setup())
        self.module_selector.layout.addStretch()
        self.btn_exit = gui.LargeButton(self.module_selector, text="Exit", command=lambda: self.callback_exit())
        self.logbox = gui.LogBox()
        self.logbox.setFeatures(QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self.logbox)

    def initialise_data(self):
        try:
            self.shiftlist = shift.load_shifts(self)
            self.payratelist = payrate.load_data_payrate(self)
            self.logbox.info("All Data Loaded")
        except Exception:
            self.logbox.error("Not All Data is Loaded")

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

    def callback_setup(self):
        setup.main(self)


    def callback_exit(self):
        print("Exiting " + str(APPTITLE))
        exit()


application=QtWidgets.QApplication(sys.argv)
