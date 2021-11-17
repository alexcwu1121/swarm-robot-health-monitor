"""
gui.py
Main file for our Graphical User Interface.
"""

import gui
import json
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk


class Gui():
    def __init__(self):
        """
        Attributes:
            - root: tkinter root instance
                the root for the gui elements
            - lom: dict<String:String>
                holds data from configuration file
            - loaded_file: Dict<String:String>
                loaded data directly from config json
            - started: Boolean
                indicates whether GUI has started or not
        """
        self.root = self.intialization()
        self.lom = {}
        self.loaded_file = ""
        self.started = False
        self.root.update()

    def refresh_gui(self):
        """Update the gui with changes"""
        self.root.update()        

    def makeCpane(self, name, data):
        """
        return collapsiblepane object representing a machine
        Arguments: 
            - name: String
                name of the machine
            - data: dict<String:String>
                The data the infodisplay object should contain
        """
        cpane = gui.cp(self.root, name, name)
        cpane.grid(row = 0, column = 0, sticky = 'w')
        info = gui.infd(cpane.frame, data)
        info.grid(row = 1, column = 0)
        return cpane, info

    def load_file(self):
        """Load a new config file and update GUI"""
        old_loaded = self.loaded_file
        filename = filedialog.askopenfilename(initialdir='./config',
                                                title = 'Select a swarm config',
                                                filetypes=[("Json", '*.json')])
        try:
            self.loaded_file = filename
            with open(filename) as f:
                data = json.load(f)
        except:
            self.loaded_file = old_loaded
            messagebox.showinfo("Config Error", "config json not in correct format!")
            return
        for v in self.lom.values():
            v["cpane"].destroy()
            v["info"].destroy()
        self.lom.clear()

        big_dict = data["mlist"]
        for i in range(0, len(big_dict)):
            ip = big_dict[i]["ip"]
            cpane, info = self.makeCpane(big_dict[i]["name"], big_dict[i])
            self.lom[ip] = {"name":big_dict[i]["name"], "cpane":cpane, "info":info}
            self.lom[ip]["cpane"].grid(row=i, column=0, sticky='nsew')

    def get_config(self):
        """return the currently loaded config file"""
        return self.loaded_file

    def update_display(self, updates):
        """
        Update the gui with updates
        Arguments: 
            - updates: dict<String:String>
                dictionary of updates for the GUI

        """
        ip = list(updates.keys())[0]
        content = updates[ip]
        info = self.lom[ip]["info"].get_data()
        for k in info:
            try:
                self.lom[ip]["info"].set_data(k, content[k])
            except KeyError:
                pass
        self.root.update()

    def changeName(self, ip, newname):
        """
        change the name of a machine
        Arguments: 
            - ip: String
                The ip of the machine
            - newname: String
                The name to change the machine to

        """
        self.lom[ip]["name"] = newname
        self.lom[ip]["cpane"].setName(newname)
        self.root.update()

    def intialization(self):
        """create the root and options of the GUI"""
        root = ThemedTk(theme="equilux")
        root.geometry('1000x1000')
        root.configure(bg='#464646')
        root.title("SRHMD")
        Grid.columnconfigure(root, 0, weight=1)
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load", command=lambda: self.load_file())
        #filemenu.add_command(label="Update", command=lambda: self.update_display({"71.25.180.79": {"mem": 1, "temp": 100}, "108.147.247.58": {"mem": 5, "temp": 500}}))
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        #filemenu.add_command(label="Exit", command=lambda: self.gui_exit())
        root.config(menu=menubar)
        return root