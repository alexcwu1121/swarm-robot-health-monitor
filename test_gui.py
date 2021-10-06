import numpy as np
from tkinter import * 
from tkinter.ttk import *
from tkinter import ttk
from collapsiblepane import CollapsiblePane as cp
from infodisplay import InfoDisplay as infd
from ttkthemes import ThemedStyle, ThemedTk
import json

def makeCpane(name, data):
    cpane = cp(root, name, name)
    cpane.grid(row = 0, column = 0, sticky = 'w')
    d = infd(cpane.frame, data).grid(row = 1, column = 0,)
    return cpane
 
# Making root window or parent window
root = ThemedTk(theme="equilux")
root.geometry('1000x1000')
root.configure(bg='#464646')
root.title("clustr")
Grid.columnconfigure(root, 0, weight=1)

#m_display = Frame(root)

with open('resources/config_example.json') as f:
   data = json.load(f)

list_of_machines = data["mlist"]

    
Buttons = [None] * len(list_of_machines)
for i in range(0, len(list_of_machines)):
    Buttons[i] = makeCpane(list_of_machines[i]['name'], list_of_machines[i])
    Buttons[i].grid(row=i, column=0, sticky='nsew')

#--------main
root.mainloop()