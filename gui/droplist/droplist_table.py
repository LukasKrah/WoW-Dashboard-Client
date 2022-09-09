"""
gui/droplist/droplist_table.py

Project: WoW-Dashboard-Client
Created: 30.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import messagebox
from time import time

from data import API, DroplistColumns, DroplistSettings
from gui.widgets import KCanvas, KTable, KTableCell

from .droplist_widgets import DroplistColumnHeader, DroplistRowHeader, DroplistNavBar


##################################################
#                     Code                       #
##################################################

class DroplistTable(KCanvas):
    """
    Droplist table to display dropped mounts
    """
    master: any
    mounts: dict

    table: KTable
    navbar: DroplistNavBar

    def __init__(self, master: any, *args: any, **kwargs: any):
        self.master = master

        # Parents init
        super().__init__(self.master, *args, **kwargs)

        # Other vars
        self.mounts = API.get_all_mounts()

        # GUI Elems
        self.table = KTable(self, [DroplistRowHeader], [DroplistColumnHeader], KTableCell)
        self.navbar = DroplistNavBar(self, new_drop_callback=self.add_drop)

        self.grid_widgets()
        self.reload_table()

    def add_drop(
            self,
            name: str,
            trys: str,
            full: str) -> None:
        if name.lower() in DroplistSettings.values:
            messagebox.showwarning("Drop hinzufügen",
                                   "Dieses Mount existiert bereits!")
        else:
            DroplistSettings[name.lower()] = {
                "label": name,
                "row": len(DroplistSettings.values),
                "columns": {
                    "mount": name,
                    "date": time(),
                    "trys": f"{trys}/{full}"
                }
            }

        self.reload_table()

    def grid_widgets(self) -> None:
        self.grid_rowconfigure(0, weight=10)
        self.grid_columnconfigure(0, weight=10)
        self.table.grid(row=0, column=0, sticky="NSEW")
        self.navbar.grid(row=1, column=0, sticky="NSEW")

    def reload_table(self) -> None:
        rows = [{"row": DroplistSettings[row]["row"],
                 "headers": [{"label": DroplistSettings[row]["label"],
                              "name": row}]}
                for row in DroplistSettings.values]
        columns = [{"column": DroplistColumns[column]["column"],
                    "headers": [{"label": DroplistColumns[column]["label"],
                                 "name": column}]}
                   for column in DroplistColumns.values]

        self.table.reload(
            rows=rows,
            columns=columns,
            values=DroplistSettings.values)
        self.table.grid_columnconfigure(0, weight=0)
