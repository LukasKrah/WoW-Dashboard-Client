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

from data import Theme


##################################################
#                     Code                       #
##################################################

class Table(CTkCanvas):
    columns: list
    rows: list
    values: dict

    def __init__(self, master, columns: list | None = None, rows: list | None = None, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(bd=0, highlightthickness=0, background=Theme.background3)

        if rows is None:
            rows = []
        if columns is None:
            columns = []

        self.rows = rows
        self.columns = columns
        self.values = {}

    def reload(self):
        self.columns = list(self.values.keys())
        self.rows = list({row: 0 for col in self.values for row in self.values[col]}.keys())

        # Column headers
        for index, col in enumerate(self.columns):
            lab = CTkLabel(self, text=col, bg_color=Theme.background3)
            lab.grid(row=0, column=index+1, sticky="NSEW")
            self.grid_columnconfigure(index+1, weight=1)
        add = CTkButton(self, text="+")
        add.grid(row=0, column=len(self.columns)+1, sticky="NSEW")

        # Row headers
        for index, row in enumerate(self.rows):
            lab = CTkLabel(self, text=row, bg_color=Theme.background3)
            lab.grid(row=index+1, column=0, sticky="NSEW")
        add = CTkButton(self, text="+")
        add.grid(row=len(self.rows) + 1, column=0, sticky="NSEW")

        for index in range(len(self.columns)+2):
            self.grid_columnconfigure(index, weight=1)

        for index in range(len(self.rows)+2):
            self.grid_rowconfigure(index, weight=1)

        # Table
        for colindex, col in enumerate(self.columns):
            for rowindex, row in enumerate(self.rows):
                lab = CTkButton(self, text="", highlightthickness=1, highlightbackground="black",
                                fg_color="grey", hover_color="darkgrey")
                lab.configure(command=lambda label=lab: self.values[col][row](label))
                lab.grid(row=rowindex+1, column=colindex+1, sticky="NSEW")

        # for col in self.values:
        #     for row in self.values[col]:
        #         cmd = self.values[col][row] if self.values[col][row] else self.basic_func
        #         lab = CTkCanvas(self, highlightthickness=1, highlightbackground="red", bg="grey")
        #         lab.bind("<Button-1>", lambda label=lab, command=cmd: self.click(label, command))
        #         lab.grid(row=self.rows.index(row)+1, column=self.columns.index(col)+1, sticky="NSEW")

    def click(self, field: CTkLabel, command: Callable) -> None:
        print("Field", field)
        command(field)
