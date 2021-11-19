import tkinter as tk
from tkinter import Canvas, ttk
import os
from PIL import ImageTk,Image

class StatusLight(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.color = 'grey'
        self.grid

        self.canvas = Canvas(self, width = 20, height = 20)
        self.canvas.grid(row = 0, column = 0)
        self.red = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/red.png"))
        self.yellow = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/yellow.png"))
        self.green = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/green.png"))
        self.grey = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"/grey.png"))
        self.canvas.create_image(20, 20, anchor='center', image=self.grey)

    def set_status(self, status):
        self.canvas.delete("all")
        if(status==-1):
            self.canvas.create_image(20, 20, anchor='center', image=self.grey)
        elif(status==1):
            self.canvas.create_image(20, 20, anchor='center', image=self.yellow)
        elif(status==0):
            self.canvas.create_image(20, 20, anchor='center', image=self.green)
        elif(status==2):
            self.canvas.create_image(20, 20, anchor='center', image=self.red)
