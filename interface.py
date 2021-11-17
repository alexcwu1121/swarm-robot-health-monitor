"""
gui.py:     Main file for our Graphical User Interface.
TODOS:      GUI quit function and Update function.
Description:This file implement majority of the main functionalities of our GUI object,
            such as initialization and update functions.
"""

import gui
import json
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk


class Gui():
    def __init__(self):
        self.root = self.intialization()
        self.lom = {}
        self.loaded_file = ""
        self.data = {}
        self.started = False
        self.root.update()

    def refresh_gui(self):
        self.root.update()        

    def makeCpane(self, name, data, graph):
        cpane = gui.cp(self.root, name, name)
        cpane.grid(row = 0, column = 0, sticky = 'w')
        info = gui.infd(cpane.frame, data, graph)
        info.grid(row = 1, column = 0)
        return cpane, info, graph

    def load_file(self):
        old_loaded = self.loaded_file
        filename = filedialog.askopenfilename(initialdir='./config',
                                                title = 'Select a swarm config',
                                                filetypes=[("Json", '*.json')])
        try:
            self.loaded_file = filename
            with open(filename) as f:
                self.data = json.load(f)
        except:
            self.loaded_file = old_loaded
            messagebox.showinfo("Config Error", "config json not in correct format!")
            return
        for v in self.lom.values():
            v["cpane"].destroy()
            v["info"].destroy()
        self.lom.clear()

        big_dict = self.data["mlist"]
        for i in range(0, len(big_dict)):
            ip = big_dict[i]["ip"]
            cpane, info, graph = self.makeCpane(big_dict[i]["name"], big_dict[i], big_dict[i].get("graph", {}))
            self.lom[ip] = {"name":big_dict[i]["name"], "cpane":cpane, "info":info, "graph":graph}
            self.lom[ip]["cpane"].grid(row=i, column=0, sticky='nsew')

    def save_file(self):
        old_loaded = self.loaded_file
        file = filedialog.asksaveasfile(initialdir='./config',
                                                title = 'Save swarm config',
                                                filetypes=[("Json", '*.json')])
        try:
            json.dump(self.data, file,  indent=4)
            self.loaded_file = file.name
        except:
            messagebox.showinfo("Config Error", "failed to save config file!")
            return

    def add_robot(self):
        pass

    def get_config(self):
        return self.loaded_file

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
        filemenu.add_command(label="Save", command=lambda: self.save_file())
        #filemenu.add_command(label="Update", command=lambda: self.update_display({"71.25.180.79": {"mem": 1, "temp": 100}, "108.147.247.58": {"mem": 5, "temp": 500}}))
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        #filemenu.add_command(label="Exit", command=lambda: self.gui_exit())
        root.config(menu=menubar)
        return root