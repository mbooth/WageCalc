from datetime import datetime
import sqlite3

DAYSTART = datetime.strptime("06:00","%H:%M")
NIGHTSTART = datetime.strptime("22:00","%H:%M")

class PayRate(object):
    def __init__(self, id, datefrom, dateto, dayrate, nightrate, description=""):
        self.id = id
        self.datefrom = datefrom
        self.dateto = dateto
        self.dayrate = dayrate
        self.nightrate = nightrate
        self.description = description


class ShiftList(list):
    def insertshift(self):
        return

class Shift(object):
    def __init__(self, start, end): #start and end are two datetime objects
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

    # @property
    # def pay(self):
    #     return (self.length_dayrate/60 * DAYRATE) + (self.length_nightrate/60 * NIGHTRATE)


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
        for shift in master.shiftlist:
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
