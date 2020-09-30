import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import DatasetCleanerMain
import sys

class CleanApp(tk.Frame):
    
    # Variables
    filename = None
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        # Get file button
        self.getFile = tk.Button(self, text="Load File", command=lambda: self.GetFile())
        self.getFile.grid(row=0, column=0, ipadx=35, ipady=10)
        
        # Is the data for Regression Checkbox
        self.isRegression = tk.IntVar()
        self.labelIsRegression = tk.Checkbutton(self, text = "Clean for Regression", variable=self.isRegression)
        self.labelIsRegression.grid(row=1, column=0, ipadx=5, ipady=5)
        
        # Get seperator
        self.entrySeperatorString = tk.StringVar()
        self.label1 = tk.Label(self, text="Seperator character:")
        self.label1.grid(row=2, column=0)
        self.entrySeperator = tk.Entry(self, bd=1, textvariable=self.entrySeperatorString)
        self.entrySeperator.grid(row=3, column=0)
        
        self.startCleaning = tk.Button(self, text = "Start Cleaning Dataset", command=lambda: self.StartCleaning())
        self.startCleaning.grid(row=0, column=1, ipadx=10, ipady=55, rowspan=4)
        
        # Status Label
        self.statusLabel = tk.Label(self, text = "Status: Waiting")
        self.statusLabel.grid(row=4, column=0, padx=5, pady=10, columnspan=2)
    
    def GetFile(self):
        self.fileName = askopenfilename()
    
    def StartCleaning(self):
        if len(self.entrySeperatorString.get()) > 1:
            self.statusLabel["text"] = "Status: ERROR: Entry Seperator must be 1\ncharacter."
        else:
            try:
                if isinstance(self.fileName, str):
                    self.statusLabel["text"] = "Status: All conditions met and files should be in\n same directory as original file"
                    DatasetCleanerMain.Run(self.fileName, self.entrySeperatorString.get(), self.isRegression.get())
            except AttributeError:
                self.statusLabel["text"] = "Status: ERROR: File not selected"
            except FileNotFoundError:
                self.statusLabel["text"] = "Status: ERROR: File not found"
            except:
                print(sys.exc_info())
                self.statusLabel["text"] = "Status: ERROR: Unknown error occured"

class ViewApp(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        # Get file button
        self.getFile = tk.Button(self, text="Load File", command=lambda: self.GetFile())
        self.getFile.pack(ipadx=35, ipady=10)
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(expand=True, side = tk.RIGHT, fill = tk.Y)
        
        self.mylist = tk.Listbox(self, yscrollcommand = self.scrollbar.set)
        
        self.mylist.pack( side = tk.LEFT, fill = tk.BOTH )
        self.scrollbar.config( command = self.mylist.yview )
    
    
    def GetFile(self):
        self.fileName = askopenfilename()
        
        self.mylist.delete(0, self.mylist.size())
        
        # Get file from user
        self.userFile = open(self.fileName, "r")
        
        self.characterCount = 0
        
        for instance in self.userFile:
            if len(instance) > self.characterCount:
                self.characterCount = len(instance)
            self.mylist.insert(tk.END, instance)
        
        self.mylist["width"] = self.characterCount
        self.mylist["heigh"] = self.mylist.size()
        
        self.userFile.close()

class LearnApp(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        pass


if __name__ == "__main__":
    
    # Setup window
    root = tk.Tk()
    tabControl = ttk.Notebook(root)
    
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    
    tabControl.add(tab1, text='Clean')
    tabControl.add(tab2, text='View')
    tabControl.add(tab3, text='Learn')
    tabControl.pack(expand=1, fill="both")
    
    cleanApp = CleanApp(master=tab1)
    viewApp = ViewApp(master=tab2)
    learnApp = LearnApp(master=tab3)
    
    root.winfo_toplevel().title("Dataset Cleaner")
    
    root.mainloop()