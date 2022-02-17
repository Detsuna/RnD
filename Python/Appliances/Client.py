from uuid import uuid4
from tkinter import Tk, StringVar
from tkinter.ttk import *

"""
import re

s = ''' name tag:tag "long name" tag:"long tag" '''
for r in re.findall(r'tag:".+?"|".+?"|tag:[\w-]+|[\w-]+', s):
    print(r)
"""

class Appliance():
    def __init__(self, Id=None, Name=None) : 
        self.Id = Id
        self.Name = Name

class Tag():
    def __init__(self, Id=None, Name=None) : 
        self.Id = Id
        self.Name = Name

class Servicing():
    def __init__(self, Id=None, ApplianceId=None, Details=None, Interval=None, Last=None) : 
        self.Id = (Id if Id else str(uuid4()))
        self.ApplianceId = ApplianceId
        self.Details = Details
        self.Interval = Interval
        self.Last = None


class BackEnd() : 
    class ApplianceManagement() : 
        def Search(self, form) : 
            print({k: v for k, v in vars(form).items() if v is not None})
            #(Id if Id else str(uuid4()))
            

    def __init__(self) :
        self.applianceManager = self.ApplianceManagement()

    def Search(self, form) :
        self.applianceManager.Search(form)

class FrontEnd(Frame):
    def __init__(self, *a, **k) :
        super().__init__(*a, **{**{"borderwidth":10}, **k})

        self.searchbox = StringVar()
        self.client = BackEnd()

        self.Render()

    def Render(self) : 
        self.grid(sticky="NSEW")        
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(2, weight=8)

        s = Style(self)
        s.configure("TLabel", font=("Helvetica", 14))
        s.configure("TButton", font=("Helvetica", 14))

        Label(self, text="Appliances").grid(row=0, column=0)
        Separator(self, orient="vertical").grid(row=0, column=1, rowspan=3, sticky="NS", padx=5)
        Separator(self, orient="horizontal").grid(row=1, column=0, columnspan=5, sticky="EW", pady=5)
        
        Entry(self, font=("Helvetica", 14), textvariable=self.searchbox).grid(row=0, column=2, sticky="EW", padx=(20, 0))
   
        Button(self, text="Clear", command=lambda:self.searchbox.set("")).grid(row=0, column=3, padx=(20, 0))
        Button(self, text="Find", command=self.Search).grid(row=0, column=4, padx=(0, 20))
    
    def Search(self, event=None):
        a = Appliance(Name=self.searchbox.get())
        self.client.Search(a)


if __name__ == "__main__" : 
    root = Tk()
    root.wm_title("Appliances")
    root.minsize(1152, 648)
        
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    app = FrontEnd(root)
    app.mainloop()
