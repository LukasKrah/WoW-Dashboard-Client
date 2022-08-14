"""
gui/window.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *

from data import Theme
from .menu import TopMenu, LeftMenu
from .instances import InstanceTable
from .wowToken import WoWToken


##################################################
#                 Window class                   #
##################################################

class Window(CTk):
    topMenu: TopMenu
    leftMenu: LeftMenu

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

        self.title("WoW-Dashboard")
        self.wm_iconbitmap("images/wow_icon.ico")
        self.minsize(self.winfo_screenwidth()//2, self.winfo_screenheight()//2)
        self.state("zoomed")
        self.option_add("*font", Theme.font)

        self.instanceTable = InstanceTable(self)
        self.wowToken = WoWToken(self)

        self.topMenu = TopMenu(self)
        self.leftMenu = LeftMenu(self, {"InstanzenTabelle": self.instanceTable,
                                        "WoW-Marke": self.wowToken})

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.topMenu.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.leftMenu.grid(row=1, column=0, sticky="NSEW")
        self.instanceTable.grid(row=1, column=1, sticky="NSEW")

        for column, weight in enumerate([5]):
            self.grid_columnconfigure(column+1, weight=weight)
        for row, weight in enumerate([5]):
            self.grid_rowconfigure(row+1, weight=weight)

