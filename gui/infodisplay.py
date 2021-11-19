"""
infodisplay.py: InfoDisplay component for each dropdown display for our GUI.
Description: This file implement a infodisplay GUI object that takes a dictionary
of datas and returns a dictionary of labels with the data
"""


import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import gui

class InfoDisplay(ttk.Frame):
    def __init__(self, parent, info, graph, gui):
        """
        Initilize Infodisplay from info and graph
        Attributes:
            - parent: frame 
                Frame of GUI this is contained in
            - graph: Dict<String:String>
                Information on what graphs should be added
            - info: Dict<String:String>
                The information for what to display
            - gui: Interface
                The interface that this is being put in
            - _r: Int
                The number of rows that the frame is using
            - _ip: String
                the ip for the represented machine
            - frame: frame
                The frame that the add/rmv buttons are contained in
            - _data: Dict<String:String>
                The data that is to be displayed
            - _plots: Dict<String:String>
                The matplots that are displayed
            - _seperators: [Seperator]
                The seperators imployed in the display
            - addbtn: Button
                The button for adding elements to the data
            - rmvbtn: Button
                The button for removing elements from the data

        """
        ttk.Frame.__init__(self, parent)				
        self.parent = parent
        self.graph = graph
        self.info = info
        self.gui = gui
        self._r = 0
        myFont = font.Font(weight="bold")

        self._ip = ttk.Label(self, 
                                text=('ip: ' + self.info['ip']), 
                                justify=tk.LEFT,
                                borderwidth = 0,
                                relief="ridge")
        self._ip['font'] = myFont
        self._ip.grid(row = self._r, 
                        column = 0, 
                        sticky='w')
        self._r = self._r + 1

        self._data, self._plots, self._seperators = self._create_text_list(info['data'])

        self.frame = ttk.Frame(self)
        self.addbtn = ttk.Checkbutton(self.frame, text="+", width='2', style ="TButton", command=lambda: self.gui.add_value(self.info['ip']))
        self.addbtn.grid(row = 0, rowspan='1', column = 0, sticky='w')
        self.rmvbtn = ttk.Checkbutton(self.frame, text="-", width='2', style ="TButton", command=lambda: self.gui.rmv_value(self.info['ip']))
        self.rmvbtn.grid(row = 0, rowspan='1', column = 1, sticky='w')
        self.frame.grid(row = self._r, rowspan='1', column = 0, sticky='w')
        self._r = self._r + 1

    def _create_text_list(self, info):
        """
        Create the labels and graphs for the info
        Arguments:
            info: Dict<String:String>
                The information to display
        """
        data = {}
        plots = {}
        separators = []
        myFont = font.Font(weight="bold")
        for k, v in info.items():
            data[k] = ttk.Label(self, 
                                    text=(k+': '+v), 
                                    justify=tk.LEFT,
                                    borderwidth = 0,
                                    relief="ridge")

            data[k]['font'] = myFont
            data[k].grid(row = self._r, 
                    column = 0, 
                    sticky='w')

            if k in self.graph.keys():
                plots[k] = gui.animplot(self, int(self.graph[k]['length']), 
                                              int(self.graph[k]['min']), 
                                              int(self.graph[k]['max']))
                plots[k].getCanvas().get_tk_widget().grid(row = self._r+1, 
                                                    column = 0, 
                                                    sticky='w')

                separators.append(tk.Label(self, bg='#464646', text=""))
                separators[-1].grid(row = self._r+2, column = 0, columnspan=5, sticky="ew")
                self._r = self._r + 3
            else:
                self._r = self._r + 1

        return data, plots, separators

    def get_data(self):
        """return the data stored in this object"""
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

