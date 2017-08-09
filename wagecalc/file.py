from PyQt5.QtWidgets import QFileDialog
import csv
import json
import pickle
from wagecalc.data import Shift
from wagecalc.data import PayRate
from wagecalc.data import PayPeriod
from datetime import datetime
from datetime import date

def import_shiftlist(filename):
    shiftlist = []
    with open(filename,'r') as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        ref = 0
        next(lines)
        for fields in lines:
            shift_line = {
                "start": datetime.strptime(fields[1], '%d/%m/%Y %H:%M'),
                "end": datetime.strptime(fields[2], '%d/%m/%Y %H:%M'),
            }
            shift_obj=Shift(shift_line['start'],shift_line['end'],0)
            shiftlist.append(shift_obj)
    f.close()
    return shiftlist

def load_shiftlist(filename="wagecalc/data/shifts.pickle"):
    try:
        with open(filename,'rb') as f:
            shifts = pickle.load(f)
        f.close()
        return shifts
    except:
        return

def save_shiftlist(shifts, filename="wagecalc/data/shifts.pickle"):
    try:
        with open(filename,'wb') as f:
            pickle.dump(shifts, f)
        f.close()
    except:
        return

def load_payratelist(filename="wagecalc/data/payrates.pickle"):
    #manually creating payratelist here for now, will get to adding the gui and proper table / list / storage later

    # dt08a=date(2008,1,1)
    # dt08b=date(2008,12,31)
    # dt09a=date(2009,1,1)
    # dt09b=date(2009,12,31)
    # dt10a=date(2010,1,1)
    # dt10b=date(2010,12,31)
    # dt11a=date(2011,1,1)
    # dt11b=date(2011,12,31)
    # dt12a=date(2012,1,1)
    # dt12b=date(2012,12,31)
    # dt13a=date(2013,1,1)
    # dt13b=date(2013,12,31)
    # dt14a=date(2014,1,1)
    # dt14b=date(2014,12,31)
    # dt15a=date(2015,1,1)
    # dt15b=date(2015,12,31)
    # dt16a=date(2016,1,1)
    # dt16b=date(2016,12,31)
    # dt17a=date(2017,1,1)
    # dt17b=date(2017,12,31)
    #
    # payrate08=PayRate(1,dt08a,dt08b,7.08,9.08)
    # payrate09=PayRate(2,dt09a,dt09b,7.09,9.09)
    # payrate10=PayRate(3,dt10a,dt10b,7.10,9.10, True)
    # payrate11=PayRate(4,dt11a,dt11b,7.11,9.11)
    # payrate12=PayRate(5,dt12a,dt12b,7.12,9.12)
    # payrate13=PayRate(6,dt13a,dt13b,7.13,9.13)
    # payrate14=PayRate(7,dt14a,dt14b,7.14,9.14)
    # payrate15=PayRate(8,dt15a,dt15b,7.15,9.15)
    # payrate16=PayRate(9,dt16a,dt16b,7.16,9.16)
    # payrate17=PayRate(10,dt17a,dt17b,7.4407,9.4802)
    #
    # payratelist=[]
    #
    # payratelist.append(payrate08)
    # payratelist.append(payrate09)
    # payratelist.append(payrate10)
    # payratelist.append(payrate11)
    # payratelist.append(payrate12)
    # payratelist.append(payrate13)
    # payratelist.append(payrate14)
    # payratelist.append(payrate15)
    # payratelist.append(payrate16)
    # payratelist.append(payrate17)
    # return payratelist
    try:
        with open(filename,'rb') as f:
            payratelist = pickle.load(f)
        f.close()
        return payratelist
    except:
        return


def save_payratelist(payratelist, filename="wagecalc/data/payrates.pickle"):
    try:
        with open(filename,'wb') as f:
            pickle.dump(payratelist, f)
        f.close()
    except:
        return

def load_payperiodlist():
    pass

def create_payperiodlist(payperiods, filename="data/payperiods.json"):
    try:
        with open(filename[0],'w') as f:
            json.dump([PayPeriod.__dict__ for PayPeriod in payperiods],f)
        f.close()
        return("Successfully generated pay periods")
    except:
        return("Failed to generate pay periods")