"""
gui/droplist/droplist_table.py

Project: WoW-Dashboard-Client
Created: 30.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from gui.widgets import KCanvas, KTable
from data import API

from ..instances.instance_headers import InstanceColHeader, InstanceRowHeader


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

    def __init__(self, master: any, *args: any, **kwargs: any):
        self.master = master

        # Parents init
        super().__init__(self.master, *args, **kwargs)

        # Other vars
        self.mounts = API.get_all_mounts()

        # GUI Elems

    def grid_widgets(self) -> None:
        self.table.grid(row=0, column=0, sticky="NSEW")
