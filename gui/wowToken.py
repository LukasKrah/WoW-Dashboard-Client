"""
gui/wowToken.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from threading import Thread
from customtkinter import *
from time import sleep

from data import API
from style import Theme


##################################################
#                 Menu classes                   #
##################################################

class WoWToken(CTkCanvas):
    force_reload: bool

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(bg=Theme.background3, bd=0, highlightthickness=0)

        self.force_reload = False

        self.price = CTkLabel(
            self, text="", text_font=(
                Theme.wow_font, Theme.fontfactor * 100), text_color="white")

        self.grid_widgets()
        self.get_token_price_threaded()

    def get_token_price_threaded(self) -> None:
        Thread(target=self.get_token_price).start()

    def get_token_price(self) -> None:
        while True:
            self.price.configure(text=str(API.get_token_history())[:-4] + " Gold")
            for index in range(20):
                sleep(1)
                if self.force_reload:
                    self.force_reload = False
                    break

    def grid_widgets(self) -> None:
        self.price.grid()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
