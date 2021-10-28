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
        self.lom = {}
        while(1):
            self.root.update()

    def makeCpane(self, name, data):
        cpane = cp(self.root, name, name)
        cpane.grid(row = 0, column = 0, sticky = 'w')
        info = infd(cpane.frame, data)
        info.grid(row = 1, column = 0)
        return cpane, info

    def load_file(self):
        filename = filedialog.askopenfilename(initialdir='./config',
                                                title = 'Select a swarm config',
                                                filetypes=[("Json", '*.json')])
        try:
            with open(filename) as f:
                data = json.load(f)
        except:
            messagebox.showinfo("Config Error", "config json not in correct format!")
            return

        big_dict = data["mlist"]
        for i in range(0, len(big_dict)):
            ip = big_dict[i]["ip"]
            cpane, info = self.makeCpane(big_dict[i]["name"], big_dict[i])
            self.lom[ip] = {"name":big_dict[i]["name"], "cpane":cpane, "info":info}
            self.lom[ip]["cpane"].grid(row=i, column=0, sticky='nsew')

    def update_display(self, updates):
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
        self.lom[ip]["name"] = newname
        self.lom[ip]["cpane"].setName(newname)
        self.root.update()

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
        filemenu.add_command(label="Update", command=lambda: self.update_display({"71.25.180.79": {"mem": 1, "temp": 100}, "108.147.247.58": {"mem": 5, "temp": 500}}))
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        #filemenu.add_command(label="Exit", command=lambda: self.gui_exit())
        root.config(menu=menubar)
        return root