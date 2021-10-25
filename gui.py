"""
gui.py:     Main file for our Graphical User Interface.
TODOS:      GUI quit function and Update function.
Description:This file implement majority of the main functionalities of our GUI object,
            such as initialization and update functions.
"""


from collapsiblepane import CollapsiblePane as cp
from infodisplay import InfoDisplay as infd
import json
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk


class Gui():
    def __init__(self):
        self.root = self.intialization()
        while(1):
            self.root.update()

    def makeCpane(self, name, data):
        cpane = cp(self.root, name, name)
        cpane.grid(row = 0, column = 0, sticky = 'w')
        d = infd(cpane.frame, data).grid(row = 1, column = 0,)
        return cpane

    def load_file(self):
        filename = filedialog.askopenfilename(initialdir='./config',
                                                title = 'Select a swarm config',
                                                filetype = [('JSON files','*.json')])
        try:
            with open(filename) as f:
                data = json.load(f)
        except:
            messagebox.showinfo("Config Error", "config json not in correct format!")
            return
            
        list_of_machines = data["mlist"]
        Buttons = [None] * len(list_of_machines)
        for i in range(0, len(list_of_machines)):
            Buttons[i] = self.makeCpane(list_of_machines[i]['name'], list_of_machines[i])
            Buttons[i].grid(row=i, column=0, sticky='nsew')

    #
    #def gui_exit(self):
    #    self.root.quit


    # Making root window or parent window
    def intialization(self):
        root = ThemedTk(theme="equilux")
        root.geometry('1000x1000')
        root.configure(bg='#464646')
        root.title("SRHMD")
        Grid.columnconfigure(root, 0, weight=1)
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load", command=lambda: self.load_file())
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        #filemenu.add_command(label="Exit", command=lambda: self.gui_exit())
        root.config(menu=menubar)
        return root

