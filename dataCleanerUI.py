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
        self.startCleaning.grid(row=1, column=1, ipadx=10, ipady=30, rowspan=3)
        
        # Quit buttonx
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(row=0, column=1, ipadx=55, ipady=10)
        
        # Status Label
        self.statusLabel = tk.Label(self, text = "Status: ")
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

if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("500x500")
    app = Application(master=root)
    app.mainloop()