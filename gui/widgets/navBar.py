"""
.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *

from data import Theme

##################################################
#                     Code                       #
##################################################


class NavBar(CTkCanvas):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1,
            height=50)
