"""
gui/menu.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk

from data import Settings
from style import Theme


##################################################
#                 Menu classes                   #
##################################################

class LeftMenu(CTkCanvas):
    master: Tk
    windows: dict[str, CTkCanvas | CTkFrame]

    def __init__(self,
                 master: Tk,
                 windows: dict[str,
                               CTkCanvas | CTkFrame],
                 *args: any,
                 **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.windows = windows

        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background2)

        for index, window in enumerate(windows):
            but = CTkButton(
                self,
                text=window,
                text_font=(
                    Theme.wow_font2,
                    Theme.fontfactor *
                    22),
                command=lambda win=windows[window]: self.change_to_frame(win))
            but.grid(row=index, column=0, sticky="EW")

        self.grid_widgets()

    def change_to_frame(self, frame: CTkCanvas | CTkFrame) -> None:
        for window in self.windows:
            self.windows[window].grid_forget()
        frame.grid(row=1, column=1, sticky="NSEW")

    def grid_widgets(self) -> None:
        ...


class TopMenu(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

        wow = ImageTk.PhotoImage(Image.open(
            "images/wow_icon.ico").resize((50, 50)))

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
            font=(
                Theme.wow_font2,
                Theme.fontfactor *
                22))

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.can.grid(row=0, column=0, sticky="NSEW")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
