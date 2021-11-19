"""
collapsiblepane.py
A frame contained within a dropdown that:
    - Opens frame when button is pressed
    - Hides frame when button is pressed again
"""
import tkinter as tk
from tkinter import ttk
 
class CollapsiblePane(ttk.Frame):
    def __init__(self, parent, expanded_text ="Collapse <<",
                               collapsed_text ="Expand >>"):
        """
        Attributes:
            - parent: frame 
                Frame of GUI this is contained in
            - _expanded_text: String
                Text displayed when frame is extended
            - _collapsed_text: String
                Text displayed when frame is collapsed
            - _variable: Int
                Tracks if the frame is extended
            - _button: Button
                The button that controls extension
            - _separator: Separator
                element used to provide a boundry
            - frame: frame
                The frame elements of this class are contained in
        """
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text
        self.columnconfigure(1, weight = 1)
        self._variable = tk.IntVar()
 
        self._button = ttk.Checkbutton(self, variable = self._variable,
                            command = self._activate, style ="TButton")
        self._button.grid(row = 0, column = 0)

        self._separator = ttk.Separator(self, orient ="horizontal")
        self._separator.grid(row = 0, column = 1, sticky ="we")
 
        self.frame = ttk.Frame(self)

        self._activate()

    def setName(self, newname):
        """
        Sets text displayed inside of button
        Arguments:
            newname: String
                the string to put on the button
        """
        self._expanded_text=newname
        self._collapsed_text=newname
 
    def _activate(self):
        """
        Activates the frame
        """
        if not self._variable.get():
            self.frame.grid_forget()
 
            self._button.configure(text = self._collapsed_text)
 
        elif self._variable.get():
            self.frame.grid(row = 1, column = 0, columnspan = 2, sticky='w')
            self._button.configure(text = self._expanded_text)
 
    def toggle(self):
        """
        Toggles if frame is extended
        """
        self._variable.set(not self._variable.get())
        self._activate()