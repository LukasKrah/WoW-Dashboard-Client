"""
gui/menu.py

Project: WoW-Dashboard-Client
Created: 13.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from PIL import Image, ImageTk
from tkinter import Tk

from gui.widgets import KButtonGroup, KCanvas
from data import Settings
from style import Theme


##################################################
#                     Code                       #
##################################################

class LeftMenu(KCanvas):
    master: Tk
    windows: dict

    butgroup: KButtonGroup

    def __init__(self,
                 master: Tk,
                 windows: dict,
                 *args: any,
                 **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.windows = windows

        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1)

        self.butgroup = KButtonGroup(self, self.windows)
        self.grid_widgets()

        self.bind("<Configure>", self.reload)

    def reload(self, *_args: any) -> None:
        ...
        # self.delete("background")
        # self.create_gradient(from_color=Theme.background1,
        #                      to_color=Theme.background2,
        #                      tags=["background"])

    def grid_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        for index, but in enumerate(self.butgroup.buttons):
            but.grid(row=index, column=0, sticky="NSEW")


class TopMenu(KCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

        self.photo = ImageTk.PhotoImage(Image.open(
            "style/images/wow.ico").resize((50, 50)))

        self.configure(
            height=50,
            bg=Theme.background1)
        self.create_image(0, 0, image=self.photo, anchor="nw")

        self.create_text(
            100,
            25,
            text=f"Willkommen  im  WoW-Dashboard  {Settings['myAccount']['characterName']}",
            anchor="w",
            fill=Theme.text_color,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                22))


