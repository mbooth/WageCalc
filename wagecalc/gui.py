import logging
from PyQt5 import QtWidgets, QtCore, QtGui


class PayRateValidator(QtGui.QDoubleValidator):
    def __init__(self):
        QtGui.QDoubleValidator.__init__(self, 0.0001,9999.999999, 4)

class InputPayRate(QtWidgets.QLineEdit):
    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)
        self.setValidator(QtGui.QDoubleValidator(0.0001,9999.999999, 4))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("00.0000")
        self.textChanged.connect(self.check_state)
        self.textChanged.emit(self.text())

    def check_state(self, *args, **kwargs):
        validator = self.validator()
        state = validator.validate(self.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'  # green
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a'  # yellow
        else:
            color = '#f6989d'  # red
        self.setStyleSheet('QLineEdit { background-color: %s }' % color)
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
