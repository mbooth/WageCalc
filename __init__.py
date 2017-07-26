import os
import sys
import wagecalc.file
from main import application
from main import App

if __name__ == '__main__':
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    # app.all_shifts = wagecalc.file.loadshifts() # Put in while developing. Easier than importing manually every time
    # app.mainloop()
    win_main = App()
    font=win_main.font()

    # for name in dir(font):
    #     try:
    #         myvalue = eval(name)
    #     except:
    #         myvalue = "NOT SET"
    #     print(name, "is", type(name), "and is equal to ", myvalue)

    sys.exit(application.exec_())


