from datetime import datetime

class Shift(object):
    def __init__(self,dictionary):
        ''' This was initially written to open my own test file of data (formatted differently)
        We did not know if all fields were present, so had to iterate over all available fields in each line
        rather than pass in and define each each field by name'''
        for key in dictionary:
            setattr(self,key,dictionary[key])
    # def to_tuple(string):
    #     ''' created to assist in loading from self-made test data. No longer needed (170115)
    #     but leaving here for the time being'''
    #     return time.strptime(string, "%Y%m%d%H%M")

    def calc_length(self):
        '''TODO: Add validation : Including same day, time formats etc
        '''
        startobj = datetime.strptime(self.start, "%H:%M")
        endobj = datetime.strptime(self.end, "%H:%M")
        diffobj = (endobj-startobj)
        self.length = diffobj.seconds/60
        return self.length

    def commit_shift(self, app, edit_window, editable_fields, curItem, *args, **kwargs):
        '''Commits changes made when editing a single shift, back to the main shift list in memory
        and also reflected in the main window display'''
        entry_date=editable_fields[0]
        entry_start=editable_fields[1]
        entry_end=editable_fields[2]
        self.date=entry_date.get()
        self.start=entry_start.get()
        self.end=entry_end.get()
        self.length=self.calc_length()

        #update the treeview from the object
        app.tv.set(curItem, column='date', value=self.date)
        app.tv.set(curItem, column='start', value=self.start)
        app.tv.set(curItem, column='end', value=self.end)
        app.tv.set(curItem, column='length', value=self.length)
        edit_window.destroy()


        #shift_dict is required to be passed back, so the data can be updated in memory. Currently it only updates the treeview
        #ie the display. It does not affect the all_shifts list in memory, so a refresh will undo any changes
        shift_dict = {"ref": self.ref, "date": self.date, "start": self.start,
                      "end": self.end, "length": self.length}
4
        app.sbar.config(text="Data edited")
        return self