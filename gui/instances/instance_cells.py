"""
gui/instances/instance_cells.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import messagebox
from tkinter import *
from json import dumps

from gui.widgets import KContextMenu, KTable
from style import Theme
from data import InstanceManager


##################################################
#                     Code                       #
##################################################

class InstanceCell(CTkCanvas):
    """
    Instance Cell widget for Instance table
    """
    master: KTable
    column: str
    row: str

    positive_bg: str
    positive_text_color: str
    negative_bg: str
    negative_text_color: str
    disabled_bg: str
    disabled_text_color: str

    width: int
    height: int
    click_x: int
    click_y: int
    rclick_y: int
    index: int

    diffs: list[str]
    con: list[KContextMenu]
    __states: list[str]

    def __init__(
            self,
            master: KTable,
            column: str,
            row: str,
            *args: any,
            positive_bg: str | None = Theme.positive_color,
            positive_text_color: str | None = Theme.positve_text,
            negative_bg: str | None = Theme.negative_color,
            negative_text_color: str | None = Theme.negative_text,
            disabled_bg: str | None = Theme.background1,
            disabled_text_color: str | None = Theme.text_color_reverse,
            **kwargs: any) -> None:
        """
        Create instance cell widget for instance table

        :param master: Master widget (Table)
        :param column: Column name
        :param row: Row name
        :param positive_bg: "YES" selection background
        :param positive_text_color: "YES" selection textcolor
        :param negative_bg: "NO" selection background
        :param negative_text_color: "YES" selection textcolor
        :param disabled_bg: Disabled state background
        :param disabled_text_color: Disabled state background
        """
        # Params
        self.master = master
        self.column = column
        self.row = row

        self.positive_bg = positive_bg
        self.positive_text_color = positive_text_color
        self.negative_bg = negative_bg
        self.negative_text_color = negative_text_color
        self.disabled_bg = disabled_bg
        self.disabled_text_color = disabled_text_color

        super().__init__(master, *args, **kwargs)

        # Other vars
        self.width, self.height = 0, 0
        self.click_x, self.click_y = 0, 0
        self.rclick_y = 0
        self.index = 0

        self.diffs = list(InstanceManager[self.row]["difficulty"].keys())
        self.con = [KContextMenu(
            self, [{"label": "Aktivieren", "command": self.toggle}]) for _diff in self.diffs]

        self.__states = ["disable" for _diff in self.diffs]
        for index, diff in enumerate(self.diffs):
            try:
                if self.column in InstanceManager[self.row]["difficulty"][diff]["chars"]:
                    self.con[index].change_label(0, "Deaktivieren")
                    match InstanceManager[self.row]["difficulty"][diff]["chars"][self.column]["done"]:
                        case True:
                            self.__states[index] = "done"
                        case False:
                            self.__states[index] = "cancel"
                        case None:
                            self.__states[index] = "neutral"
                    self._reload()
            except KeyError:
                ...

        # Configuration
        self.configure(
            bd=5,
            highlightthickness=0,
            background=Theme.background3)
        self.bind("<Configure>", self.__resize)
        self.bind("<Button-1>", self.__click)
        self.bind("<Button-3>", self._popup)

    # Index and height helping funcs
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

    def toggle(self) -> None:
        indexes = [self._get_index()]
        if self._all_equal() and self.__states[0] not in ["neutral"]:
            indexes = [index for index in range(len(self.diffs))]
        for index in indexes:
            if self.__states[index] == "disable":
                self.__states[index] = "neutral"
                InstanceManager.values[self.row]["difficulty"][self.diffs[index]]["chars"][self.column] = {
                    "done": None}
                self.con[index].change_label(0, "Deaktivieren")
            else:
                self.__states[index] = "disable"
                del InstanceManager.values[self.row]["difficulty"][self.diffs[index]
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

    # --- State funcs --- #
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

    def __click(self, event: Event) -> None:
        self.click_x, self.click_y = event.x, event.y

        if self._all_equal() and self.__states[0] not in ["neutral"]:
            eval(
                f"self._{self.__states[0]}_click({dumps([index for index in range(len(self.diffs))])})")
        else:
            index = self._get_index(self.click_y)
            eval(f"self._{self.__states[index]}_click([{index}])")
        InstanceManager.write()

    def __hover(self, event: Event) -> None:
        ...

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

                InstanceManager[self.row]["difficulty"][self.diffs[index]
                                                        ]["chars"][self.column] = {"done": True}
            else:
                self.__states[index] = "cancel"
                InstanceManager[self.row]["difficulty"][self.diffs[index]
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
                InstanceManager.values[self.row]["difficulty"][self.diffs[index]
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
                Theme.wow_font,
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
                Theme.wow_font,
                Theme.fontfactor *
                18),
            justify="center")
