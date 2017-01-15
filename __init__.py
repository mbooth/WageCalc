import os
import tkinter
from tkinter import ttk
from datetime import datetime
from wagecalc import data
import wagecalc.file
from wagecalc.gui import EditBox,Button,StatusBar,ToolBar,Window,Menu
from wagecalc.options import app_title,app_width,app_height
from wagecalc.data import Shift


class App(tkinter.Tk):
    def __init__(self, master):
        tkinter.Tk.__init__(self)
        frame=tkinter.Frame(self).pack()
        master.wm_title(app_title)
        master.geometry(
            "%dx%d+%d+%d" % (app_width, app_height, ((-app_width) - (app_width)),
                             (master.winfo_screenheight() / 2) - (app_height / 2)))
        # master.geometry(
        #     "%dx%d+%d+%d" % (app_width, app_height, ((master.winfo_screenwidth() / 2) - (app_width / 2)),
        #                      (master.winfo_screenheight() / 2) - (app_height / 2)))
        # temporarily changed the above while developing to show app on second monitor instead of over pycharm

        #Menus
        self.menubar=Menu(master)
        self.menu_file=Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.menu_file)
        self.menu_file.add_command(label="Import", command=self.importCB)
        self.menu_file.add_command(label="Load",command=self.loadCB)
        self.menu_file.add_command(label="Exit",command=self.exitCB)

        self.menu_edit=Menu(self.menubar)
        self.menubar.add_cascade(label="Edit",menu=self.menu_edit)
        self.menu_edit.add_command(label="Edit Entry",command=self.editCB)

        master.config(menu=self.menubar)

        #Toolbar
        self.tbar = ToolBar(frame)
        self.btn_import = Button(self.tbar, text="Import", command=lambda: self.importCB()).pack(side="left")
        self.btn_load = Button(self.tbar, text="Load", command=lambda: self.loadCB()).pack(side="left")
        self.btn_save = Button(self.tbar, text="Save", command=lambda: self.saveCB()).pack(side="left")
        self.btn_refresh = Button(self.tbar, text="Refresh", command=lambda: self.refreshCB()).pack(side="left")
        self.btn_sort = Button(self.tbar, text="Sort", command=lambda: self.sortCB()).pack(side="left")
        self.btn_edit = Button(self.tbar, text="Edit", command=lambda: self.editCB()).pack(side="left")
        self.btn_exit = Button(self.tbar, text="Exit", command=lambda: self.exitCB()).pack(side="right",anchor="e")

        #Statusbar
        self.sbar = StatusBar(frame, text="Program ready")
        #Main Display of Shifts (Treeview)
        self.main = tkinter.Frame(frame, relief="flat")
        self.main.pack()
        self.tvstyle = ttk.Style()
        self.tvstyle.configure('Treeview', borderwidth=0, relief="flat")
        self.tv = ttk.Treeview(self.main, height=30, columns=("ref", "date", "start", "end", "length"),
                               show="headings")
        self.tv.heading('ref', text="Ref")
        self.tv.heading('date', text="Date")
        self.tv.heading('start', text="Start")
        self.tv.heading('end', text="End")
        self.tv.heading('length', text="Length")
        self.tv.column('ref', width=65, minwidth=65, anchor="center", stretch="true")
        self.tv.column('date', width=100, anchor="center", stretch="true")
        self.tv.column('start', width=60, anchor="center", stretch="true")
        self.tv.column('end', width=60, anchor="center", stretch="true")
        self.tv.column('length', width=60, anchor="center", stretch="true")
        self.tv.bind('<Double-1>', lambda x: self.editCB())
        self.tv.configure()
        self.tv.grid(row=0, column=0)

    def clear_all_data(self):
        try:
            del self.all_shifts
        except:
            return
    def clear_display(self):
        self.tv.delete(*self.tv.get_children())
    def show_display(self):
        for shift in range(0,len(self.all_shifts),1):
            ref = self.all_shifts[shift]['ref']
            date = self.all_shifts[shift]['date']
            start = self.all_shifts[shift]['start']
            end = self.all_shifts[shift]['end']
            length = self.all_shifts[shift]['length']
            self.tv.insert('','end',values=(self.all_shifts[shift]['ref'],date,start,end,length))

    def importCB(self):
        self.clear_all_data()
        self.clear_display()
        try:
            self.all_shifts = wagecalc.file.import_data()
        except:
             self.sbar.newtext("Import Failed")
        try:
            self.all_shifts = wagecalc.data.calc_all_lengths(self.all_shifts)
            self.show_display()
        except:
             self.sbar.newtext("Calculating Lengths Failed")

    def loadCB(self):
        self.sbar.newtext("'Load' Not implemented")
    def editCB(self):
        #try to read the selected item in the treeview, or return an error
        try:
            curshift_item = self.tv.focus()
            curshift_values = self.tv.item(curshift_item)['values']
            curshift_ref=curshift_values[0]
        except:
            self.sbar.newtext("No entry selected")
            return
        #create shift object with values in the selected item
        curshift = Shift({"ref" : curshift_values[0],"date" : curshift_values[1],"start" : curshift_values[2], "end" : curshift_values[3]})

        ''' TODO : Tidy the below code up. Automatically create status bar and toolbar when the window is created instead of separately.
        Do this in the wagecalc.gui.Window class instead'''
        self.edit_window = Window(app,title="Edit Shift : Ref #" + str(curshift.ref))
        print(dir(self.edit_window))
        self.edit_toolbar = ToolBar(self.edit_window)
        self.edit_statusbar = StatusBar(self.edit_window,text="Edit the data then click SAVE")

        #create the entry boxes
        self.edit_date = EditBox(self.edit_window,text="Date")
        self.edit_start = EditBox(self.edit_window,text="Start")
        self.edit_end = EditBox(self.edit_window,text="End")

        #populate the entry boxes with current values of selected item
        self.edit_date.value.insert(0,curshift.date)
        self.edit_start.value.insert(0,curshift.start)
        self.edit_end.value.insert(0,curshift.end)

        #create and pass a list of the three entry boxes to the btn_save command
        self.editable_fields=[self.edit_date,self.edit_start,self.edit_end]
        self.btn_save = Button(self.edit_toolbar, text="Save", side="left", command=lambda: curshift.commit_shift(app, self.edit_window, self.editable_fields, curshift_item))
        self.btn_cancel = Button(self.edit_toolbar,text="Cancel", side="right",command=lambda: self.edit_window.destroy())
    def sortCB(self):
        ''' currently sorts the list holding all the dictionaries, then refreshes the treeview
        Note : Does not sort the treeview elements specifically'''
        self.clear_display()
        if hasattr(self, "all_shifts") and len(self.all_shifts) > 0:
            self.sbar.newtext("Sorting Data")
            all_shifts_sorted = sorted(app.all_shifts, key=lambda k: k['ref'])
            self.all_shifts=all_shifts_sorted
            self.sbar.newtext("Data sorted")
            self.show_display()
        else:
            self.sbar.newtext("Sorting failed. Has the data been loaded?")
    def saveCB(self):
        self.sbar.newtext("'Save' Not implemented")
    def refreshCB(self):
        try:
            self.clear_display()
            self.show_display()
            self.sbar.newtext("Data refreshed")
        except:
            self.sbar.newtext("Failed to refresh")
    def exitCB(self):
        exit()

def donothing():
    pass

if __name__ == '__main__':
    root=tkinter.Tk()
    app=App(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    app.clear_all_data()
    app.clear_display()
    app.all_shifts = wagecalc.file.import_data()
    app.show_display()
    app.mainloop()
    try:
        app.destroy()
    except:
        pass

