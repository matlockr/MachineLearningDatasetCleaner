import tkinter as tk
from tkinter.filedialog import askopenfilename
import DatasetCleanerMain
import sys

class Application(tk.Frame):
    
    # Variables
    filename = None
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Dataset Cleaner")
        
        # Get file button
        self.getFile = tk.Button(self, text="Load File", command=lambda: self.GetFile())
        self.getFile.pack(side="top")
        
        # Is the data for Regression Checkbox
        self.isRegression = tk.IntVar()
        self.labelIsRegression = tk.Checkbutton(self, text = "Clean for Regression", variable=self.isRegression)
        self.labelIsRegression.pack()
        
        # Get seperator
        self.entrySeperatorString = tk.StringVar()
        self.label1 = tk.Label(self, text="Seperator character:")
        self.label1.pack()
        self.entrySeperator = tk.Entry(self, bd=1, textvariable=self.entrySeperatorString)
        self.entrySeperator.pack()
        
        # Get delete instance question
        self.deleteBadInstances = tk.IntVar()
        self.label2 = tk.Label(self, text="If there are any unknows or null values in the data, would you like to: \na: Leave unknowns and null values but use default values for all of them \nb: Delete any instance with a unknown or null value")
        self.label2.pack()
        self.checkBox = tk.Checkbutton(self, text = "Delete Bad Instances", variable=self.deleteBadInstances)
        self.checkBox.pack()
        
        self.startCleaning = tk.Button(self, text = "Start Cleaning Dataset", command=lambda: self.StartCleaning())
        self.startCleaning.pack()
        
        # Quit button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        # Status Label
        self.statusLabel = tk.Label(self, text = "Status: ")
        self.statusLabel.pack();
    
    def GetFile(self):
        self.fileName = askopenfilename()
    
    def StartCleaning(self):
        if len(self.entrySeperatorString.get()) > 1:
            self.statusLabel["text"] = "Status: ERROR: Entry Seperator must be 1\ncharacter."
        else:
            try:
                if isinstance(self.fileName, str):
                    self.statusLabel["text"] = "Status: All conditions met and files should be in\n same directory as original file"
                    DatasetCleanerMain.Run(self.fileName, self.entrySeperatorString.get(), self.deleteBadInstances.get(), self.isRegression.get())
            except AttributeError:
                self.statusLabel["text"] = "Status: ERROR: File not selected"
            except:
                print(sys.exc_info())
                self.statusLabel["text"] = "Status: ERROR: Unknown error occured"

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = Application(master=root)
    app.mainloop()