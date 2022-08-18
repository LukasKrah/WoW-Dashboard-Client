"""
gui/widgets/table.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable
from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk

from style import Theme
from data import Settings


##################################################
#                     Code                       #
##################################################

class Table(CTkCanvas):
    columns: list
    rows: list
    values: dict

    def __init__(
            self,
            master,
            columns: list | None = None,
            rows: list | None = None,
            rowheader=None,
            colheader=None,
            cells=None,
            *args,
            **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)

        self.cells = cells
        self.rowheader = rowheader
        self.colheader = colheader

        if rows is None:
            rows = []
        if columns is None:
            columns = []

        self.rows = rows
        self.columns = columns
        self.values = {}

    def reload(self):
        self.rows = list(self.values.keys())
        self.columns = [char["characterName"] for char in Settings["chars"]]
        for instance in self.values:
            for diff in self.values[instance]["difficulty"]:
                for char in self.values[instance]["difficulty"][diff]["chars"]:
                    if char not in self.columns:
                        self.columns.append(char)

        # Delete old elems
        for widget in self.grid_slaves():
            self.grid_columnconfigure(widget.grid_info()["column"], weight=0)
            self.grid_rowconfigure(widget.grid_info()["row"], weight=0)
            widget.grid_forget()
            del widget

        # Column headers
        for index, col in enumerate(self.columns):
            lab = self.colheader(self, text=col, image=None)
            lab.grid(row=0, column=index + 1, sticky="NSEW")

        # Row headers
        for index, row in enumerate(self.rows):
            lab = self.rowheader(
                self, text=row, image=self.values[row]["image"])

            lab.grid(row=index + 1, column=0, sticky="NSEW")

        # Table
        for rowindex, row in enumerate(self.rows):
            for colindex, col in enumerate(self.columns):
                lab = self.cells(self, col=col, row=row)
                lab.grid(row=rowindex + 1, column=colindex + 1, sticky="NSEW")

        for index in range(len(self.columns) + 1):
            self.grid_columnconfigure(index, weight=1)

        for index in range(len(self.rows) + 1):
            self.grid_rowconfigure(index, weight=1)

        # for col in self.values:
        #     for row in self.values[col]:
        #         cmd = self.values[col][row] if self.values[col][row] else self.basic_func
        #         lab = CTkCanvas(self, highlightthickness=1, highlightbackground="red", bg="grey")
        #         lab.bind("<Button-1>", lambda label=lab, command=cmd: self.click(label, command))
        #         lab.grid(row=self.rows.index(row)+1, column=self.columns.index(col)+1, sticky="NSEW")

    def add(self, col_row_list: list, column: int, row: int) -> None:
        ...

    def click(self, field: CTkLabel, command: Callable) -> None:
        print("Field", field)
        command(field)
