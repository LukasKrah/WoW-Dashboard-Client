"""
gui/widgets/k_popup.py

Project: WoW-Dashboard-Client
Created: 14.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import CTkToplevel, CTkButton, CTk
from typing import Callable

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
            confirm_call: Callable[[any], None],
            **kwargs: any) -> None:
        self.master = master
        self.name = name
        self.inputs = inputs
        self.args = args
        self.relx = relx
        self.rely = rely
        self.confirm_call = confirm_call
        self.kwargs = kwargs

        super().__init__(self.master, *self.args, *self.kwargs)
        self.iconify()
        self.withdraw()
        self.update()

        self.title(self.name)
        self.configure(background=Theme.background1)
        self.attributes("-topmost", True)
        self.wm_iconbitmap("style/images/wow_icon.ico")

        self.input_elems = []
        self.buttons = []

        for _input in self.inputs:
            if _input["type"] == "InputText":
                self.input_elems.append(
                    KEntry(
                        self,
                        _input["label"],
                        value=_input["value"] if "value" in _input else None))

            elif _input["type"] == "OptionMenu":
                self.input_elems.append(
                    KOptionMenu(
                        self,
                        _input["label"],
                        values=_input["validValues"],
                        value=_input["value"] if "value" in _input else None))

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
                    text_color=Theme.text_color,
                    fg_color=Theme.primary_middle,
                    hover_color=Theme.primary_light,
                    text_font=(
                        Theme.wow_font,
                        Theme.fontfactor *
                        18)))

        self.grid_widgets()

        self.protocol("WM_DELETE_WINDOW", lambda s=self: self.withdraw())
        self.bind("<Return>", self.confirm)
        self.bind("<Escape>", self.close_popup)

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
                pady=(20, 0),
                padx=(
                    0,
                    10 if index +
                    1 != len(
                        self.buttons) else 0),
                sticky="NSEW")
            self.grid_columnconfigure(index, weight=1)

    def center(self) -> None:
        root: CTk = self.nametowidget(".")

        rootx = root.winfo_rootx()
        rooty = root.winfo_rooty()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        self.width = self.winfo_width()
        self.height = self.winfo_height()

        center_x = int((root_width / 2 - self.width / 2))
        center_y = int((root_height / 2 - self.height / 2))

        posx = rootx + center_x
        posy = rooty + center_y
        self.resizable(width=False, height=False)
        self.geometry(
            f"+{posx}+{posy}")

    def open_popup(self, *_args: any) -> None:
        for input_elem in self.input_elems:
            input_elem.reset()
        self.center()
        self.deiconify()

    def close_popup(self, *_args: any) -> None:
        self.withdraw()

    def set_values(self, *args: any) -> None:
        for index, input_elem in enumerate(self.input_elems):
            input_elem.set(args[index])

    def confirm(self, *_args: any) -> None:
        self.close_popup()
        values = [input_elem.get() for input_elem in self.input_elems]
        [input_elem.reset() for input_elem in self.input_elems]
        self.confirm_call(*values)
