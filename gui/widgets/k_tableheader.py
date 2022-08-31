"""
gui/widgets/k_tableheader.py

Project: WoW-Dashboard-Client
Created: 30.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Literal, Callable, Union
from tkinter import Event

from .k_contextmenu import KContextMenu
from .k_canvas import KCanvas
from .k_table import KTable
from .k_image import KImage


##################################################
#                     Code                       #
##################################################

class KTableHeader(KCanvas):
    """
    Custom Table Header Widget
    """
    # Params
    master: KTable
    name: str
    labels: list[str]
    index: int
    header_index: int
    typ: Literal["row", "column"]

    image: KImage | None
    move_callback: Callable[[str, int, int], any]
    context_menu: list[dict[Literal["label", "command"], Union[str, Callable[[None], any]]]]

    # Style params
    fg_color: str
    text_color: str
    text_font: tuple[str, int]
    move_fg_color: str
    move_text_color: str
    move_text_font: tuple[str, int]
    movemark_color: str
    movemark_width: int

    # Vars for drag'n'drop
    index: int
    __dragindex: int
    __all_header_elems: dict[str, list["KTableHeader"]]
    __all_header_by_index: list[list["KTableHeader"]]

    # GUI Vars
    width: int
    height: int

    context_menu_elem: KContextMenu | None
    label_ids = list[int]

    def __init__(
            self,
            master: KTable,
            name: str,
            labels: list[str],
            index: int,
            header_index: int,
            typ: Literal["row", "column"],
            *args: any,
            image: KImage | None = None,
            move_callback: Callable[[str, int], any] | None = None,
            context_menu: list[dict[Literal["label", "command"], Union[str, Callable[[None], any]]]] | None = None,

            fg_color: str | None = "#222222",
            text_color: str | None = "#CCCCCC",
            text_font: tuple[str, int] | None = ("Arial", 18),
            move_fg_color: str | None = "#333333",
            move_text_color: str | None = "#CCCCCC",
            move_text_font: tuple[str, int] | None = ("Arial", 18),
            movemark_color: str | None = "#0000FF",
            movemark_width: int | None = 20,
            **kwargs: any) -> None:
        """
        Create custom Table Header

        :param master: Table where this header is placed in (passed by KTable)
        :param name: Name of the header (only for callbacks) (passed by KTable)
        :param labels: Labels to show in header (passed by KTable)
        :param index: Index of the Header in the row / column (passed by KTable)
        :param header_index: Index of the Header (passed by KTable)
        :param typ: Whether this header is a row or column-header
        :param image: Image to show in header
        :param move_callback: Callback for moving rows/cols. Will pass name, current index and new index
        :param context_menu: Right click context menu
        :param fg_color: Normal foreground color
        :param text_color: Normal text color
        :param text_font: Normal text font
        :param move_fg_color: Foreground color when header is "dragged"
        :param move_text_color: Text color when header is "dragged"
        :param move_text_font: Text font when header is "dragged"
        :param movemark_color: Drag'n'drop locationmark color
        :param movemark_width: Drag'n'drop locationmark width
        """
        print("NEW", master, name, labels, typ)
        # Params
        self.master = master
        self.name = name
        self.labels = labels
        self.index = index
        self.header_index = header_index
        self.typ = typ

        self.image = image
        self.move_callback = move_callback
        self.context_menu = context_menu

        # Style params
        self.fg_color = fg_color
        self.text_color = text_color
        self.text_font = text_font
        self.move_fg_color = move_fg_color
        self.move_text_color = move_text_color
        self.move_text_font = move_text_font
        self.movemark_color = movemark_color
        self.movemark_width = movemark_width

        # Parent init
        super().__init__(master, *args, **kwargs)

        # Vars for drag'n'drop
        self.__dragindex = 0
        self.__all_header_elems = self.master.row_headerwidgets if self.typ == "row" \
            else self.master.column_headerwidgets
        self.__all_header_by_index = []

        # GUI vars
        self.width, self.height = 100, 100
        self.label_ids = []

        self.context_menu_elem = KContextMenu(self, self.context_menu) if self.context_menu else None
        if self.context_menu_elem:
            self.bind("<Button-3>", self.context_menu_elem.popup)

        if self.move_callback:
            self.bind("<ButtonPress-1>", self._move_dragclickdown)
            self.bind("<B1-Motion>", self._move_dragdown)
            self.bind("<ButtonRelease-1>", self._move_dragup)

        self.bind("<Configure>", self.__resize)

        self._create_widgets()

    def _create_widgets(self) -> None:
        """
        Create all "widgets"
        """
        if self.image:
            self.create_image(0, 0, image=self.image.imgTk, anchor="center", tags=["image"])

        for label in self.labels:
            self.label_ids.append(self.create_text(0, 0, text=label))

        self.reload(full_reformat=True)

    # --- GUI Functions --- #
    def reload(self, full_reformat: bool | None = False, grey_out: bool | None = False) -> None:
        """
        Reload (mainly called after Resize) position and sizes
        :param full_reformat: Whether everything (fill, font, anchor) should be set
        :param grey_out: If the image of the header should be greyed out or not
        """
        if full_reformat:
            self.configure(bg=self.fg_color)

        labels_len = len(self.labels) + 1
        for index, label_id in enumerate(self.label_ids):
            self.coords(label_id, self.width//2, (self.height / labels_len) * (index + 1))
            if full_reformat:
                self.itemconfigure(label_id, fill=self.text_color, font=self.text_font, anchor="center")

        if self.image:
            self.image.resize(self.width, self.height, "cover")
            self.coords("image", self.width // 2, self.height // 2)
            self.itemconfigure("image", image=self.image.imgTk_greyout if grey_out else self.image.imgTk,
                               anchor="center")

    def __resize(self, event: Event) -> None:
        self.height = event.height
        self.width = event.width
        self.reload()

    # --- Move (Drag'n'drop) functions --- #
    def _move_dragdown(self, event: Event) -> None:
        """
        Move (Drag'n'drop) animation
        :param event: Tk-Bind event
        """
        match self.typ:
            case "column":
                eventcoord = event.x
                size = self.width
            case "row" | _:
                eventcoord = event.y
                size = self.height

        self.__all_header_by_index = [[] for _header in self.__all_header_elems]
        for header in self.__all_header_elems:
            self.__all_header_by_index[self.__all_header_elems[header][
                0].index] = self.__all_header_elems[header]

        # Selection effect

        for header in self.__all_header_by_index[self.index]:
            if header.image:
                header.reload(grey_out=True)
            else:
                header.configure(bg=header.move_fg_color)
            for label_id in header.label_ids:
                header.itemconfigure(label_id, font=header.move_text_font, fill=header.move_text_color)

        # Calculate dragindex
        modify = 0.5 if eventcoord >= 0 else -0.5
        self.__dragindex = int(
            ((eventcoord / size) + modify)) + self.index

        # Delete old Movemarks
        self._movemark_delete()

        # Create new Movemarks
        try:
            for header in self.__all_header_by_index[self.__dragindex - 1]:
                header._movemark_pre() if self.__dragindex > 0 else None
        except (IndexError, KeyError):
            ...
        try:
            for header in self.__all_header_by_index[self.__dragindex]:
                header._movemark_next()
        except (IndexError, KeyError):
            ...

        # idk
        self.__dragindex = 0 if self.__dragindex < 0 else self.__dragindex
        self.__dragindex = len(
            self.__all_header_elems) if self.__dragindex > len(
            self.__all_header_elems) else self.__dragindex

    def _move_dragclickdown(self, event: Event) -> None:
        """
        Clickdown moving event
        :param event: Tkinter Bind-Event
        """
        for header_list in self.__all_header_elems:
            for header in self.__all_header_elems[header_list]:
                header.index = header.master.get_index(header.typ, header.name)
                print(header, "new index", header.index)
        self._move_dragdown(event)

    def _move_dragup(self, _event: Event) -> None:
        """
        Final moving function
        :param _event: Tkinter Bind-Event
        """

        for header in self.__all_header_by_index[self.index]:
            header._movemark_delete()
            header.reload(full_reformat=True)

        self.__dragindex += (-1 if self.index <= self.__dragindex - 1 else 0)

        self.move_callback(self.name, self.index, self.__dragindex)
        self.master.master.master.reload_table()

    def _movemark_pre(self, tag: str | None = "movemark") -> None:
        """
        Draw a line between self and the previous elem in the header-row/column
        :param tag: Tag of the line
        """
        match self.typ:
            case "column":
                self.create_line(
                    self.width, 0, self.width, self.height,
                    fill=self.movemark_color,
                    width=self.movemark_width,
                    tags=[tag]
                )
            case "row":
                self.create_line(
                    0, self.height, self.width, self.height,
                    fill=self.movemark_color,
                    width=self.movemark_width,
                    tags=[tag]
                )

    def _movemark_next(self, tag: str | None = "movemark") -> None:
        """
        Draw a line between self and the next elem in the header-row/column
        :param tag: Tag of the line
        """
        match self.typ:
            case "column":
                self.create_line(
                    0, 0, 0, self.height,
                    fill=self.movemark_color,
                    width=self.movemark_width,
                    tags=[tag]
                )
            case "row":
                self.create_line(
                    0, 0, self.width, 0,
                    fill=self.movemark_color,
                    width=self.movemark_width,
                    tags=[tag]
                )

    def _movemark_delete(self, tag: str | None = "movemark") -> None:
        """
        Delete Move-Mark in ALL headers of the header-row/column
        :param tag: Tag of the lines to delete
        """
        for header_list in self.__all_header_elems:
            for header in self.__all_header_elems[header_list]:
                header.delete(tag)


class KTableRowHeader(KTableHeader):
    """
    Default Row-Header widget
    """
    def __init__(
            self,
            master: KTable,
            name: str,
            *args: any,
            **kwargs: any):
        """
        Create default Row-Header widget
        :param master: Is passed by KTable
        :param name: Is passed by KTable
        :param args: Look at KTableHeader for exact doc
        :param kwargs: Look at KTableHeader for exact doc
        """
        super().__init__(
            master,
            name,
            "row",
            *args,
            **kwargs)


class KTableColHeader(KTableHeader):
    """
    Default Column-Header widget
    """
    def __init__(
            self,
            master: KTable,
            name: str,
            *args: any,
            **kwargs: any):
        """
        Create default Column-Header widget
        :param master: Is passed by KTable
        :param name: Is passed by KTable
        :param args: Look at KTableHeader for exact doc
        :param kwargs: Look at KTableHeader for exact doc
        """
        super().__init__(
            master,
            name,
            "column",
            *args,
            **kwargs)
