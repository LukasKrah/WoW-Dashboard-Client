"""
gui/instances/instance_headers.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from typing import Literal
from tkinter import *

from gui.widgets import KContextMenu
from style import KImage, Theme
from data import InstanceManager, Settings


##################################################
#                     Code                       #
##################################################

class InstanceRowHeader(CTkCanvas):
    master: any
    name: str
    index: int
    typ: Literal["col", "row"]

    width: int
    height: int

    labels: list[str]
    image: KImage | None
    con: KContextMenu

    def __init__(
            self,
            master: any,
            name: str,
            index: int,
            *args: any,
            typ: Literal["col"] | None = "row",
            **kwargs: any) -> None:
        self.master = master
        self.name = name
        self.index = index
        self.typ = typ

        super().__init__(master, *args, **kwargs)

        if index == 0:
            self.con = KContextMenu(
                self, [{"label": "Alle Aktivieren (ACHTUNG)", "command": self.activate_whole},
                       {"label": "Alle Deaktivieren (ACHTUNG)", "command": self.deactivate_whole},
                       {"label": "Löschen (ACHTUNG)", "command": self.delete_whole}])
            self.bind("<Button-3>", self.con.popup)

        self.width, self.height = 0, 0
        self.labels = self.name.split(",") if self.name else []
        if typ == "row":
            self.image = KImage(
                InstanceManager[name]["image"]) if InstanceManager[name]["image"] else None
        else:
            self.image = None

        self.configure(
            bd=5,
            highlightthickness=0,
            background=Theme.background3)
        self.bind("<Configure>", self.__resize)

    def reload(self) -> None:
        self.delete("all")

        if self.image:
            self.image.resize(self.width, self.height, "cover")
            self.create_image(
                self.width / 2,
                self.height / 2,
                image=self.image.imgTk)

        labels_len = len(self.labels) + 1
        for index, label in enumerate(self.labels):
            self.create_text(
                self.width / 2,
                (self.height / labels_len) * (index + 1),
                text=label,
                anchor="center",
                font=(Theme.wow_font, Theme.fontfactor * 18),
                fill=Theme.text_color
            )

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self.reload()

    def delete_whole(self) -> None:
        match self.typ:
            case "row":
                InstanceManager.values[self.name]["active"] = False

            case "col":
                Settings.values["chars"][self.name]["active"] = False
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
