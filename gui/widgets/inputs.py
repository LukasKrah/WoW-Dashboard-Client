"""
gui/widgets/inputs.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *

from style import Theme


##################################################
#                     Code                       #
##################################################

class KEntry(CTkCanvas):
    label: str
    entry: CTkEntry
    valid_symbols: str | None
    textvar: StringVar

    def __init__(self, master, label: str, *args: any, valid_symbols: str | None = None, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(bd=0, highlightthickness=0, background=Theme.background1)

        self.label = label
        self.valid_symbols = valid_symbols

        self.create_text(10, 10, text=self.label, anchor="nw", font=(Theme.wow_font2, Theme.fontfactor*18))

        self.textvar = StringVar()
        self.entry = CTkEntry(self, text_font=(Theme.wow_font2, Theme.fontfactor*18), width=300,
                              textvariable=self.textvar)
        self.textvar.trace_add("write", self.__change_text)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.entry.grid(row=0, column=0, sticky="NSEW", pady=((Theme.fontfactor*18)+30, 0))

    def __change_text(self, *args) -> None:
        newstring = ""
        for let in self.textvar.get():
            if self.valid_symbols:
                if let in self.valid_symbols:
                    newstring += let
            else:
                newstring += let
        self.textvar.set(newstring)

    def get(self) -> str:
        return self.entry.get()


class KOptionMenu(CTkCanvas):
    label: str
    optionMenu: CTkOptionMenu
    values: list[str]

    def __init__(self, master, label: str, values: list[str], *args: any, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(bd=0, highlightthickness=0, background=Theme.background1)

        self.label = label
        self.values = values

        self.create_text(10, 10, text=label, font=(Theme.wow_font2, Theme.fontfactor*18), anchor="nw")
        self.optionMenu = CTkOptionMenu(self, values=self.values, text_font=(Theme.wow_font2, Theme.fontfactor*18))
        self.optionMenu.dropdown_menu.configure(tearoff=False)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.optionMenu.grid(row=0, column=0, sticky="NSEW", pady=((Theme.fontfactor*18)+30, 0))

    def get(self) -> str:
        return self.optionMenu.get()


class KMenu(CTkCanvas):
    label: str
    menuButton: Menubutton
    menu: Menu
    values: list[str]
    selection: dict

    def __init__(self, master, label: str, values: list[str], *args: any, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(bd=0, highlightthickness=0, background=Theme.background1)

        self.label = label
        self.values = values

        self.create_text(10, 10, text=label, font=(Theme.wow_font2, Theme.fontfactor*18), anchor="nw")
        self.menuButton = Menubutton(self, text=self.label,
                                     indicatoron=True)
        self.menu = Menu(self.menuButton, tearoff=False)
        self.menuButton.configure(menu=self.menu)

        self.selection = {}
        for value in self.values:
            self.selection[value] = IntVar(value=0)
            self.menu.add_checkbutton(label=value, variable=self.selection[value],
                                      onvalue=1, offvalue=0)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.menuButton.grid(row=0, column=0, sticky="NSEW", pady=((Theme.fontfactor * 18) + 30, 0))

    def get(self) -> dict:
        return self.selection
