"""
gui/instances/instance_cells.py

Project: WoW-Dashboard-Client
Created: 19.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import messagebox, Event
from threading import Thread
from json import dumps

from gui.widgets import KContextMenu, KTable, KCanvas
from data import InstanceManager
from style import Theme


##################################################
#                     Code                       #
##################################################

class InstanceCell(KCanvas):
    """
    Instance Cell widget for Instance table
    """
    master: KTable
    column: str
    row: str

    done_fg: str
    done_fg_hover: str
    done_text_color: str
    done_text_color_hover: str
    done_font: tuple[str, int]
    done_font_hover: tuple[str, int]

    cancel_fg: str
    cancel_fg_hover: str
    cancel_text_color: str
    cancel_text_color_hover: str
    cancel_font: tuple[str, int]
    cancel_font_hover: tuple[str, int]

    positive_fg: str
    positive_fg_hover: str
    positive_text_color: str
    positive_text_color_hover: str
    positive_font: tuple[str, int]
    positive_font_hover: tuple[str, int]

    negative_fg: str
    negative_fg_hover: str
    negative_text_color: str
    negative_text_color_hover: str
    negative_font: tuple[str, int]
    negative_font_hover: tuple[str, int]

    disabled_fg: str
    disabled_fg_hover: str
    disabled_text_color: str
    disabled_text_color_hover: str
    disabled_font: tuple[str, int]
    disabled_font_hover: tuple[str, int]

    width: int
    height: int
    click_x: int
    click_y: int
    rclick_y: int
    hover_x: int
    hover_y: int
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

            done_fg: str | None = Theme.done_color,
            done_fg_hover: str | None = Theme.done_color_light,
            done_text_color: str | None = Theme.done_text,
            done_text_color_hover: str | None = Theme.done_text,
            done_font: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 18),
            done_font_hover: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 16),

            cancel_fg: str | None = Theme.cancel_color,
            cancel_fg_hover: str | None = Theme.cancel_color_light,
            cancel_text_color: str | None = Theme.cancel_text,
            cancel_text_color_hover: str | None = Theme.cancel_text,
            cancel_font: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 18),
            cancel_font_hover: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 16),

            positive_fg: str | None = Theme.positive_color,
            positive_fg_hover: str | None = Theme.positive_color_light,
            positive_text_color: str | None = Theme.positive_text,
            positive_text_color_hover: str | None = Theme.positive_text,
            positive_font: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 18),
            positive_font_hover: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 16),

            negative_fg: str | None = Theme.negative_color,
            negative_fg_hover: str | None = Theme.negative_color_light,
            negative_text_color: str | None = Theme.negative_text,
            negative_text_color_hover: str | None = Theme.negative_text,
            negative_font: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 18),
            negative_font_hover: tuple[str, int] | None = (Theme.wow_font, Theme.fontfactor * 16),

            disabled_fg: str | None = Theme.background1,
            disabled_fg_hover: str | None = Theme.background1,
            disabled_text_color: str | None = Theme.text_color,
            disabled_text_color_hover: str | None = Theme.text_color,
            disabled_font: tuple[str, int] | None = (Theme.font, Theme.fontfactor * 25),
            disabled_font_hover: tuple[str, int] | None = (Theme.font, Theme.fontfactor * 20),

            **kwargs: any) -> None:
        """
        Create instance cell widget for instance table

        :param master: Master widget (Table)
        :param column: Columns name
        :param row: Row name
        :param positive_fg:
        :param positive_fg_hover:
        :param positive_text_color:
        :param positive_text_color_hover:
        :param positive_font:
        :param positive_font_hover:
        :param negative_fg:
        :param negative_fg_hover:
        :param negative_text_color:
        :param negative_text_color_hover:
        :param negative_font:
        :param negative_font_hover:
        :param disabled_fg:
        :param disabled_fg_hover:
        :param disabled_text_color:
        :param disabled_text_color_hover:
        :param disabled_font:
        :param disabled_font_hover:
        """
        # Params
        self.master = master
        self.column = column
        self.row = row

        self.done_fg = done_fg
        self.done_fg_hover = done_fg_hover
        self.done_text_color = done_text_color
        self.done_text_color_hover = done_text_color_hover
        self.done_font = done_font
        self.done_font_hover = done_font_hover

        self.cancel_fg = cancel_fg
        self.cancel_fg_hover = cancel_fg_hover
        self.cancel_text_color = cancel_text_color
        self.cancel_text_color_hover = cancel_text_color_hover
        self.cancel_font = cancel_font
        self.cancel_font_hover = cancel_font_hover

        self.positive_fg = positive_fg
        self.positive_fg_hover = positive_fg_hover
        self.positive_text_color = positive_text_color
        self.positive_text_color_hover = positive_text_color_hover
        self.positive_font = positive_font
        self.positive_font_hover = positive_font_hover

        self.negative_fg = negative_fg
        self.negative_fg_hover = negative_fg_hover
        self.negative_text_color = negative_text_color
        self.negative_text_color_hover = negative_text_color_hover
        self.negative_font = negative_font
        self.negative_font_hover = negative_font_hover

        self.disabled_fg = disabled_fg
        self.disabled_fg_hover = disabled_fg_hover
        self.disabled_text_color = disabled_text_color
        self.disabled_text_color_hover = disabled_text_color_hover
        self.disabled_font = disabled_font
        self.disabled_font_hover = disabled_font_hover

        super().__init__(master, *args, **kwargs)

        # Other vars
        self.width, self.height = 0, 0
        self.click_x, self.click_y = 0, 0
        self.rclick_y = 0
        self.index = 0

        self.diffs = list(
            InstanceManager.values[self.row]["difficulty"].keys())
        self.con = [KContextMenu(
            self, [{"label": "Aktivieren", "command": self.toggle}]) for _diff in self.diffs]
        self.__states = []
        self.reload()

        # Configuration
        self.configure(
            background=Theme.background3)
        self.bind("<Configure>", self.__resize)
        self.bind("<Button-1>", self.__click)
        self.bind("<Button-3>", self._popup)
        self.bind("<Leave>", lambda e=...: self._reload())
        self.bind("<Enter>", self.__hover)
        self.bind("<Motion>", self.__hover)

    def reload(self) -> None:
        states = ["disable" for _diff in self.diffs]
        for index, diff in enumerate(self.diffs):
            try:
                if self.column in InstanceManager[self.row]["difficulty"][diff]["chars"]:
                    self.con[index].change_label(0, "Deaktivieren")
                    match InstanceManager[self.row]["difficulty"][diff]["chars"][self.column]["done"]:
                        case True:
                            states[index] = "done"
                        case False:
                            states[index] = "cancel"
                        case None:
                            states[index] = "neutral"
            except KeyError:
                ...
        self.__states = states
        self._reload()

    # Index and height helping funcs
    def _get_index_y(self, cord_y: int | None = None) -> int:
        """
        Get index on which part (difficulty) of cell is clicked
        :param cord_y: Y-Coordinate of the click
        :return: Index
        """
        if cord_y is None:
            cord_y = self.rclick_y
        return int(cord_y / self.height * len(self.diffs))

    def _get_index_x(self, cord_x: int | None = None,
                     len_xelems: int | None = 2) -> int:
        if cord_x is None:
            cord_x = self.hover_x
        return int(cord_x / self.width * len_xelems)

    def _get_height(self, index: int | None = None,
                    all_len: int | None = None) -> int:
        """
        Get upper y-coord for element of index of certain number of elements
        :param index: Index of difficulty element
        :param all_len: How many elements are there
        :return: Y-Coordinate upper position
        """
        index = self.index if index is None else index
        all_len = len(self.diffs) if all_len is None else all_len
        return int(self.height * (index / all_len))

    def _get_height_top(self, index: int | None = None,
                        all_len: int | None = None) -> int:
        """
        Get down y-coord for element of index of certain number of elements
        :param index: Index of difficulty element
        :param all_len: How many elements are there
        :return: Y-Coordinate down position
        """
        if index is None:
            index = self.index
        return self._get_height(index=index + 1, all_len=all_len)

    def _get_height_text(self, index: int | None = None,
                         all_len: int | None = None) -> int:
        """
        Get y-position for text for element of index of certain number of elements
        :param index: Index of difficulty element
        :param all_len: How many elements are there
        :return: Y-Position of text
        """
        if all_len is None:
            all_len = len(self.diffs)
        return self._get_height(index=index, all_len=all_len) + \
            int((self.height / all_len) / 2)

    def _popup(self, event: Event) -> None:
        """
        Open right click contextmenu popup
        :param event: Event with coords
        """
        self.rclick_y = event.y
        self.con[self._get_index_y()].popup(event)

    def toggle(self) -> None:
        """
        Toggle enabled / disabled of element
        """
        indexes = [self._get_index_y()]
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
        """
        Check if all in list are equal
        """
        all_equal = True
        for state in self.__states:
            if state != self.__states[0]:
                all_equal = False
        return all_equal

    # --- State funcs --- #
    def _reload(
            self,
            prefix_eval: str | None = "self._",
            suffix_eval: str | None = "",
            suffix_indexes: list[int] | None = None) -> None:
        suffix_indexes = suffix_indexes if suffix_indexes else []

        self.delete("all")

        if self._all_equal() and self.__states[0] not in ["neutral"]:
            eval(
                f"{prefix_eval}{self.__states[0]}{suffix_eval}(index=0, all_len=1)")
        else:
            for index in range(len(self.diffs)):
                self.index = index
                eval(
                    f"{prefix_eval}{self.__states[index]}{suffix_eval if index in suffix_indexes else ''}()")
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
            self.index = self._get_index_y(self.click_y)
            eval(f"self._{self.__states[self.index]}_click([{self.index}])")
        self.__hover(event)
        InstanceManager.write()

    def __hover(self, event: Event) -> None:
        self.hover_x, self.hover_y = event.x, event.y
        self._reload(
            suffix_eval="_hover",
            suffix_indexes=[
                self._get_index_y(
                    event.y)])

    # --- Different states --- #
    # Disable
    def _disable_click(self, _index: list[int]) -> None:
        ...

    def _disable(self,
                 fg: str | None = None,
                 text_color: str | None = None,
                 text_font: tuple[str, int] | None = None,
                 **kwargs) -> None:
        fg = fg if fg else self.disabled_fg
        text_color = text_color if text_color else self.disabled_text_color
        text_font = text_font if text_font else self.disabled_font

        self.create_rectangle_rounded_filled(
            0,
            self._get_height(**kwargs),
            self.width,
            self._get_height_top(**kwargs),
            r=15 if self.height // len(self.diffs) > 30 else self.height // len(self.diffs) // 3,
            fill=fg
        )

        self.create_text(
            self.width / 2,
            self._get_height_text(**kwargs),
            text="-",
            fill=text_color,
            font=text_font)

    def _disable_hover(self, **kwargs) -> None:
        self._disable(
            fg=self.disabled_fg_hover,
            text_color=self.disabled_text_color,
            text_font=self.disabled_font_hover,
            **kwargs
        )

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

    def _neutral(self,
                 positive_fg: str | None = None,
                 positive_text_color: str | None = None,
                 positive_text_font: tuple[str, int] | None = None,
                 negative_fg: str | None = None,
                 negative_text_color: str | None = None,
                 negative_text_font: tuple[str, int] | None = None,
                 **kwargs) -> None:
        positive_fg = positive_fg if positive_fg else self.positive_fg
        positive_text_color = positive_text_color if positive_text_color else self.positive_text_color
        positive_text_font = positive_text_font if positive_text_font else self.positive_font
        negative_fg = negative_fg if negative_fg else self.negative_fg
        negative_text_color = negative_text_color if negative_text_color else self.negative_text_color
        negative_text_font = negative_text_font if negative_text_font else self.negative_font

        self.create_rectangle_rounded_filled(
            0,
            self._get_height(**kwargs),
            self.width / 2,
            self._get_height_top(**kwargs),
            r_nw=15 if self.height // len(self.diffs) > 30 else self.height // len(self.diffs) // 3,
            r_sw=15 if self.height // len(self.diffs) > 30 else self.height // len(self.diffs) // 3,
            fill=positive_fg)
        self.create_rectangle_rounded_filled(
            self.width / 2,
            self._get_height(**kwargs),
            self.width,
            self._get_height_top(**kwargs),
            r_ne=15 if self.height // len(self.diffs) > 30 else self.height // len(self.diffs) // 3,
            r_se=15 if self.height // len(self.diffs) > 30 else self.height // len(self.diffs) // 3,
            fill=negative_fg)

        self.create_text(
            self.width / 4,
            self._get_height_text(**kwargs),
            text="✓",
            anchor="center",
            fill=positive_text_color,
            font=positive_text_font)
        self.create_text(
            self.width / 4 * 3,
            self._get_height_text(**kwargs),
            text="❌",
            anchor="center",
            fill=negative_text_color,
            font=negative_text_font)

    def _neutral_hover(self, **kwargs) -> None:
        if self._get_index_x() == 0:
            self._neutral(
                positive_fg=self.positive_fg_hover,
                positive_text_color=self.positive_text_color_hover,
                positive_text_font=self.positive_font_hover,
                negative_fg=self.negative_fg,
                negative_text_color=self.negative_text_color,
                negative_text_font=self.negative_font,
                **kwargs
            )
        else:
            self._neutral(
                positive_fg=self.positive_fg,
                positive_text_color=self.positive_text_color,
                positive_text_font=self.positive_font,
                negative_fg=self.negative_fg_hover,
                negative_text_color=self.negative_text_color_hover,
                negative_text_font=self.negative_font_hover,
                **kwargs
            )

    # Done
    def _done_click_threaded(self, indexes: list[int]) -> None:
        if messagebox.askyesno(
                "Zurücksetzen",
                "Sicher das du dieses Feld zurücksetzen willst?"):
            for index in indexes:
                self.__states[index] = "neutral"
                InstanceManager.values[self.row]["difficulty"][self.diffs[index]
                                                               ]["chars"][self.column] = {"done": None}
            self._reload()

    def _done_click(self, indexes: list[int]) -> None:
        Thread(target=self._done_click_threaded,
               kwargs={"indexes": indexes}).start()

    def _done(self,
              fg: str | None = None,
              text_color: str | None = None,
              text_font: tuple[str, int] | None = None,
              **kwargs) -> None:
        fg = fg if fg else self.done_fg
        text_color = text_color if text_color else self.done_text_color
        text_font = text_font if text_font else self.done_font

        self.create_rectangle_rounded_filled(
            0,
            self._get_height(
                **kwargs),
            self.width,
            self._get_height_top(
                **kwargs),
            r=15 if self.height // len(self.diffs) > 30 else self.height // len(self.diffs) // 3,
            fill=fg)

        self.create_text(
            self.width / 2,
            self._get_height_text(**kwargs),
            text="Erledigt!",
            anchor="center",
            fill=text_color,
            font=text_font)

    def _done_hover(self, **kwargs) -> None:
        self._done(
            fg=self.done_fg_hover,
            text_color=self.done_text_color,
            text_font=self.done_font_hover,
            **kwargs
        )

    # Cancel
    def _cancel_click(self, indexes: list[int]) -> None:
        self._done_click(indexes)

    def _cancel(self,
                fg: str | None = None,
                text_color: str | None = None,
                text_font: tuple[str, int] | None = None,
                **kwargs) -> None:
        fg = fg if fg else self.cancel_fg
        text_color = text_color if text_color else self.cancel_text_color
        text_font = text_font if text_font else self.cancel_font

        h1, h2 = self._get_height(**kwargs), self._get_height_top(**kwargs)
        self.create_rectangle_rounded_filled(0, h1, self.width, h2,
                                             r=15 if self.height // len(self.diffs) > 30
                                             else self.height // len(self.diffs) // 3, fill=fg)
        self.create_text(
            self.width /
            2,
            self._get_height_text(
                **kwargs),
            text="Machs gefällig\ndu KEK!" if h2 -
            h1 > Theme.fontfactor *
            50 else "KEKW!",
            anchor="center",
            font=text_font,
            fill=text_color,
            justify="center")

    def _cancel_hover(self, **kwargs) -> None:
        self._cancel(
            fg=self.cancel_fg_hover,
            text_color=self.cancel_text_color,
            text_font=self.cancel_font_hover,
            **kwargs
        )
