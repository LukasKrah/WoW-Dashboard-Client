"""
gui/widgets/inputs.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *

from style import Theme


##################################################
#                     Code                       #
##################################################

class KEntry(CTkCanvas):
    label: str
    entry: CTkEntry
    valid_symbols: str | None
    textvar: StringVar

    def __init__(
            self,
            master,
            label: str,
            *args: any,
            valid_symbols: str | None = None,
            **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1)

        self.label = label
        self.valid_symbols = valid_symbols

        self.create_text(
            10,
            10,
            text=self.label,
            anchor="nw",
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                18))

        self.textvar = StringVar()
        self.entry = CTkEntry(
            self,
            text_font=(
                Theme.wow_font,
                Theme.fontfactor * 18),
            width=300,
            textvariable=self.textvar)
        self.textvar.trace_add("write", self.__change_text)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.entry.grid(
            row=0, column=0, sticky="NSEW", pady=(
                (Theme.fontfactor * 18) + 30, 0))

    def __change_text(self, *_args) -> None:
        newstring = ""
        for let in self.textvar.get():
            if self.valid_symbols:
                if let in self.valid_symbols:
                    newstring += let
            else:
                newstring += let
        self.textvar.set(newstring)

    def get(self) -> str:
        return self.entry.get()

    def reset(self) -> None:
        self.entry.delete(0, END)


class KOptionMenu(CTkCanvas):
    label: str
    optionMenu: CTkOptionMenu
    values: list[str]

    def __init__(
            self,
            master,
            label: str,
            values: list[str],
            *args: any,
            **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1)

        self.label = label
        self.values = values

        self.create_text(
            10,
            10,
            text=label,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                18),
            anchor="nw")
        self.optionMenu = CTkOptionMenu(
            self, values=self.values, text_font=(
                Theme.wow_font, Theme.fontfactor * 18))
        self.optionMenu.dropdown_menu.configure(tearoff=False)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.optionMenu.grid(
            row=0, column=0, sticky="NSEW", pady=(
                (Theme.fontfactor * 18) + 30, 0))

    def get(self) -> str:
        return self.optionMenu.get()

    def reset(self) -> None:
        self.optionMenu.set(self.values[0])


class KMenu(CTkCanvas):
    label: str
    menuButton: CTkOptionMenu
    menu: Menu
    values: list[str]
    selection: dict[str, IntVar]

    def __init__(
            self,
            master,
            label: str,
            values: list[str],
            *args: any,
            **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1)

        self.label = label
        self.values = values

        self.create_text(
            10,
            10,
            text=label,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                18),
            anchor="nw")
        self.menuButton = CTkOptionMenu(
            self,
            values=[
                self.label],
            text_font=(
                Theme.wow_font,
                Theme.fontfactor *
                18))
        self.menuButton.dropdown_menu.configure(tearoff=False)

        self.selection = {}
        for value in self.values:
            self.selection[value] = IntVar(value=0)
            self.menuButton.dropdown_menu.add_checkbutton(
                label=value,
                variable=self.selection[value],
                selectcolor="white",
                onvalue=1,
                offvalue=0)
            self.selection[value].trace_add("write", self.set)

        self.grid_widgets()

    def set(self, *_args: str) -> None:
        selection_labels = []
        for selection in self.selection:
            if self.selection[selection].get():
                selection_labels.append(selection)

        self.menuButton.text_label.configure(text=", ".join(
            selection_labels) if selection_labels != [] else self.label)

    def grid_widgets(self) -> None:
        self.menuButton.grid(
            row=0, column=0, sticky="NSEW", pady=(
                (Theme.fontfactor * 18) + 30, 0))

    def get(self) -> dict | None:
        return self.menuButton.text_label["text"] if self.menuButton.text_label["text"] != self.label else None

    def reset(self) -> None:
        for selection in self.selection:
            self.selection[selection].set(0)


class KSlider(CTkCanvas):
    """
    Custom slider with label
    """

    master: any
    label: str
    range: list[int, int]

    slider: CTkSlider

    def __init__(self, master: any, label: str, range: str, *args: any, **kwargs: any) -> None:
        """
        Create custom slider and grid widgets

        :param master: Master widget
        :param label: Label to display
        :param range: Slider range in form: "from:to"
        """
        self.master = master
        self.label = label
        self.range = [int(ran) for ran in range.split(":")]

        super().__init__(self.master, *args, **kwargs)

        self.create_text(
            10,
            10,
            text=self.label,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                18),
            anchor="nw")

        self.slider = CTkSlider(from_=self.range[0], to=self.range[1])

    def grid_widgets(self) -> None:
        """
        Grid custom slider widgets
        """
        self.slider.grid(
            row=0, column=0, sticky="NSEW", pady=(
                (Theme.fontfactor * 18) + 30, 0))

    def get(self) -> float:
        """
        Get value of slider
        :return: Value of slider in float
        """
        return self.slider.get()

    def reset(self) -> None:
        """
        Reset slider to the from value
        """
        self.slider.set(self.range[0])
