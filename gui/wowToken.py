"""
gui/wowToken.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from threading import Thread
from customtkinter import *

from data import API
from style import Theme


##################################################
#                 Menu classes                   #
##################################################

class WoWToken(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(bg=Theme.background3, bd=0, highlightthickness=0)

        self.price = CTkLabel(
            self, text="", text_font=(
                Theme.wow_font, Theme.fontfactor * 100))

        self.grid_widgets()
        Thread(target=self.get_token_price()).start()

    def get_token_price(self) -> None:
        self.price.configure(text=str(API.get_token_history())[:-4] + " Gold")

    def grid_widgets(self) -> None:
        self.price.grid()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
