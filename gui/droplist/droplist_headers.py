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

from gui.widgets import KTableHeader
from data import DroplistSettings, DroplistColumns


##################################################
#                     Code                       #
##################################################

class DroplistRowHeader(KTableHeader):
    def __init__(self,
                 master: any,
                 name: str,
                 label: str,
                 index: int,
                 header_index: int,
                 move_callback: Callable[[str, int, int], None] | None = DroplistSettings.move,
                 typ: Literal["row", "column"] | None = "row") -> None:
        super().__init__(
            master=master,
            name=name,
            labels=[label],
            index=index,
            header_index=header_index,
            typ=typ,
            move_callback=move_callback)


class DroplistColumnHeader(DroplistRowHeader):
    def __init__(self,
                 master: any,
                 name: str,
                 label: str,
                 index: int,
                 header_index: int
                 ) -> None:
        super().__init__(
            master=master,
            name=name,
            label=label,
            index=index,
            header_index=header_index,
            typ="column",
            move_callback=DroplistColumns.move
        )
