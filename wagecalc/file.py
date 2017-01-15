from tkinter import filedialog
import csv
from wagecalc.data import Shift

def import_data(filename="hourstracker.csv"):
    # source data is from Hours Tracker App, so we have a specific format to read from. Makes things easier/predictable
    # filename=filedialog.askopenfilename()
    all_shifts = []
    with open(filename,'r') as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        ref = 0
        next(lines)
        for row in lines:
            ref += 1
            shift_line = {
                "ref": ref,
                "date": row[1][:10],
                "start": row[1][11:],
                "end": row[2][11:],
                # calculate length of shift here at import time, or later (outside of this loop)?
                # now would be cleaner?
            }
            shift_obj=Shift(shift_line)
            shift_length=shift_obj.calc_length()
            shift_line['length'] = shift_length
            all_shifts.append(shift_line)
    f.close()
    return all_shifts


# Old functions to to read/write data from my own text file storage. Replaced by an improved import, direct from Hours Tracker file
# def import_data():
#     all_shifts=read_all()
#     return all_shifts
# def read_all(): #reads the whole file into a list called 'all_shifts'
#     all_shifts=[]
#     shift={'ref' : '',
#            'date' : '',
#            'start' : '',
#            'finish' : '',
#            'length' : ''
#         }
#     with open("hourstracker.csv", "r+") as f:
#         lines = csv.reader(f,delimiter=',',quotechar='"')
#         ref=0
#         next(lines)
#         for row in lines: #iterate over each line
#             ref+=1
#             one_shift = {
#                 "ref"   : ref,
#                 "date"  : row[1][:10],
#                 "start" : row[1][12:],
#                 "end": row[2][12:]
#             }
#             all_shifts.append(one_shift)
#     f.close()
#     return all_shifts
# def write_all():
#     with open("data.txt","w") as f:
#         for shift in all_shifts:
#             f.write(str(shift["start"]) + " " + str(shift["finish"]))
#             if len(shift)==3:
#                 f.write(" " + str(shift["total"]))
#             f.write("\n")
#     f.close()

