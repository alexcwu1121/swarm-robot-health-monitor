"""
infodisplay.py: InfoDisplay component for each dropdown display for our GUI.
TODOS: CHANGE DISPLAY FORMAT TO BE 2 COLUMNS
Description: This file implement a infodisplay GUI object that takes a dictionary
of datas and returns a dictionary of labels with the data
"""


import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import gui

class InfoDisplay(ttk.Frame):

    def __init__(self, parent, info, graph):
        """
        Initilize Infodisplay from info and graph
        """
        ttk.Frame.__init__(self, parent)				
        self.parent = parent
        self.graph = graph
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
        self.frame = ttk.Frame(self)
        self._data, self._plots, self._seperators = self._create_text_list(info['data'])

    def _create_text_list(self, info):
        """
        Create the labels and graphs for the info
        """
        data = {}
        plots = {}
        separators = []
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

            if k in self.graph.keys():
                plots[k] = gui.animplot(self, int(self.graph[k]['length']), 
                                              int(self.graph[k]['min']), 
                                              int(self.graph[k]['max']))
                plots[k].getCanvas().get_tk_widget().grid(row = i+1, 
                                                    column = 0, 
                                                    sticky='w')

                separators.append(tk.Label(self, bg='#464646', text=""))
                separators[-1].grid(row = i+2, column = 0, columnspan=5, sticky="ew")
                i = i + 3
            else:
                i = i + 1

        return data, plots, separators

    def get_data(self):
        """
        return the data stored in this object
        """
        return self._data

    def set_data(self, k, v):
        """
        set the data stored in this object
        Arguments: 
            k: String
                the item in data to update
            v: String
                the value to update to
        """
        self._data[k].config(text=str(v))
        if v.split()[-1] != '0':
            self._plots[k].update(float(v.split()[-1][1:-2]))

