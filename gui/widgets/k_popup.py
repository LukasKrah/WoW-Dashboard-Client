"""
widgets/k_popup.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable
from customtkinter import *

from style import Theme

from .intern import KEntry, KOptionMenu, KMenu


##################################################
#                     Code                       #
##################################################

class KPopUp(CTkToplevel):
    master: any
    name: str
    inputs: list[dict]
    args: any
    relx: float
    rely: float
    confirm_call: Callable
    kwargs: any

    width: int
    height: int

    input_elems: list[KEntry | KOptionMenu | KMenu]
    buttons: list[CTkButton]

    def __init__(
            self,
            master,
            name: str,
            inputs: list[dict],
            *args: any,
            relx: float | None = 0.25,
            rely: float | None = 0.25,
            confirm_call: Callable,
            **kwargs: any) -> None:
        self.master = master
        self.name = name
        self.inputs = inputs
        self.args = args
        self.relx = relx
        self.rely = rely
        self.confirm_call = confirm_call
        self.kwargs = kwargs

        CTkToplevel.__init__(self, self.master, *self.args, *self.kwargs)

        self.create(True)

    def create(self, first: bool | None = False) -> None:
        if not first:
            CTkToplevel.__init__(self, self.master, *self.args, *self.kwargs)

        self.withdraw()
        self.title(self.name)
        self.configure(background=Theme.background1)
        self.attributes("-topmost", True)
        self.wm_iconbitmap("style/images/wow_icon.ico")

        self.input_elems = []
        self.buttons = []

        for _input in self.inputs:
            if _input["type"] == "InputText":
                self.input_elems.append(KEntry(self, _input["label"]))

            elif _input["type"] == "OptionMenu":
                self.input_elems.append(
                    KOptionMenu(
                        self,
                        _input["label"],
                        values=_input["validValues"]))

            elif _input["type"] == "ComboBox":
                self.input_elems.append(
                    KMenu(
                        self,
                        _input["label"],
                        values=_input["validValues"]))

        for but, cmd in (["Erstellen", self.confirm], [
                         "Abbrechen", self.close_popup]):
            self.buttons.append(
                CTkButton(
                    self,
                    text=but,
                    command=cmd,
                    text_font=(
                        Theme.wow_font,
                        Theme.fontfactor *
                        18)))

        self.grid_widgets()

        self.protocol("WM_DELETE_WINDOW", lambda s=self: self.withdraw())
        self.bind("<Return>", self.confirm)

    def grid_widgets(self) -> None:
        for index, input_elem in enumerate(self.input_elems):
            input_elem.grid(
                row=index, column=0, columnspan=len(
                    self.buttons), sticky="NSEW")
            self.grid_rowconfigure(index, weight=1)

        for index, but in enumerate(self.buttons):
            but.grid(
                row=len(
                    self.input_elems),
                column=index,
                padx=(
                    0,
                    10 if index +
                    1 != len(
                        self.buttons) else 0),
                sticky="NSEW")
            self.grid_columnconfigure(index, weight=1)

    def center(self) -> None:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = int(screen_width * self.relx)
        self.height = int(screen_height * self.rely)

        center_x = int(screen_width / 2 - self.width / 2)
        center_y = int(screen_height / 2 - self.height / 2)

        self.resizable(width=False, height=False)
        self.geometry(f"{self.width}+{self.height}+{center_x}+{center_y}")

    def open_popup(self) -> None:
        if not self.winfo_exists():
            self.create()
        self.deiconify()
        self.center()

    def close_popup(self) -> None:
        if not self.winfo_exists():
            self.create()
        self.withdraw()

    def confirm(self, *_args: any) -> None:
        self.close_popup()
        values = [input_elem.get() for input_elem in self.input_elems]
        [input_elem.reset() for input_elem in self.input_elems]
        self.confirm_call(*values)
