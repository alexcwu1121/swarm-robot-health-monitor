import tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import numpy as np
import random

#creates a plot that can be displayed withing the GUI
#The root param is the root 
#The seconds param is for how long in the past it should track, this is the range of the x axis
#Min and max determin range of y axis
class animatedplot():
    def __init__(self, parent, seconds, min, max): 
        plt.rcParams["figure.figsize"] = [3.00, 1.50]
        plt.rcParams["figure.autolayout"] = True

        plt.axes(xlim=(-seconds, 0), ylim=(min, max))
        self.fig = plt.Figure(dpi=100)
        ax = self.fig.add_subplot(xlim=(-seconds, 0), ylim=(min, max))
        self.line, = ax.plot([], [], lw=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()

        self.seconds = seconds
        self.data = [0] * seconds

    #update the plot with a new value
    def update(self, value):
        self.data.pop(0)
        self.data.append(value)

        x = np.linspace(-self.seconds, 0, self.seconds)
        y = self.data
        self.line.set_data(x, y)
        self.canvas.draw()

    def getCanvas(self):
        return self.canvas
