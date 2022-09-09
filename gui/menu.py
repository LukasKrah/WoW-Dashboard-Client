"""
gui/menu.py

Project: WoW-Dashboard-Client
Created: 13.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import CTkCanvas
from PIL import Image, ImageTk
from tkinter import Tk

from gui.widgets import KButtonGroup
from data import Settings
from style import Theme


##################################################
#                     Code                       #
##################################################

class LeftMenu(CTkCanvas):
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
            background=Theme.background2)

        self.butgroup = KButtonGroup(self, self.windows)
        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        for index, but in enumerate(self.butgroup.buttons):
            but.grid(row=index, column=0, sticky="NSEW")


class TopMenu(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

        wow = ImageTk.PhotoImage(Image.open(
            "style/images/wow.ico").resize((50, 50)))

        self.can = CTkCanvas(
            self,
            width=50,
            height=50,
            bg=Theme.background1,
            bd=0,
            highlightthickness=0)
        self.can.create_image(0, 0, image=wow, anchor="nw")
        self.can.photo = wow

        self.can.create_text(
            100,
            25,
            text=f"Willkommen  im  WoW-Dashboard  {Settings['myAccount']['characterName']}",
            anchor="w",
            fill=Theme.text_color,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                22))

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.can.grid(row=0, column=0, sticky="NSEW")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
