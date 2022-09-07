"""
gui/widgets/k_tablecells.py

Project: WoW-Dashboard-Client
Created: 07.09.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import Event

from style import Theme

from .k_canvas import KCanvas
from .k_table import KTable


##################################################
#                     Code                       #
##################################################

class KTableCell(KCanvas):
    """
    Custom table cell
    """
    master: KTable
    col_name: str
    row_name: str
    label: str

    width: int
    height: int

    label_id: int

    def __init__(self,
                 master: KTable,
                 col_name: str,
                 row_name: str,
                 *args,
                 label: str | None = None,
                 **kwargs
                 ) -> None:
        self.master = master
        self.col_name = col_name
        self.row_name = row_name
        self.label = label if label else self.master.values[row_name]["columns"][col_name]

        super().__init__(self.master, *args, **kwargs)

        self.configure(bg=Theme.background2)

        self.label_id = self.create_text(0, 0, text=self.label, anchor="center", fill=Theme.text_color,
                                         font=(Theme.font, Theme.fontfactor*18))

        self.width, self.height = 0, 0

        self.bind("<Configure>", self.__resize)

    def reload(self) -> None:
        self.coords(self.label_id, self.width//2, self.height//2)

    def __resize(self, event: Event) -> None:
        self.width = event.width
        self.height = event.height

        self.reload()
