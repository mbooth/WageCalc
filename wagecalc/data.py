from datetime import datetime, timedelta
from PyQt5 import QtCore,QtGui,QtWidgets
from wagecalc.options import DAYRATE, NIGHTRATE, SLRATE, DAYSTART, NIGHTSTART

class PayRate(object):
    def __init__(self, id, datefrom, dateto, dayrate, nightrate, description=""):
        self.id = id
        self.datefrom = datefrom
        self.dateto = dateto
        self.dayrate = dayrate
        self.nightrate = nightrate
        self.description = description
class PayRateTableModel(QtCore.QAbstractTableModel):
    def __init__(self,master):
        QtCore.QAbstractTableModel.__init__(self)
        self.header_labels = ['ID','From','To','Day Rate','Night Rate', 'Description']
        self.payrates = master.payrates
    def rowCount(self, master, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.payrates)
    def columnCount(self,master,parent=QtCore.QModelIndex()):
        return 6
    def flags(self, index):
        flags=super(self.__class__, self).flags(index)
        if index.column() in [1,2,3,4,5]:
            flags |= QtCore.Qt.ItemIsEditable
        return flags
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row=index.row()
        col=index.column()
        i = row
        if col == 1:
            try:
                self.payrates[i].datefrom = value.toPyDate()
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 2:
            try:
                self.payrates[i].dateto = value.toPyDate()
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 3:
            try:
                newrate=float(value)
                self.payrates[i].dayrate = newrate
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 4:
            try:
                newrate=float(value)
                self.payrates[i].nightrate = newrate
                self.dataChanged(index)
                return True
            except:
                return False
        elif col == 5:
            try:
                newdescription=str(value)
                self.payrates[i].description = newdescription
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
            i = row
            if col==0:
                return self.payrates[i].id
            elif col==1:
                return QtCore.QDate(self.payrates[i].datefrom)
            elif col==2:
                return QtCore.QDate(self.payrates[i].dateto)
            elif col==3:
                return "%7.4f" % self.payrates[i].dayrate
            elif col==4:
                return "%7.4f" % self.payrates[i].nightrate
            elif col==5:
                # return getattr(self.payrates[i], 'description', '')
                return self.payrates[i].description
        elif role==QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role==QtCore.Qt.FontRole:
            f=QtGui.QFont
            return f
    def headerData(self, p_int, Qt_Orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Qt_Orientation == QtCore.Qt.Horizontal:
            return self.header_labels[p_int]
        return QtCore.QAbstractTableModel.headerData(self,p_int, Qt_Orientation,role)

class Shift(object):
    def __init__(self, start, end, length): #start and end are two datetime objects
        self.start = start
        self.end = end

    @property
    def length_unpaid(self):
        return 0

    @property
    def length_nightrate(self):
        if self.start.time() < DAYSTART.time(): #shift starts during NIGHTRATE
            return (DAYSTART - self.start).seconds / 60
        else:
            return 0

    @property
    def length_dayrate(self):
        if self.start.time() >= DAYSTART.time(): #shift starts during DAYRATE
            minutes = (self.end - self.start).seconds / 60 #assumes ALL is at DAYRATE
            return minutes
        elif self.start.time() < DAYSTART.time(): #shift starts during NIGHTRATE
            minutes = (self.end - DAYSTART).seconds / 60
            return minutes
        else:
            return 0 #just incase

    @property
    def length(self):
        minutes = (self.end-self.start).seconds / 60
        return minutes

    @property
    def pay(self):
        return (self.length_dayrate/60 * DAYRATE) + (self.length_nightrate/60 * NIGHTRATE)
class ShiftTableModel(QtCore.QAbstractTableModel):
    def __init__(self, master, requested_from, requested_to):
        QtCore.QAbstractTableModel.__init__(self)
        self.header_labels = ['Date','Start','End','Length','Day Length','Night length','Unpaid', 'Day Rate', 'Night Rate']
        self.allshifts=master.all_shifts
        self.requested_from=requested_from
        self.requested_to=requested_to
        self.startptr = -99 #dummy value to initiate with because 0 could be a positive match
        self.endptr = -99
        totalshifts=len(master.all_shifts)

        ''' This now loops through all the shifts, and checks the date on every one, to see if it's AFTER
        the user's requested 'from' date '''
        for _ in range(0,totalshifts):
            if master.all_shifts[_].start.date() >= self.requested_from:
                self.startptr = _ # We've found a match for the start shift, we're done with this loop
                break

        if self.startptr > -99: #Only true if a start shift was found
            for _ in range(self.startptr,totalshifts): #loop again from the found start shift
                if master.all_shifts[_].start.date() > self.requested_to:
                    self.endptr = _
                    break
                else:
                    self.endptr = len(master.all_shifts)

        self.grantedall_shifts= self.endptr - self.startptr
    def rowCount(self, master, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self.grantedall_shifts
    def columnCount(self,master,parent=QtCore.QModelIndex()):
        return 9
        # return(len(self.allshifts[0].__dict__))+1 # Add 1 extra column because date doesn't exist in the data yet
        # Commented out in the interim and hardcoded the columns in. The +1 works upon initial load...it creates 5 columns
        # If initiated during an import, then it only creates 4 for some reason (Length is not yet defined?)
        # Changed to a hard 5 so it returns correct in both circumstances...FOR NOW

    def flags(self, index):
        flags=super(self.__class__, self).flags(index)
        if index.column() in [0,1,2,7,8]: # only want date, start and end fields to be editable
            flags |= QtCore.Qt.ItemIsEditable
        return flags
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row=index.row()
        col=index.column()
        i = row + self.startptr
        if col == 0:
            try:
                newday=int(value[:2])
                newmonth=int(value[3:5])
                newyear=int(value[6:])+2000
                self.allshifts[i].start = self.allshifts[i].start.replace(day=newday,month=newmonth,year=newyear)
                self.allshifts[i].start.replace()
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 1:
            try:
                newhour=int(value[:2])
                newminute=int(value[3:])
                self.allshifts[i].start = self.allshifts[i].start.replace(hour=newhour,minute=newminute)
                self.dataChanged(index)
                return True
            except:
                return False

        elif col == 2:
            try:
                newhour=int(value[:2])
                newminute=int(value[3:])
                self.allshifts[i].end = self.allshifts[i].end.replace(hour=newhour,minute=newminute)
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
            if col==0: #DATE
                return self.allshifts[i].start.strftime('%d/%m/%y')
            elif col==1: #START TIME
                return self.allshifts[i].start.strftime('%H:%M')
            elif col==2: #END TIME
                return self.allshifts[i].end.strftime('%H:%M')
            elif col==3: #TOTAL LENGTH
                # hh=self.allshifts[i].length // 60
                # mm=self.allshifts[i].length % 60
                return str(int(self.allshifts[i].length // 60))+":"+str(int(self.allshifts[i].length % 60)).zfill(2)
            elif col==4: #LENGTH AT DAY RATE
                if self.allshifts[i].length_dayrate > 0:
                    return str(int(self.allshifts[i].length_dayrate // 60))+":"+str(int(self.allshifts[i].length_dayrate % 60)).zfill(2)
                else:
                    return '-'
            elif col==5: #LENGTH AT NIGHT RATE
                if self.allshifts[i].length_nightrate > 0:
                    return str(int(self.allshifts[i].length_nightrate // 60))+":"+str(int(self.allshifts[i].length_nightrate % 60)).zfill(2)
                else:
                    return '-'
            elif col==6: #UNPAID
                if self.allshifts[i].length_unpaid > 0:
                    return str(int(self.allshifts[i].length_unpaid // 60)) + ":" + str(
                        int(self.allshifts[i].length_unpaid % 60)).zfill(2)
                else:
                    return '-'
            elif col==7: #DAY RATE
                return 'DR'
            elif col==8: #NIGHT RATE
                return 'NR'

        elif role==QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role==QtCore.Qt.FontRole:
            f=QtGui.QFont
            return f
    def headerData(self, p_int, Qt_Orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and Qt_Orientation == QtCore.Qt.Horizontal:
            return self.header_labels[p_int]
        return QtCore.QAbstractTableModel.headerData(self,p_int, Qt_Orientation,role)

class RotaWeek(object):
    def __init__(self,year,weeknum):
        self.year=year
        self.week=weeknum
        self.days=[]
        self.days[0]=RotaDay('Sunday','00:00','00:00',daytype='OFF')
        self.days[1]=RotaDay('Monday','00:00','00:00',daytype='OFF')
        self.days[2]=RotaDay('Tuesday','00:00','00:00',daytype='OFF')
        self.days[3]=RotaDay('Wednesday','00:00','00:00',daytype='OFF')
        self.days[4]=RotaDay('Thursday','00:00','00:00',daytype='OFF')
        self.days[5]=RotaDay('Friday','00:00','00:00',daytype='OFF')
        self.days[6]=RotaDay('Saturday','00:00','00:00',daytype='OFF')
class RotaDay(object):
    def __init__(self,day,start,end,type):
        self.day = day
        self.start = start
        self.end = end
        self.type = type
        # self.length = self.calclength()
class PayPeriod(object):
    def __init__(self,master,paydate,payfrom,payto):
        # ''' Class for a single Pay Period, currently only three fields :
        # 1 : An identifier (date), 2 : A start date (date), 3 : An end date (date)
        # Could add in attributes like tax bracket, total hours etc, pay rates for each pay period?
        # (although how would you deal with multiple pay rates over one period.'''
        # for key in dictionary:
        #     ''' This just loops through all the keys in the dictionary that is passed in, creating attributes for each
        #     one, this allows us to add in extra attributes later without refactoring'''
        #     setattr(self,key,dictionary[key])
        self.paydate = str(paydate)
        self.payfrom = str(payfrom)
        self.payto = str(payto)


    def calc_pay(self):
        for shift in master.all_shifts:
            print(shift)

class Contract(object):
    def __init__(self):
        self.sat=Shift((datetime.time(hour=4,minute=30),datetime.time(hour=12,minute=0)))
        self.sun=False
        self.mon=(datetime.time(hour=4,minute=30),datetime.time(hour=12,minute=0))
        self.tue=(datetime.time(hour=13,minute=00),datetime.time(hour=22,minute=0))
        self.wed=False
        self.thu=(datetime.time(hour=4,minute=30),datetime.time(hour=12,minute=0))
        self.fri=(datetime.time(hour=4,minute=30),datetime.time(hour=12,minute=0))
