"""
gui/droplist/droplist_headers.py

Project: WoW-Dashboard-Client
Created: 07.09.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Literal, Callable
from customtkinter import CTkButton
from tkinter import Misc

from gui.widgets import KTableHeader, KCanvas, KPopUp
from data import DroplistColumns
from style import Theme


##################################################
#                     Code                       #
##################################################

class DroplistColumnHeader(KTableHeader):
    def __init__(self,
                 master: any,
                 name: str,
                 label: str,
                 index: int,
                 header_index: int,
                 move_callback: Callable[[str, int, int], None] | None = DroplistColumns.move,
                 typ: Literal["row", "column"] | None = "column") -> None:
        super().__init__(
            master=master,
            name=name,
            labels=[label],
            index=index,
            header_index=header_index,
            typ=typ,
            move_callback=move_callback)


class DroplistRowHeader(KCanvas):
    def __init__(self,
                 master: any,
                 _name: str,
                 _label: str,
                 _index: int,
                 _header_index: int
                 ) -> None:
        super().__init__(master=master)
        self.configure(background=Theme.background3)


class DroplistNavBar(KCanvas):
    master: Misc
    new_drop_callback: Callable[[str, str, str], None]

    add: CTkButton
    add_popup: KPopUp

    def __init__(
            self,
            master: Misc,
            new_drop_callback: Callable[[str, str, str], None],
            *args: any,
            **kwargs: any) -> None:
        self.master = master
        self.new_drop_callback = new_drop_callback

        super().__init__(master, *args, **kwargs)
        self.configure(background=Theme.background3)

        self.add_popup = KPopUp(self,
                                "Neuer Drop",
                                inputs=[{"type": "InputText",
                                         "label": "Mount"},
                                        {"type": "InputText",
                                         "label": "Versuche"},
                                        {"type": "InputText",
                                         "label": "von Versuchen:"}
                                        ],
                                confirm_call=self.new_drop_callback)

        self.add = CTkButton(self,
                             text="Drop hinzufügen",
                             fg_color=Theme.primary_middle,
                             hover_color=Theme.primary_light,
                             text_color=Theme.text_color,
                             text_font=(
                                 Theme.wow_font,
                                 Theme.fontfactor * 18),
                             command=self.add_popup.open_popup)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.add.grid(row=0, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=10)
        self.grid_columnconfigure(0, weight=10)
