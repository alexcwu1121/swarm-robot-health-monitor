"""
infodisplay.py: InfoDisplay component for each dropdown display for our GUI.
TODOS: TBD
Description: This file implement a infodisplay GUI object that takes a dictionary
of datas and returns a dictionary of labels with the data
"""


import tkinter as tk
from tkinter import ttk

class InfoDisplay(ttk.Frame):

    def __init__(self, parent, info):
        ttk.Frame.__init__(self, parent)				
        self.parent = parent
        self._r = 0
        #ip address as string
        self._ip = ttk.Label(self, 
                                text=('ip: ' + info['ip']), 
                                justify=tk.LEFT,
                                borderwidth = 2,
                                relief="ridge")
        self._ip.grid(row = self._r, 
                        column = 0, 
                        sticky='w')
        self._r = self._r + 1
        #dictionary of core datas to be displayed
        self._core = self._create_text_list(info['data'])
        self.frame = ttk.Frame(self)

    def _create_text_list(self, info):
        data = {}
        i = 0
        for k, v in info.items():
            data[k] = ttk.Label(self, 
                                    text=(k+': '+v), 
                                    justify=tk.LEFT,
                                    borderwidth = 2,
                                    relief="ridge",
                                    width=20)
            data[k].grid(row = self._r, 
                            column = i, 
                            sticky='w')
            i = i + 1
        return data
