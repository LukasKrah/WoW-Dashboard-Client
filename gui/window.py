"""
gui/window.py

Project: WoW-Dashboard-Client
Created: 12.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import CTk
from os import kill, getpid
from tkinter import Event

from data import Settings, InstanceManager
from style import Theme

from .instances import InstanceTable
from .menu import TopMenu, LeftMenu
from .wowToken import WoWToken


##################################################
#                     Code                       #
##################################################

class Window(CTk):
    topMenu: TopMenu
    leftMenu: LeftMenu
    windows: dict

    current_window: str

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

        self.title("WoW-Dashboard")
        self.wm_iconbitmap("style/images/wow.ico")
        self.minsize(
            self.winfo_screenwidth() // 2,
            self.winfo_screenheight() // 2)
        self.state("zoomed")
        self.option_add("*font", Theme.font)

        self.current_window = "instanceTable"

        self.windows = {
            "instanceTable": InstanceTable(self),
            "wowToken": WoWToken(self)}

        self.topMenu = TopMenu(self)
        self.leftMenu = LeftMenu(
            self,
            {"instanceTable":
                {"label": "InstanzenTabelle",
                 "selected": True,
                 "command": lambda w="instanceTable": self.change_to_frame(w)},
             "wowToken":
                {"label": "WoW-Token",
                 "command": lambda w="wowToken": self.change_to_frame(w)}}
        )

        self.bind("<F11>", self.toggle_fullscreen)
        self.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.grid_widgets()

    def change_to_frame(self, framename: str) -> None:
        self.current_window = framename

        for window in self.windows:
            self.windows[window].grid_forget()

        match framename:
            case "wowToken":
                self.windows[framename].force_reload = True

        self.windows[framename].grid(row=1, column=1, sticky="NSEW")

    def grid_widgets(self) -> None:
        self.topMenu.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.leftMenu.grid(row=1, column=0, sticky="NSEW")
        self.windows[self.current_window].grid(row=1, column=1, sticky="NSEW")

        for column, weight in enumerate([1]):
            self.grid_columnconfigure(column + 1, weight=weight)
        for row, weight in enumerate([1]):
            self.grid_rowconfigure(row + 1, weight=weight)
        self.update_idletasks()
        self.leftMenu.grid_columnconfigure(
            0, minsize=self.leftMenu.winfo_width())

    def toggle_fullscreen(self, _event: Event) -> None:
        if self.state() == "zoomed":
            self.state("normal")
            return
        self.state("zoomed")

    def delete_window(self, *_args: any) -> None:
        Settings.write()
        InstanceManager.write()

        self.destroy()
        kill(getpid(), 9)
