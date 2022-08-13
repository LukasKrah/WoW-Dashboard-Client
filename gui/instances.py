"""
gui/instances.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *

from .widgets import Table, NavBar
from data import Theme


##################################################
#                 Menu classes                   #
##################################################

class InstanceTable(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(bd=0, highlightthickness=0, background=Theme.background3)

        self.table = Table(self)
        # self.table.values = {"a": {"b": self.click, "c": self.click}}
        self.table.reload()
        self.navBar = NavBar(self)

        self.grid_widgets()

    def click(self, field: CTkCanvas) -> None:
        ...

    def grid_widgets(self) -> None:
        self.table.grid(row=0, column=0, sticky="NSEW")
        self.navBar.grid(row=1, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



