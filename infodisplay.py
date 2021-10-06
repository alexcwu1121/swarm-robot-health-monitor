# Implementation of Collapsible Pane container
 
# importing tkinter and ttk modules
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
        self._core = self._create_text_list(info['core_data'], 
                                                'Core Data: ')
        self._r = self._r + 1
        
        #dictionary of sensor data to be displayed
        self._sensor = self._create_text_list(info['sensors_data'], 
                                                'Sensor Data: ')
        
        self.frame = ttk.Frame(self)
        
    def _create_text_list(self, info, title):
        core_data = {}
        core_data['title'] = ttk.Label(self, 
                                        text=title, 
                                        justify=tk.LEFT,
                                        borderwidth = 2,
                                        relief="ridge")
        core_data['title'].grid(row = self._r, 
                                column = 0, 
                                sticky='w')
        i = 1
        for k, v in info.items():
            core_data[k] = ttk.Label(self, 
                                        text=(k+': '+v), 
                                        justify=tk.LEFT,
                                        borderwidth = 2,
                                        relief="ridge",
                                        width=20)
            core_data[k].grid(row = self._r, 
                                column = i, 
                                sticky='w')
            i = i + 1
        return core_data