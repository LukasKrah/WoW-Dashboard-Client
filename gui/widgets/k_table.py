"""
gui/widgets/k_table.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################
from style import Theme

from .k_canvas import KCanvas


##################################################
#                     Code                       #
##################################################

class KTable(KCanvas):
    """
    General table widget
    """
    master: any
    rowheaders: list[any]
    colheaders: list[any]
    cells: any

    row_weight: int
    col_weight: int

    __topleft: any

    __columns: list
    __rows: list
    __values: dict

    column_headerwidgets: dict
    row_headerwidgets: dict
    cell_widgets: dict

    row_offset: int
    col_offset: int

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

        self.__topleft = None
        self.__rows = []
        self.__columns = []
        self.__values = {}

        self.column_headerwidgets = {}
        self.row_headerwidgets = {}
        self.cell_widgets = {}

        self.row_offset = len(self.colheaders)
        self.col_offset = len(self.rowheaders)

    @property
    def topleft(self) -> any:
        return self.__topleft

    @topleft.setter
    def topleft(self, widget: any) -> None:
        self.__topleft = widget
        self.__topleft.grid(
            row=0,
            column=0,
            rowspan=self.row_offset,
            columnspan=self.col_offset,
            sticky="NSEW")

    def __reload(self) -> None:
        """
        Relaod table rowheaders, columnheaders and cells
        """
        # Delete old elems
        del_cells = []

        for row in self.cell_widgets:
            for column in self.cell_widgets[row]:
                if row not in [
                        header["headers"][0]["label"] for header in self.__rows] or column not in [
                        header["headers"][0]["label"] for header in self.__columns]:
                    del_cells.append(f"{row},{column}")
                    self.grid_columnconfigure(
                        self.cell_widgets[row][column].grid_info()["column"], weight=0)
                    self.grid_rowconfigure(
                        self.cell_widgets[row][column].grid_info()["row"], weight=0)
                    self.cell_widgets[row][column].grid_forget()
                    self.cell_widgets[row][column].destroy()

        for del_cel in del_cells:
            splitdel = del_cel.split(",")
            del self.cell_widgets[splitdel[0]][splitdel[1]]

        for header, colrows, typ in ((self.row_headerwidgets, self.__rows, "row"), (
                self.column_headerwidgets, self.__columns, "column")):
            del_headers = []

            for headers in header:
                if headers not in [colrow["headers"][0]["label"]
                                   for colrow in colrows]:
                    del_headers.append(headers)
                    for widget in header[headers]:
                        self.grid_columnconfigure(
                            widget.grid_info()[typ], weight=0)
                        widget.destroy()

            for del_header in del_headers:
                del header[del_header]

        # Column headers
        for col in self.__columns:
            add = False
            for colindex, colheader in enumerate(self.colheaders):
                if col["headers"][0]["label"] not in self.column_headerwidgets or add:
                    if not add:
                        self.column_headerwidgets[col["headers"][0]["label"]] = [
                        ]
                        add = True
                    self.column_headerwidgets[col["headers"][0]["label"]].append(colheader(
                        self, col["headers"][colindex]["label"], col["column"], colindex))
                self.column_headerwidgets[col["headers"][0]["label"]][colindex].set_index(
                    col["column"])
                self.column_headerwidgets[col["headers"][0]["label"]][colindex].grid(
                    row=colindex,
                    column=col["column"] +
                    self.col_offset,
                    sticky="NSEW")
                # self.grid_rowconfigure(
                #     colindex,
                #     weight=col["headers"][colindex]["weight"] if "weight" in col["headers"][colindex]
                #     else self.col_weight)

        # Row headers
        for row in self.__rows:
            add = False
            for rowindex, rowheader in enumerate(self.rowheaders):
                if row["headers"][0]["label"] not in self.row_headerwidgets or add:
                    if not add:
                        self.row_headerwidgets[row["headers"][0]["label"]] = []
                        add = True
                    self.row_headerwidgets[row["headers"][0]["label"]].append(rowheader(
                        self, row["headers"][rowindex]["label"], row["row"], rowindex))
                self.row_headerwidgets[row["headers"][0][
                    "label"]][rowindex].set_index(row["row"])
                self.row_headerwidgets[row["headers"][0]["label"]][rowindex].grid(
                    row=row["row"] + self.row_offset,
                    column=rowindex,
                    sticky="NSEW")
                # self.grid_columnconfigure(
                #     rowindex,
                #     weight=row["headers"][rowindex]["weight"] if "weight" in row["headers"][rowindex]
                #     else self.row_weight)

        # Table
        for rowindex, row in enumerate(self.__rows):
            for colindex, col in enumerate(self.__columns):
                if row["headers"][0]["label"] not in self.cell_widgets:
                    self.cell_widgets[row["headers"][0]["label"]] = {}
                if col["headers"][0]["label"] not in self.cell_widgets[row["headers"][0]["label"]]:
                    self.cell_widgets[row["headers"][0]["label"]][col["headers"][0]["label"]] = self.cells(
                        self, col["headers"][0]["label"], row["headers"][0]["label"])
                self.cell_widgets[row["headers"][0]["label"]
                                  ][col["headers"][0]["label"]].reload()
                self.cell_widgets[row["headers"][0]["label"]][col["headers"][0]["label"]].grid(
                    row=row["row"] +
                    self.row_offset,
                    column=col["column"] +
                    self.col_offset,
                    sticky="NSEW")

        # Weights
        for row in range(self.row_offset):
            self.grid_rowconfigure(row, weight=self.row_weight)

        for col in range(self.col_offset):
            self.grid_columnconfigure(col, weight=self.col_weight)

        for row in self.__rows:
            self.grid_rowconfigure(
                row["row"] + self.row_offset,
                weight=self.row_weight)
        try:
            self.grid_rowconfigure(
                max([row["row"] + self.row_offset for row in self.__rows]) + 1, weight=0)
        except ValueError:
            ...

        for column in self.__columns:
            self.grid_columnconfigure(
                column["column"] + self.col_offset,
                weight=self.col_weight)
        try:
            self.grid_columnconfigure(max(
                [column["column"] + self.col_offset for column in self.__columns]) + 1, weight=0)
        except ValueError:
            ...

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
