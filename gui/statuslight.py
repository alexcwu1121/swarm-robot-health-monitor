"""
StatusLight.py
Implements a status to indicate robot status that:
    - changes when a new status is inputed
"""

import tkinter as tk
import os
from PIL import ImageTk,Image
from tkinter import Canvas, ttk

class StatusLight(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        """
        Attributes:
            - parent: Parent GUI frame
                This holds Statuslight as a GUI
            - canvas: Tkinter Canvas GUI
                This will hold the image of the status light
            - red: Tkinter Image
                Image read from file red.png to be used in canvas
            - yellow: Tkinter Image
                Image read from file yellow.png to be used in canvas
            - green: Tkinter Image
                Image read from file green.png to be used in canvas
            - grey: Tkinter Image
                Image read from file grey.png to be used in canvas
        """
        self.parent = parent
        self.canvas = Canvas(self, width = 20, height = 20)
        self.canvas.grid(row = 0, column = 0)
        self.red = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/red.png"))
        self.yellow = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/yellow.png"))
        self.green = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/green.png"))
        self.grey = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/grey.png"))
        self.canvas.create_image(20, 20, anchor='center', image=self.grey)

    def set_status(self, status):
        """
        Function that changes the displayed image to match status
        :parameters:
            - status String
                String represents the current status of the robot
        :return:
            None
        """
        self.canvas.delete("all")
        if(status=="disconnect"):
            self.canvas.create_image(20, 20, anchor='center', image=self.grey)
        elif(status=="warning"):
            self.canvas.create_image(20, 20, anchor='center', image=self.yellow)
        elif(status=="nominal"):
            self.canvas.create_image(20, 20, anchor='center', image=self.green)
        elif(status=="critical"):
            self.canvas.create_image(20, 20, anchor='center', image=self.red)

    