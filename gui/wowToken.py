"""
gui/wowToken.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from threading import Thread
from customtkinter import *
from tkinter import *

from data import API
from style import Theme


##################################################
#                 Menu classes                   #
##################################################

class WoWToken(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(bg=Theme.background3, bd=0, highlightthickness=0)

        self.price = CTkLabel(self, text="", text_font=Theme.font)

        self.grid_widgets()
        Thread(target=self.getTokenPrive).start()

    def getTokenPrive(self) -> None:
        self.price.configure(text=str(API.getTokenPrice())[:-4] + " Gold")

    def grid_widgets(self) -> None:
        self.price.grid()
