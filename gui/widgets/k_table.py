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

    topleft: any

    __columns: list
    __rows: list
    __values: dict

    def __init__(
            self,
            master,
            rowheaders: list[any],
            colheaders: list[any],
            cells: any,
            *args,
            **kwargs) -> None:
        """
        Create table (call .reload to load table)
        :param master: master widget (e.g: root)
        :param rowheaders: Row-header widgets (will pass master, rowname and header-index as positional arg)
        :param colheaders: Col-header widgets (will pass master, colname and header-index as positional arg)
        :param cells: Cells widgets (will pass master, first colname and first rowname as positional args)
        """
        self.master = master
        self.rowheaders = rowheaders
        self.colheaders = colheaders
        self.cells = cells

        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)

        self.topleft = None
        self.__rows = []
        self.__columns = []
        self.__values = {}

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
        for index, col in enumerate(self.__columns):
            for colindex, colheader in enumerate(self.colheaders):
                lab = colheader(self, col[colindex], colindex)
                lab.grid(
                    row=colindex,
                    column=index +
                    col_offset,
                    sticky="NSEW")

        # Row headers
        for index, row in enumerate(self.__rows):
            for rowindex, rowheader in enumerate(self.rowheaders):
                lab = rowheader(self, row[rowindex], rowindex)
                lab.grid(
                    row=index + row_offset,
                    column=rowindex,
                    sticky="NSEW")

        # Table
        for rowindex, row in enumerate(self.__rows):
            for colindex, col in enumerate(self.__columns):
                lab = self.cells(self, col=col[0], row=row[0])
                lab.grid(
                    row=rowindex +
                    row_offset,
                    column=colindex +
                    col_offset,
                    sticky="NSEW")

        # Weights
        for index in range(len(self.__columns) + col_offset):
            self.grid_columnconfigure(index, weight=1)

        for index in range(len(self.__rows) + row_offset):
            self.grid_rowconfigure(index, weight=1)

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
