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
from time import sleep

from data import API
from style import Theme, KImage


##################################################
#                 Menu classes                   #
##################################################

class WoWToken(CTkCanvas):
    force_reload: bool

    width: int
    height: int

    price: int

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(bg=Theme.background3, bd=0, highlightthickness=0)

        self.force_reload = False

        self.height = 0
        self.width = 0

        self.token_photo = KImage("style/images/wow_token.jpg")
        self.img = self.create_image(
            self.width/2,
            self.height/2,
            image=self.token_photo.imgTk,
            anchor="center")
        self.photo = self.token_photo

        self.price = self.create_text(
            self.width / 2,
            self.height / 2,
            text="",
            font=(Theme.wow_font, Theme.fontfactor * 100),
            fill=Theme.text_color_light)

        self.reload()
        self.get_token_price_threaded()

        self.bind("<Configure>", self.__resize)

    def reload(self) -> None:
        self.coords(self.price, self.width/2, self.height/2)
        self.coords(self.img, self.width/2, self.height/2)

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self.token_photo.resize(self.width, self.height, "cover")
        self.itemconfigure(self.img, image=self.token_photo.imgTk)
        self.reload()

    def get_token_price_threaded(self) -> None:
        Thread(target=self.get_token_price).start()

    def get_token_price(self) -> None:
        while True:
            self.itemconfigure(self.price, text=str(API.get_token_history())[:-4] + " Gold")
            for index in range(20):
                sleep(1)
                if self.force_reload:
                    self.force_reload = False
                    break
