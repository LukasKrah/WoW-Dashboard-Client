"""
gui/instances.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from json import dumps

from gui.widgets import Table, NavBar, ContextMenu
from style import Theme, ImageManager, KImage

from data.settings import InstanceManager
from data import Settings

##################################################
#                 Menu classes                   #
##################################################


class InstanceRowHeader(CTkCanvas):
    width: int
    height: int
    text: str
    image: KImage | None

    def __init__(
            self,
            master: Table,
            text: str,
            image: str,
            *args: any,
            **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.width, self.height = 0, 0
        self.text = text
        print("IMAGE", image)
        if image:
            self.image = KImage(image)
        else:
            self.image = None

        self.configure(
            bd=5,
            highlightthickness=0,
            background=Theme.background3)
        self.bind("<Configure>", self.__resize)

    def _reload(self) -> None:
        self.delete("all")
        # 100, 100
        # 200,
        print(self.image)
        if self.image:
            self.image.resize(self.width, self.height, "fitx")
            self.create_image(
                self.width / 2,
                self.height / 2,
                image=self.image.imgTk)

        self.create_text(
            self.width / 2,
            self.height / 2,
            text=self.text,
            anchor="center",
            font=Theme.wow_font,
            fill="white")

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self._reload()


class InstanceCell(CTkCanvas):
    width: int
    height: int
    click_x: int
    click_y: int
    rclick_y: int

    column: str
    row: str

    con: list[ContextMenu]
    __states: list[str]
    diffs: list[str]
    index: int

    def __init__(
            self,
            master: Table,
            col: str,
            row: str,
            *args: any,
            **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.width, self.height = 0, 0
        self.click_x, self.click_y = 0, 0
        self.rclick_y = 0
        self.column, self.row = col, row
        self.diffs = list(self.master.values[self.row]["difficulty"].keys())
        self.index = 0

        self.con = [ContextMenu(
            self, [{"label": "Aktivieren", "command": self.toggle}]) for diff in self.diffs]

        self.__states = ["disable" for diff in self.diffs]
        for index, diff in enumerate(self.diffs):
            try:
                if self.column in self.master.values[self.row]["difficulty"][diff]["chars"]:
                    self.con[index].change_label(0, "Deaktivieren")
                    match self.master.values[self.row]["difficulty"][diff]["chars"][self.column]["done"]:
                        case True:
                            self.__states[index] = "done"
                        case False:
                            self.__states[index] = "cancel"
                        case None:
                            self.__states[index] = "neutral"
                    self._reload()
            except KeyError:
                ...
        print(self.__states)

        self.configure(
            bd=5,
            highlightthickness=0,
            background=Theme.background3)
        self.bind("<Configure>", self.__resize)
        self.bind("<Button-1>", self.__click)
        self.bind("<Button-3>", self._popup)

    def _get_index(self, cord_y: int | None = None) -> int:
        if cord_y is None:
            cord_y = self.rclick_y
        return int(cord_y / self.height * len(self.diffs))

    def _get_height(self, index: int | None = None,
                    all_len: int | None = None) -> int:
        index = self.index if index is None else index
        all_len = len(self.diffs) if all_len is None else all_len
        return int(self.height * (index / all_len))

    def _get_height_top(self, index: int | None = None,
                        all_len: int | None = None) -> int:
        if index is None:
            index = self.index
        return self._get_height(index=index + 1, all_len=all_len)

    def _get_height_text(self, index: int | None = None,
                         all_len: int | None = None) -> int:
        if all_len is None:
            all_len = len(self.diffs)
        return self._get_height(index=index, all_len=all_len) + \
            int((self.height / all_len) / 2)

    def _popup(self, event: Event) -> None:
        self.rclick_y = event.y
        self.con[self._get_index()].popup(event)

    @property
    def states(self) -> list[str]:
        return self.__states

    @states.setter
    def states(self, value: list[str]) -> None:
        self.__states = value
        self._reload()

    def toggle(self) -> None:
        indexes = [self._get_index()]
        if self._all_equal() and self.__states[0] not in ["neutral"]:
            indexes = [index for index in range(len(self.diffs))]
        for index in indexes:
            if self.__states[index] == "disable":
                self.__states[index] = "neutral"
                self.master.values[self.row]["difficulty"][self.diffs[index]
                                                           ]["chars"][self.column] = {"done": None}
                self.con[index].change_label(0, "Deaktivieren")
            else:
                self.__states[index] = "disable"
                del self.master.values[self.row]["difficulty"][self.diffs[index]
                                                               ]["chars"][self.column]
                self.con[index].change_label(0, "Aktivieren")
        self._reload()
        InstanceManager.write()

    def _all_equal(self) -> bool:
        all_equal = True
        for state in self.__states:
            if state != self.__states[0]:
                all_equal = False
        return all_equal

    def _reload(self) -> None:
        self.delete("all")

        if self._all_equal() and self.__states[0] not in ["neutral"]:
            eval(f"self._{self.__states[0]}(index=0, all_len=1)")
        else:
            for index in range(len(self.diffs)):
                self.index = index
                eval(f"self._{self.__states[index]}()")
        InstanceManager.write()

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self._reload()

    def __click(self, event) -> None:
        self.click_x, self.click_y = event.x, event.y

        if self._all_equal() and self.__states[0] not in ["neutral"]:
            eval(
                f"self._{self.__states[0]}_click({dumps([index for index in range(len(self.diffs))])})")
        else:
            index = self._get_index(self.click_y)
            eval(f"self._{self.__states[index]}_click([{index}])")
        InstanceManager.write()

    # --- Different states --- #
    # Disable
    def _disable_click(self, _index: list[int]) -> None:
        ...

    def _disable(self, **kwargs) -> None:
        self.create_rectangle(
            0,
            self._get_height(
                **kwargs),
            self.width,
            self._get_height_top(
                **kwargs),
            fill="#555555")
        self.create_text(
            self.width / 2,
            self._get_height_text(**kwargs),
            text="-",
            font=(
                Theme.font,
                Theme.fontfactor * 18))

    # Neutral
    def _neutral_click(self, indexes: list[int]) -> None:
        for index in indexes:
            if self.click_x < self.width / 2:
                self.__states[index] = "done"

                print(self.diffs)
                self.master.values[self.row]["difficulty"][self.diffs[index]
                                                           ]["chars"][self.column] = {"done": True}
            else:
                self.__states[index] = "cancel"
                self.master.values[self.row]["difficulty"][self.diffs[index]
                                                           ]["chars"][self.column] = {"done": False}
            self._reload()

    def _neutral(self, **kwargs) -> None:
        self.create_rectangle(
            0,
            self._get_height(
                **kwargs),
            self.width / 2,
            self._get_height_top(
                **kwargs),
            fill="#00ff00")
        self.create_rectangle(
            self.width / 2,
            self._get_height(
                **kwargs),
            self.width,
            self._get_height_top(
                **kwargs),
            fill="#ff0000")

        self.create_text(
            self.width / 4,
            self._get_height_text(**kwargs),
            text="✓",
            anchor="center",
            font=(
                Theme.font,
                Theme.fontfactor * 18))
        self.create_text(
            self.width / 4 * 3,
            self._get_height_text(**kwargs),
            text="❌",
            anchor="center",
            font=(
                Theme.font,
                Theme.fontfactor * 18))

    # Done
    def _done_click(self, indexes: list[int]) -> None:
        if messagebox.askyesno(
                "Zurücksetzen",
                "Sicher das du dieses Feld zurücksetzen willst?"):
            for index in indexes:
                self.__states[index] = "neutral"
                self.master.values[self.row]["difficulty"][self.diffs[index]
                                                           ]["chars"][self.column] = {"done": None}
            self._reload()

    def _done(self, **kwargs) -> None:
        self.create_rectangle(
            0,
            self._get_height(
                **kwargs),
            self.width,
            self._get_height_top(
                **kwargs),
            fill="#00ff00")

        self.create_text(
            self.width / 2,
            self._get_height_text(**kwargs),
            text="Erledigt!",
            anchor="center",
            font=(
                Theme.font,
                Theme.fontfactor * 18))

    # Cancel
    def _cancel_click(self, indexes: list[int]) -> None:
        self._done_click(indexes)

    def _cancel(self, **kwargs) -> None:
        h1, h2 = self._get_height(**kwargs), self._get_height_top(**kwargs)
        self.create_rectangle(0, h1, self.width, h2, fill="#ff0000")
        self.create_text(
            self.width /
            2,
            self._get_height_text(
                **kwargs),
            text="Machs gefällig\ndu KEK!" if h2 -
            h1 > Theme.fontfactor *
            50 else "KEKW!",
            anchor="center",
            font=(
                Theme.font,
                Theme.fontfactor *
                18),
            justify="center")


class InstanceTable(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)

        self.table = Table(
            self,
            cells=InstanceCell,
            rowheader=InstanceRowHeader,
            colheader=InstanceRowHeader)
        self.table.values = InstanceManager.values
        self.table.reload()
        self.navBar = NavBar(self, self.set_week,
                             new_char_callback=self.add_char,
                             new_todo_callback=self.add_todo)

        self.grid_widgets()

    def add_char(self, name: str, realm: str) -> None:
        Settings["chars"].append({"characterName": name, "realmSlug": realm})
        Settings.write()
        self.table.reload()

    def add_todo(self, name: str, typ: str, diff: str) -> None:
        if name not in self.table.values:
            self.table.values[name] = {
                "type": typ,
                "image": ImageManager.get_image(name),
                "difficulty": {
                    dif: {"chars": {}} for dif in diff.split(", ")
                } if diff else {"": {"chars": {}}}
            }
        self.table.reload()

    def set_week(self, week: str) -> None:
        InstanceManager.today = week
        Settings.today = week
        self.table.values = InstanceManager.values
        self.table.reload()

    def grid_widgets(self) -> None:
        self.table.grid(row=0, column=0, sticky="NSEW")
        self.navBar.grid(row=1, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
