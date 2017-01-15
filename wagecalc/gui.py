import tkinter
class EditBox(object):
    def __init__(self,parent,text="Text : "):
        edit_frame=tkinter.Frame(parent)
        edit_frame.pack(fill="x")
        edit_col0=tkinter.Frame(edit_frame)
        edit_col0.grid(column=0,row=0, sticky="e")
        edit_col1=tkinter.Frame(edit_frame)
        edit_col1.grid(column=1,row=0, sticky="w")
        edit_frame.columnconfigure(0,weight=2, uniform="group1")
        edit_frame.columnconfigure(1,weight=5, uniform="group1")
        self.text = tkinter.Label(edit_col0,text=text + " :")
        self.text.pack(side="right")
        self.value = tkinter.Entry(edit_col1)
        self.value.pack(side="left")

    def get(self):
        text=tkinter.Entry.get(self.value)
        return text
class Button(tkinter.Button):
    def __init__(self,parent,command,side="left",text="****"):
        tkinter.Button.__init__(self, parent, text=text, command=command)
        tkinter.Button.pack(self,side=side, anchor="n")
class ToolBar(tkinter.Frame):
    def __init__(self,parent):
        tkinter.Frame.__init__(self,parent,relief="raised",borderwidth=1)
        tkinter.Frame.pack(self,side="top", fill="both",padx=5, pady=5)
class StatusBar(tkinter.Label):
    def __init__(self,parent,text="..."):
        tkinter.Label.__init__(self, parent,text=text,borderwidth=1,relief="flat",background="#e9e9e9")
        tkinter.Label.pack(self,side="bottom", fill="both")
    def newtext(self,text="Default text"):
        self.config(text=text)
class Menu(tkinter.Menu):
    def __init__(self,parent,*args,**kwargs):
        tkinter.Menu.__init__(self,parent,tearoff=0)
class Window(tkinter.Toplevel):
    def __init__(self,parent,width=400,height=300,title="Default"):
        tkinter.Toplevel.__init__(self,parent)
        # self.geometry("%dx%d+%d+%d" % (width, height, ((parent.winfo_screenwidth() / 2) - (width / 2)),
        #                                (parent.winfo_screenheight() / 2) - (height / 2)))
        # changed the above temporarily to show window on screen 2, near main app for ease of testingw
        self.geometry("%dx%d+%d+%d" % (width, height, -width,
                             (parent.winfo_screenheight() / 2) - (height / 2)))
        self.title(title)



