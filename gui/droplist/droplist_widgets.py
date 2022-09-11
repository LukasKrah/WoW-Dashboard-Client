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
from time import strftime, gmtime
from tkinter import Misc

from gui.widgets import KTableHeader, KCanvas, KPopUp, KTableCell, KTable
from data import DroplistColumns
from style import Theme


##################################################
#                     Code                       #
##################################################

class DroplistCell(KTableCell):
    master: KTable

    def __init__(self,
                 master: KTable,
                 col_name: str,
                 row_name: str,
                 ) -> None:
        self.master = master

        match col_name:
            case "date":
                week = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
                week_day = week[int(strftime("%u", gmtime(self.master.values[row_name]["columns"][col_name]+7200)))-1]

                super().__init__(master, col_name, row_name,
                                 label=strftime(f"%H:%M:%S {week_day} %d.%m.%Y",
                                                gmtime(self.master.values[row_name]["columns"][col_name]+7200)))
            case "trys":
                splitlab = self.master.values[row_name]["columns"][col_name].split("/")
                prop = self.get_propabilty(int(splitlab[0]), int(splitlab[1]))

                label = f"Versuche: {splitlab[0]}\n"\
                        f"Ø benötige Versuche: {splitlab[1]}\n"\
                        f"Wahrscheinlichkeit: {prop*100}%"

                super().__init__(master, col_name, row_name,
                                 label=label)

                self.configure(background='#%02x%02x%02x' % (int(255*prop), int(255*(1-prop)), 0))
                if prop < 0.5:
                    self.itemconfigure(self.label_id, fill=Theme.text_color_reverse)

            case _:
                super().__init__(master, col_name, row_name)

    def get_propabilty(self, trys: int, full: int) -> float:
        factor = 1 / full
        prop = factor
        num = factor
        for index in range(trys - 1):
            num *= (1 - factor)
            prop += num

        return round(prop, 4)


class DroplistColumnHeader(KTableHeader):
    def __init__(self,
                 master: any,
                 name: str,
                 label: str,
                 index: int,
                 header_index: int,
                 move_callback: Callable[[str,
                                          int,
                                          int],
                                         None] | None = DroplistColumns.move,
                 typ: Literal["row",
                              "column"] | None = "column") -> None:
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
