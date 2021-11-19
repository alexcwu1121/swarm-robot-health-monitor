import tkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import numpy as np
import random

class animatedplot():
    def __init__(self, parent, seconds, min, max): 
        """creates a matplot with given parameters
        Attributes:
            - fig: Figure 
                The matplot figure to show
            - line: Plot
                The data to graph
            - canvas: Canvas
                The canvas to display
            - seconds: Int
                The number number of entries to keep track of
            - data: [Int]
                The values to graph
        """
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

    def update(self, value):
        """
        updates plot with new value
        Arguments:
            value: Int
                The value to add to the graph
        """
        self.data.pop(0)
        self.data.append(value)

        x = np.linspace(-self.seconds, 0, self.seconds)
        y = self.data
        self.line.set_data(x, y)
        self.canvas.draw()

    def getCanvas(self):
        """returns the canvas the plot is on"""
        return self.canvas
