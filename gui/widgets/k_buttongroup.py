"""
gui/widgets/k_buttongroup.py

Project: WoW-Dashboard-Client
Created: 22.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import CTkButton
from typing import Callable

from style import Theme

from .k_button import KButton


##################################################
#                     Code                       #
##################################################

class KButtonGroup:
    master: any
    __buttons: dict

    bg: str
    bg_hover: str
    bg_selected: str
    bg_selected_hover: str
    fg: str
    fg_hover: str
    fg_selected: str
    fg_selected_hover: str
    fontsize: int
    fontsize_hover: int
    fontsize_selected: int
    fontsize_selected_hover: int

    def __init__(self,
                 master: any,
                 buttons: dict,
                 bg: str | None = Theme.primary_dark,
                 bg_hover: str | None = Theme.primary_middle,
                 bg_selected: str | None = Theme.primary_light,
                 bg_selected_hover: str | None = Theme.primary_light,
                 fg: str | None = Theme.text_color,
                 fg_hover: str | None = Theme.text_color,
                 fg_selected: str | None = Theme.text_color,
                 fg_selected_hover: str | None = Theme.text_color,
                 fontsize: int | None = 18,
                 fontsize_hover: int | None = 17,
                 fontsize_selected: int | None = 18,
                 fontsize_selected_hover: int | None = 18) -> None:
        self.master = master
        self.bg = bg
        self.bg_hover = bg_hover
        self.bg_selected = bg_selected
        self.bg_selected_hover = bg_selected_hover
        self.fg = fg
        self.fg_hover = fg_hover
        self.fg_selected = fg_selected
        self.fg_selected_hover = fg_selected_hover
        self.fontsize = fontsize
        self.fontsize_hover = fontsize_hover
        self.fontsize_selected = fontsize_selected
        self.fontsize_selected_hover = fontsize_selected_hover

        self.__buttons = {}
        for but in buttons:
            self.add_button(
                but,
                buttons[but]["label"],
                buttons[but]["command"],
                buttons[but]["selected"] if "selected" in buttons[but] else None)

    def hover_on(self, but: str) -> None:
        self.__buttons[but]["hover"] = True
        self.__buttons[but]["but"].stop_scaling()

        match self.__buttons[but]["but"].fg_color:
            case self.bg | self.bg_hover:
                self.__buttons[but]["but"].configure(
                    fg_color=self.bg_hover, text_color=self.fg_hover)
                self.__buttons[but]["but"].text_label.configure(
                    font=(Theme.wow_font, Theme.fontfactor * self.fontsize_hover))
            case self.bg_selected | self.bg_selected_hover:
                self.__buttons[but]["but"].configure(
                    fg_color=self.bg_selected_hover,
                    text_color=self.fg_selected_hover)
                self.__buttons[but]["but"].text_label.configure(
                    font=(Theme.wow_font, Theme.fontfactor * self.fontsize_selected_hover))

        self.__buttons[but]["but"].resume_scaling()

    def hover_off(self, but: str) -> None:
        self.__buttons[but]["hover"] = False
        self.__buttons[but]["but"].stop_scaling()

        match self.__buttons[but]["but"].fg_color:
            case self.bg_hover | self.bg:
                self.__buttons[but]["but"].configure(
                    fg_color=self.bg, text_color=self.fg)
                self.__buttons[but]["but"].text_label.configure(
                    font=(Theme.wow_font, Theme.fontfactor * self.fontsize))
            case self.bg_selected_hover | self.bg_selected:
                self.__buttons[but]["but"].configure(
                    fg_color=self.bg_selected, text_color=self.fg_selected)
                self.__buttons[but]["but"].text_label.configure(
                    font=(Theme.wow_font, Theme.fontfactor * self.fontsize_selected))

        self.__buttons[but]["but"].resume_scaling()

    @property
    def buttons(self) -> list[CTkButton]:
        return [self.__buttons[but]["but"] for but in self.__buttons]

    def add_button(
            self,
            name: str,
            label: str,
            command: Callable,
            selected: bool | None = False) -> None:
        self.__buttons[name] = {
            "label": label,
            "command": command,
            "selected": selected}
        self.__buttons[name]["but"] = KButton(
            self.master, text=label,
            fg_color=self.bg_selected if selected else self.bg, hover=False,
            text_font=(Theme.wow_font, Theme.fontfactor * 20),
            command=lambda b=name: self.cmd(b)
        )
        self.__buttons[name]["hover"] = False
        self.__buttons[name]["but"].bind_all_widgets(
            "<Enter>", lambda e=..., b=name: self.hover_on(b))
        self.__buttons[name]["but"].bind_all_widgets(
            "<Leave>", lambda e=..., b=name: self.hover_off(b))
        self.hover_off(name)

    def cmd(self, key: str) -> None:
        for but in self.__buttons:
            if but == key:
                CTkButton.configure(
                    self.__buttons[but]["but"],
                    fg_color=self.bg_selected)
            else:
                CTkButton.configure(
                    self.__buttons[but]["but"],
                    fg_color=self.bg)
            self.hover_on(
                but) if self.__buttons[but]["hover"] else self.hover_off(but)
        self.__buttons[key]["command"]()
