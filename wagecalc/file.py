import csv
import json
import pickle
from datetime import datetime

from wagecalc.data import Shift


def import_shiftlist(filename):
    """ Import file into list of shift objects"""
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

def load_shiftlist_file(filename="wagecalc/data/shifts.pickle"):
    """ Load shift file and return as list of shift objects"""
    try:
        with open(filename,'rb') as f:
            shifts = pickle.load(f)
        f.close()
        return shifts
    except:
        return

def save_shiftlist_file(shifts, filename="wagecalc/data/shifts.pickle"):
    """ Take list of shift objects and save to file"""
    try:
        with open(filename,'wb') as f:
            pickle.dump(shifts, f)
        f.close()
    except:
        return

def load_payratelist_file(filename="wagecalc/data/payrates.pickle"):
    """ Load payrates file and return as list of payrate objects"""
    try:
        with open(filename,'rb') as f:
            payratelist = pickle.load(f)
        f.close()
        return payratelist
    except:
        return


def save_payratelist(payratelist, filename="wagecalc/data/payrates.pickle"):
    """ Take list of payrate objects and save to file"""
    try:
        with open(filename,'wb') as f:
            pickle.dump(payratelist, f)
        f.close()
    except:
        return

def create_payperiodlist(payperiods, filename="data/payperiods.json"):
    """ Unknown. Was used to generate pay periods, but must be some other code somewhere to go with it"""
    try:
        with open(filename[0],'w') as f:
            json.dump([PayPeriod.__dict__ for PayPeriod in payperiods],f)
        f.close()
        return("Successfully generated pay periods")
    except:
        return("Failed to generate pay periods")