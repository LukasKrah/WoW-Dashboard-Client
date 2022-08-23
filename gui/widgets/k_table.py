"""
gui/widgets/k_table.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *

from style import Theme


##################################################
#                     Code                       #
##################################################

class KTable(CTkCanvas):
    """
    General table widget
    """
    master: any
    rowheaders: list[any]
    colheaders: list[any]
    cells: any

    row_weight: int
    col_weight: int

    topleft: any

    __columns: list
    __rows: list
    __values: dict

    column_headerwidgets: list
    row_headerwidgets: list

    def __init__(
            self,
            master,
            rowheaders: list[any],
            colheaders: list[any],
            cells: any,
            *args,
            row_weight: int | None = 10,
            col_weight: int | None = 10,
            **kwargs) -> None:
        """
        Create table (call .reload to load table)
        :param master: master widget (e.g: root)
        :param rowheaders: Row-header widgets (will pass master, rowname, rowindex and header-index as positional arg)
        :param colheaders: Col-header widgets (will pass master, colname, colindex amd header-index as positional arg)
        :param cells: Cells widgets (will pass master, first colname and first rowname as positional args)
        """
        self.master = master
        self.rowheaders = rowheaders
        self.colheaders = colheaders
        self.cells = cells

        self.row_weight = row_weight
        self.col_weight = col_weight

        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)

        self.topleft = None
        self.__rows = []
        self.__columns = []
        self.__values = {}

        self.column_headerwidgets = []
        self.row_headerwidgets = []

    def __reload(self) -> None:
        """
        Relaod table rowheaders, columnheaders and cells
        """
        # Delete old elems
        for widget in self.grid_slaves():
            self.grid_columnconfigure(widget.grid_info()["column"], weight=0)
            self.grid_rowconfigure(widget.grid_info()["row"], weight=0)
            widget.grid_forget()
            del widget
        self.row_headerwidgets = []
        self.column_headerwidgets = []

        row_offset = len(self.colheaders)
        col_offset = len(self.rowheaders)

        # TopLeft
        if self.topleft is not None:
            self.topleft.grid(
                row=0,
                column=0,
                rowspan=row_offset,
                columnspan=col_offset,
                sticky="NSEW")

        # Column headers
        self.grid_rowconfigure(0, weight=self.row_weight)
        self.grid_columnconfigure(0, weight=self.col_weight)

        try:
            for index in range(max([col["column"]
                                    for col in self.__columns]) + 1):
                self.column_headerwidgets.append([])
        except ValueError:
            ...

        for index, col in enumerate(self.__columns):
            self.column_headerwidgets.append([])
            for colindex, colheader in enumerate(self.colheaders):
                self.column_headerwidgets[col["column"]].append(colheader(
                    self, col["headers"][colindex]["label"], col["column"], colindex))
                self.column_headerwidgets[col["column"]][colindex].grid(
                    row=colindex,
                    column=col["column"] +
                    col_offset,
                    sticky="NSEW")
                self.grid_rowconfigure(
                    colindex,
                    weight=col["headers"][colindex]["weight"] if "weight" in col["headers"][colindex]
                    else self.col_weight)

        # Row headers
        try:
            for index in range(max([row["row"] for row in self.__rows]) + 1):
                self.row_headerwidgets.append([])
        except ValueError:
            ...

        for index, row in enumerate(self.__rows):
            for rowindex, rowheader in enumerate(self.rowheaders):
                self.row_headerwidgets[row["row"]].append(rowheader(
                    self, row["headers"][rowindex]["label"], row["row"], rowindex))
                self.row_headerwidgets[row["row"]][rowindex].grid(
                    row=row["row"] + row_offset,
                    column=rowindex,
                    sticky="NSEW")
                self.grid_columnconfigure(
                    rowindex,
                    weight=row["headers"][rowindex]["weight"] if "weight" in row["headers"][rowindex]
                    else self.row_weight)

        # Table
        for rowindex, row in enumerate(self.__rows):
            for colindex, col in enumerate(self.__columns):
                lab = self.cells(
                    self,
                    col["headers"][0]["label"],
                    row["headers"][0]["label"])
                lab.grid(
                    row=row["row"] +
                    row_offset,
                    column=col["column"] +
                    col_offset,
                    sticky="NSEW")

        # Weights
        for row in self.__rows:
            self.grid_rowconfigure(
                row["row"] + row_offset,
                weight=self.row_weight)
        for column in self.__columns:
            self.grid_columnconfigure(
                column["column"] + col_offset,
                weight=self.col_weight)

    def reload(
            self,
            rows: list | None = None,
            columns: list | None = None,
            values: list | None = None) -> None:
        """
        Reload table rows, columns and cells (__values)

        :param rows: Optional updated rows
        :param columns: Optional updated columns
        :param values: Optional updated cell-__values
        """
        self.__rows = rows if rows is not None else self.__rows
        self.__columns = columns if columns is not None else self.__columns
        self.__values = values if values is not None else self.__values

        self.__reload()

    @property
    def rows(self) -> list:
        return self.__rows

    @rows.setter
    def rows(self, rows: list) -> None:
        self.__rows = rows
        self.__reload()

    @property
    def columns(self) -> list:
        return self.__columns

    @columns.setter
    def columns(self, columns: list) -> None:
        self.__columns = columns
        self.__reload()

    @property
    def values(self) -> dict:
        return self.__values

    @values.setter
    def values(self, values: dict) -> None:
        self.__values = values
        self.__reload()
