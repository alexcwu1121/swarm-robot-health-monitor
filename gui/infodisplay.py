"""
infodisplay.py: InfoDisplay component for each dropdown display for our GUI.
TODOS: CHANGE DISPLAY FORMAT TO BE 2 COLUMNS
Description: This file implement a infodisplay GUI object that takes a dictionary
of datas and returns a dictionary of labels with the data
"""


import tkinter as tk
from tkinter import ttk
import tkinter.font as font

class InfoDisplay(ttk.Frame):

    def __init__(self, parent, info):
        ttk.Frame.__init__(self, parent)				
        self.parent = parent
        self._r = 0
        myFont = font.Font(weight="bold")
        #ip address as string
        self._ip = ttk.Label(self, 
                                text=('ip: ' + info['ip']), 
                                justify=tk.LEFT,
                                borderwidth = 0,
                                relief="ridge")
        self._ip['font'] = myFont
        self._ip.grid(row = self._r, 
                        column = 0, 
                        sticky='w')
        self._r = self._r + 1
        #dictionary of core datas to be displayed
        self._data = self._create_text_list(info['data'])
        self.frame = ttk.Frame(self)

    def _create_text_list(self, info):
        data = {}
        myFont = font.Font(weight="bold")
        i = 1
        for k, v in info.items():
            data[k] = ttk.Label(self, 
                                    text=(k+': '+v), 
                                    justify=tk.LEFT,
                                    borderwidth = 0,
                                    relief="ridge")
            data[k]['font'] = myFont
            data[k].grid(row = i, 
                            column = 0, 
                            sticky='w')
            i = i + 1
        return data

    def get_data(self):
        return self._data

    def set_data(self, k, v):
        self._data[k].config(text=str(v))

