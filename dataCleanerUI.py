import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import DatasetCleanerMain
import LearnML
import PredictML
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
        fileName = askopenfilename()
        
        self.mylist.delete(0, self.mylist.size())
        
        # Get file from user
        userFile = open(fileName, "r")
        
        characterCount = 0
        
        for instance in userFile:
            if len(instance) > characterCount:
                characterCount = len(instance)
            self.mylist.insert(tk.END, instance)
        
        self.mylist["width"] = characterCount
        self.mylist["heigh"] = self.mylist.size()
        
        userFile.close()

class LearnApp(tk.Frame):
    
    # Variables
    learnFile = None
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Get file button
        self.getFile = tk.Button(self, text="Load File", command=lambda: self.GetFile())
        self.getFile.grid(row=0, column=0, ipadx=40, ipady=10)
        
        self.startLearning = tk.Button(self, text = "Start Learning from Dataset", command=lambda: self.StartLearning())
        self.startLearning.grid(row=0, column=1, ipadx=10, ipady=10, rowspan=1)
        
        # Status Label
        self.statusLabel = tk.Label(self, text = "Status: Waiting")
        self.statusLabel.grid(row=1, column=0, padx=5, pady=10, columnspan=2)
    
    def GetFile(self):
        self.learnFile = askopenfilename()
    
    def StartLearning(self):
        try:
            if isinstance(self.learnFile, str):
                self.statusLabel["text"] = "Status: All conditions met and files should be in\n same directory as original file"
                LearnML.Run(self.learnFile)
        except AttributeError:
            self.statusLabel["text"] = "Status: ERROR: File not selected"
        except FileNotFoundError:
            self.statusLabel["text"] = "Status: ERROR: File not found"
        except:
            print(sys.exc_info())
            self.statusLabel["text"] = "Status: ERROR: Unknown error occured"

class PredictApp(tk.Frame):
    
    # Variables
    modelFile = None
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Get file button
        self.getFile = tk.Button(self, text="Load Model File", command=lambda: self.GetFile())
        self.getFile.grid(row=0, column=0, ipadx=30, ipady=10)
        
        self.startPredicting = tk.Button(self, text = "Predict Target from Model", command=lambda: self.StartPredicting())
        self.startPredicting.grid(row=0, column=1, ipadx=10, ipady=10, rowspan=1)
        
        # Get seperator
        self.entryFeatureString = tk.StringVar()
        self.label1 = tk.Label(self, text="Features(Comma Seperated):")
        self.label1.grid(row=1, column=0)
        self.entrySeperator = tk.Entry(self, bd=1, textvariable=self.entryFeatureString)
        self.entrySeperator.grid(row=1, column=1)
        
        # Status Label
        self.statusLabel = tk.Label(self, text = "Status: Waiting")
        self.statusLabel.grid(row=2, column=0, padx=5, pady=10, columnspan=2)

    def GetFile(self):
        self.modelFile = askopenfilename()
        
    def StartPredicting(self):
        if len(self.entryFeatureString.get()) < 1:
            self.statusLabel["text"] = "Status: ERROR: Entry Seperator must be atleast 1 character."
        else:
            try:
                if isinstance(self.modelFile, str):
                    self.statusLabel["text"] = PredictML.Run(self.modelFile, self.entryFeatureString.get())
                    
            except AttributeError:
                self.statusLabel["text"] = "Status: ERROR: File not selected"
            except FileNotFoundError:
                self.statusLabel["text"] = "Status: ERROR: File not found"
            except:
                print(sys.exc_info())
                self.statusLabel["text"] = "Status: ERROR: Unknown error occured"

if __name__ == "__main__":
    
    # Setup window
    root = tk.Tk()
    tabControl = ttk.Notebook(root)
    
    cleanTab = ttk.Frame(tabControl)
    dataViewTab = ttk.Frame(tabControl)
    learnTab = ttk.Frame(tabControl)
    predictTab = ttk.Frame(tabControl)
    
    tabControl.add(cleanTab, text='Clean Dataset')
    tabControl.add(dataViewTab, text='View Dataset')
    tabControl.add(learnTab, text='Learn')
    tabControl.add(predictTab, text="Predict")
    tabControl.pack(expand=1, fill="both")
    
    cleanApp = CleanApp(master=cleanTab)
    viewApp = ViewApp(master=dataViewTab)
    learnApp = LearnApp(master=learnTab)
    predictApp = PredictApp(master=predictTab)
    
    root.winfo_toplevel().title("Machine Leanring Tool")
    
    root.mainloop()