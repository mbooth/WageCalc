from PyQt5 import QtCore, QtGui, QtSql
import inspect
from pprint import pprint
from datetime import datetime

class ShiftTableModel(QtCore.QAbstractTableModel):
    def __init__(self, master, requested_from, requested_to):
        QtCore.QAbstractTableModel.__init__(self)
        self.header_labels = ['Date','Start','End','Total\nLength','Day\nLength','Night\nLength','Unpaid', 'Day Rate', 'Night Rate']
        self.editable_columns = [0,1,2,7,8]

        self.allshifts=master.shiftlist
        self.requested_from=requested_from
        self.requested_to=requested_to
        self.startptr = -99 #dummy value to initiate with because 0 could be a positive match
        self.endptr = -99
        totalshifts=len(master.shiftlist)

        ''' This now loops through all the shifts, and checks the date on every one, to see if it's AFTER
        the user's requested 'from' date '''
        for _ in range(0,totalshifts):
            if master.shiftlist[_].start.date() >= self.requested_from:
                self.startptr = _ # We've found a match for the start shift, we're done with this loop
                break

        if self.startptr > -99: #Only true if a start shift was found
            for _ in range(self.startptr,totalshifts): #loop again from the found start shift
                if master.shiftlist[_].start.date() > self.requested_to:
                    self.endptr = _
                    break
                else:
                    self.endptr = len(master.shiftlist)

        self.grantedshiftlist= self.endptr - self.startptr
    def rowCount(self, master, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self.grantedshiftlist
    def columnCount(self,master,parent=QtCore.QModelIndex()):
        return 9
        # return(len(self.allshifts[0].__dict__))+1 # Add 1 extra column because date doesn't exist in the data yet
        # Commented out in the interim and hardcoded the columns in. The +1 works upon initial load...it creates 5 columns
        # If initiated during an import, then it only creates 4 for some reason (Length is not yet defined?)
        # Changed to a hard 5 so it returns correct in both circumstances...FOR NOW

    def flags(self, index):
        flags=super(self.__class__, self).flags(index)
        if index.column() in self.editable_columns: # only want date, start and end fields to be editable
            flags |= QtCore.Qt.ItemIsEditable
        else: #all other columns not editable, so make them non-selectable (prettier behaviour)
            flags ^= QtCore.Qt.ItemIsSelectable
        return flags

    def setData(self, index: object, value: object, role: object = QtCore.Qt.EditRole) -> object:
        row=index.row()
        col=index.column()
        i = row + self.startptr
        if col == 0: #Date
            try:
                newdate=value.toPyDate()
                self.allshifts[i].start = self.allshifts[i].start.replace(day=newdate.day, month=newdate.month, year=newdate.year)
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 1: #Start
            try:
                newhour=int(value[:2])
                newminute=int(value[3:])
                self.allshifts[i].start = self.allshifts[i].start.replace(hour=newhour,minute=newminute)
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 2: #End
            try:
                newhour=int(value[:2])
                newminute=int(value[3:])
                self.allshifts[i].end = self.allshifts[i].end.replace(hour=newhour,minute=newminute)
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 7: #Day Rate
            try:
                self.allshifts[i].dayrate = value
                self.dataChanged(index)
                return True
            except:
                return False
        elif col == 8: #Night Rate
            try:
                self.allshifts[i].nightrate = value
                self.dataChanged(index)
                return True
            except:
                return False
        else:
            return False
    def data(self, index, role):
        row=index.row()
        col=index.column()
        if role==QtCore.Qt.DisplayRole or role==QtCore.Qt.EditRole:
            i = row + self.startptr
            if col==0: #Date
                return QtCore.QDate(self.allshifts[i].start)
            elif col==1: #Start Time
                return self.allshifts[i].start.strftime('%H:%M')
            elif col==2: #End Time
                return self.allshifts[i].end.strftime('%H:%M')
            elif col==3: #Total Length
                return str(int(self.allshifts[i].length // 60))+":"+str(int(self.allshifts[i].length % 60)).zfill(2)
            elif col==4: #Length during Day
                if self.allshifts[i].length_dayrate > 0:
                    return str(int(self.allshifts[i].length_dayrate // 60))+":"+str(int(self.allshifts[i].length_dayrate % 60)).zfill(2)
                else:
                    return '-'
            elif col==5: #Length during Night
                if self.allshifts[i].length_nightrate > 0:
                    return str(int(self.allshifts[i].length_nightrate // 60))+":"+str(int(self.allshifts[i].length_nightrate % 60)).zfill(2)
                else:
                    return '-'
            elif col==6: #Length Unpaid
                if self.allshifts[i].length_unpaid > 0:
                    return str(int(self.allshifts[i].length_unpaid // 60)) + ":" + str(
                        int(self.allshifts[i].length_unpaid % 60)).zfill(2)
                else:
                    return '-'
            elif col==7: #DAY RATE
                return str(self.allshifts[i].dayrate)
            elif col==8: #NIGHT RATE
                return str(self.allshifts[i].nightrate)

        elif role==QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role==QtCore.Qt.FontRole:
            f=QtGui.QFont
            return f
        elif role==QtCore.Qt.ForegroundRole and index.column() not in self.editable_columns:
            return QtGui.QColor(150,150,150)

    def headerData(self, p_int, Qt_Orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Qt_Orientation == QtCore.Qt.Horizontal:
            return self.header_labels[p_int]
        return QtCore.QAbstractTableModel.headerData(self,p_int, Qt_Orientation,role)

class PayRateTableModel(QtSql.QSqlRelationalTableModel):
    def __init__(self,master):
        QtSql.QSqlRelationalTableModel.__init__(self,db=master.db)
        self.header_labels = ['ID','From','To','Day Rate','Night Rate', 'Description']
        self.editable_columns = [1,2,3,4,5]
        self.setTable('payrates')
        self.setEditStrategy(QtSql.QSqlRelationalTableModel.OnRowChange)
        self.select()

    def columnCount(self,master,parent=QtCore.QModelIndex()):
        return 6

    def flags(self, index):
        flags=super(self.__class__, self).flags(index)
        if index.column() not in self.editable_columns:
            flags ^= QtCore.Qt.ItemIsEditable
        return flags

    def headerData(self, p_int, Qt_Orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Qt_Orientation == QtCore.Qt.Horizontal:
            return self.header_labels[p_int]
        return QtCore.QAbstractTableModel.headerData(self,p_int, Qt_Orientation,role)

    def data(self, index, role):
        row=index.row()
        col=index.column()
        data = super(PayRateTableModel, self).data(index, role)
        if role==QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role==QtCore.Qt.FontRole:
            f=QtGui.QFont
            return f
        elif role==QtCore.Qt.ForegroundRole and index.column() not in self.editable_columns:
            return QtGui.QColor(150,150,150)
        try:
            if (col in [1,2]) and (role==QtCore.Qt.DisplayRole) and data:
                data=super(PayRateTableModel, self).data(index,role)
                year=data[:4]
                month=data[5:7]
                day=data[8:10]
                data=QtCore.QDate(int(year),int(month),int(day)).toString("dd/MM/yyyy")
                return data
            elif col in [3,4] and role ==QtCore.Qt.DisplayRole:
                data=super(PayRateTableModel, self).data(index,role)
                return '%.4f' % data
        except:
            return "Deleted"
        return super(PayRateTableModel, self).data(index,role)

