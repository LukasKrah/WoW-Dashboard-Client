"""
gui/instances/instance_headers.py

Project: WoW-Dashboard-Client
Created: 19.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Literal
from tkinter import Event

from gui.widgets import KContextMenu, KCanvas
from data import InstanceManager, Settings
from style import KImage, Theme


##################################################
#                     Code                       #
##################################################

class InstanceRowHeader(KCanvas):
    master: any
    name: str
    colrow_index: int
    index: int
    typ: Literal["col", "row"]

    headerwidgets: dict
    headerwidgets_by_index: list
    dragindex: int

    width: int
    height: int

    labels: list[str]
    image: KImage | None
    con: KContextMenu

    def __init__(
            self,
            master: any,
            name: str,
            colrow_index: int,
            index: int,
            *args: any,
            typ: Literal["col"] | None = "row",
            **kwargs: any) -> None:
        self.master = master
        self.name = name
        self.colrow_index = colrow_index
        self.index = index
        self.typ = typ

        self.dragindex = 0
        match self.typ:
            case "row":
                self.headerwidgets = self.master.row_headerwidgets
            case "col":
                self.headerwidgets = self.master.column_headerwidgets

        super().__init__(master, *args, **kwargs)

        if index == 0:
            self.con = KContextMenu(
                self, [{"label": "Alle Aktivieren (ACHTUNG)", "command": self.activate_whole},
                       {"label": "Alle Deaktivieren (ACHTUNG)", "command": self.deactivate_whole},
                       {"label": "Löschen (ACHTUNG)", "command": self.delete_whole}])
            self.bind("<Button-3>", self.con.popup)
            self.bind("<ButtonPress-1>", self.drag_down)
            self.bind("<B1-Motion>", self.drag_down)
            self.bind("<ButtonRelease-1>", self.drag_up)

        self.width, self.height = 0, 0

        if self.index == 0 and typ == "col":
            self.labels = [Settings["chars"][self.name]["characterName"]]
        else:
            self.labels = self.name.split(",") if self.name else []

        if typ == "row":
            self.image = KImage(
                InstanceManager[name]["image"]) if InstanceManager[name]["image"] else None
        else:
            self.image = None

        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)
        self.bind("<Configure>", self.__resize)

    def delete_in_all_headers(self, tag: str | None = "dragndrop"):
        for header in self.headerwidgets:
            for subheader in self.headerwidgets[header]:
                subheader.delete(tag)

    def drag_down(self, event: Event) -> None:
        match self.typ:
            case "col":
                eventcoord = event.x
                size = self.width
            case _:
                eventcoord = event.y
                size = self.height
        self.delete_in_all_headers()
        if not self.image:
            self.configure(bg=Theme.background2)
        else:
            self.reload(grey_out=True)

        modify = 0.5 if eventcoord >= 0 else -0.5
        self.dragindex = int(
            ((eventcoord / size) + modify)) + self.colrow_index

        self.headerwidgets_by_index = [[] for _header in self.headerwidgets]
        for header in self.headerwidgets:
            self.headerwidgets_by_index[self.headerwidgets[header][
                0].colrow_index] = self.headerwidgets[header]

        try:
            self.headerwidgets_by_index[self.dragindex -
                                        1][self.index].draw_pre() if self.dragindex > 0 else None
        except (IndexError, KeyError):
            ...
        try:
            self.headerwidgets_by_index[self.dragindex][self.index].draw_after(
            )
        except (IndexError, KeyError):
            ...

        self.dragindex = 0 if self.dragindex < 0 else self.dragindex
        self.dragindex = len(
            self.headerwidgets) if self.dragindex > len(
            self.headerwidgets) else self.dragindex

    def drag_up(self, _event: Event) -> None:
        self.delete_in_all_headers()
        self.configure(bg=Theme.background3)

        self.dragindex += (-1 if self.colrow_index <=
                           self.dragindex - 1 else 0)
        match self.typ:
            case "row":
                if self.dragindex != InstanceManager.values[self.name]["row"]:
                    for instance in InstanceManager.values:
                        if instance != self.name and InstanceManager.values[instance]["active"]:
                            if self.colrow_index < InstanceManager.values[
                                    instance]["row"] < self.dragindex + 1:
                                InstanceManager.values[instance]["row"] -= 1
                            elif self.colrow_index >= InstanceManager.values[instance]["row"] >= self.dragindex:
                                InstanceManager.values[instance]["row"] += 1
                    InstanceManager.values[self.name]["row"] = self.dragindex

            case "col":
                if self.dragindex != Settings["chars"][self.name]["column"]:
                    for user in Settings.values["chars"]:
                        if user != self.name and Settings.values["chars"][user]["active"]:
                            if self.colrow_index < Settings.values["chars"][user]["column"] < self.dragindex + 1:
                                Settings.values["chars"][user]["column"] -= 1
                            elif self.colrow_index >= Settings.values["chars"][user]["column"] >= self.dragindex:
                                Settings.values["chars"][user]["column"] += 1
                    Settings.values["chars"][self.name]["column"] = self.dragindex

        self.reload()
        Settings.write()
        InstanceManager.write()
        self.master.master.master.reload_table()

    def draw_after(self) -> None:
        match self.typ:
            case "col":
                self.create_line(
                    0,
                    0,
                    0,
                    self.height,
                    fill="blue",
                    width=20,
                    tags=["dragndrop"])
            case "row":
                self.create_line(
                    0,
                    0,
                    self.width,
                    0,
                    fill="blue",
                    width=20,
                    tags=["dragndrop"])

    def draw_pre(self) -> None:
        match self.typ:
            case "col":
                self.create_line(
                    self.width,
                    0,
                    self.width,
                    self.height,
                    fill="blue",
                    width=20,
                    tags=["dragndrop"])
            case "row":
                self.create_line(
                    0,
                    self.height,
                    self.width,
                    self.height,
                    fill="blue",
                    width=20,
                    tags=["dragndrop"])

    def set_index(self, value: int) -> None:
        self.colrow_index = value

    def reload(self, grey_out: bool | None = False) -> None:
        self.delete("all")

        if self.image:
            self.image.resize(self.width, self.height, "cover")
            self.create_image(
                self.width / 2,
                self.height / 2,
                image=self.image.imgTk_greyout if grey_out else self.image.imgTk)

        labels_len = len(self.labels) + 1
        for index, label in enumerate(self.labels):
            self.create_text(
                self.width / 2,
                (self.height / labels_len) * (index + 1),
                text=label,
                anchor="center",
                font=(Theme.wow_font, Theme.fontfactor * 18),
                fill=Theme.text_color_light if self.image else Theme.text_color
            )

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self.reload()

    def delete_whole(self) -> None:
        match self.typ:
            case "row":
                InstanceManager.values[self.name]["active"] = False
                for instance in InstanceManager.values:
                    if "row" in InstanceManager.values[instance]:
                        if InstanceManager.values[instance]["row"] > InstanceManager.values[self.name]["row"]:
                            InstanceManager.values[instance]["row"] -= 1
                del InstanceManager.values[self.name]["row"]

            case "col":
                Settings.values["chars"][self.name]["active"] = False
                for char in Settings["chars"]:
                    if "column" in Settings["chars"][char]:
                        if Settings["chars"][char]["column"] > Settings["chars"][self.name]["column"]:
                            Settings["chars"][char]["column"] -= 1
                del Settings.values["chars"][self.name]["column"]
        self.master.master.master.reload_table()

    def _set_states(self, value: bool | str | None) -> None:
        match self.typ:
            case "row":
                for diff in InstanceManager.values[self.name]["difficulty"]:
                    if value == "del":
                        InstanceManager.values[self.name]["difficulty"][diff]["chars"] = {
                        }
                    else:
                        for char in Settings.values["chars"]:
                            if char not in InstanceManager.values[self.name]["difficulty"][diff]["chars"]:
                                InstanceManager.values[self.name]["difficulty"][diff]["chars"][char] = {
                                    "done": value}

            case "col":
                for instance in InstanceManager.values:
                    for diff in InstanceManager.values[instance]["difficulty"]:
                        if self.name in InstanceManager.values[instance]["difficulty"][diff]["chars"]:
                            if value == "del":
                                del InstanceManager.values[instance]["difficulty"][diff]["chars"][self.name]
                        else:
                            if value != "del":
                                InstanceManager.values[instance]["difficulty"][diff]["chars"][self.name] = {
                                    "done": value}
        self.master.master.master.reload_table()

    def activate_whole(self) -> None:
        self._set_states(None)

    def deactivate_whole(self) -> None:
        self._set_states("del")


class InstanceColHeader(InstanceRowHeader):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, typ="col", **kwargs)
