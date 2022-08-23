"""
gui/widgets/inputs.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################
from typing import Callable

from customtkinter import *
from tkinter import *

from style import Theme


##################################################
#                     Code                       #
##################################################

class KEntry(CTkCanvas):
    label: str
    entry: CTkEntry
    value: str
    valid_symbols: str | None
    textvar: StringVar

    def __init__(
            self,
            master,
            label: str,
            *args: any,
            value: str | None = None,
            valid_symbols: str | None = None,
            **kwargs: any) -> None:
        self.value = value

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
            fill=Theme.text_color,
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
            fg_color=Theme.background2,
            text_color=Theme.text_color,
            textvariable=self.textvar)

        self.textvar.trace_add("write", self.__change_text)

        self.grid_widgets()

        self.bind("<Expose>", self.default_value)

    def default_value(self, _event: Event) -> None:
        self.entry.delete(0, END)
        self.entry.insert(0, self.value) if self.value else ...

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
        value = self.entry.get()
        if self.value is not None:

            self.value = value
        return value

    def reset(self) -> None:
        self.entry.delete(0, END)


class KButtonGroupInput(CTkCanvas):
    master: any
    buttons: dict

    def __init__(
            self,
            master: any,
            buttons: dict,
            *args: any,
            **kwargs: any):
        self.master = master
        self.buttons = buttons

        super().__init__(master, *args, **kwargs)

    def grid_widgets(self) -> None:
        ...


class KOptionMenu(CTkCanvas):
    label: str
    optionMenu: CTkOptionMenu
    values: list[str]
    value: str

    def __init__(
            self,
            master,
            label: str,
            values: list[str],
            *args: any,
            value: str | None = None,
            **kwargs: any) -> None:
        self.value = value

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
            fill=Theme.text_color,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                18),
            anchor="nw")
        self.optionMenu = CTkOptionMenu(
            self,
            values=self.values,
            fg_color=Theme.primary_dark,
            button_color=Theme.primary_middle,
            button_hover_color=Theme.primary_light,
            text_color=Theme.text_color,
            text_font=(
                Theme.wow_font,
                Theme.fontfactor * 18))
        self.optionMenu.dropdown_menu.configure(
            tearoff=False,
            bg=Theme.background2,
            text_color="white",
            hover_color=Theme.background1,
            activeforeground="white")
        self.optionMenu.set(value) if value else ...
        self.grid_widgets()

        self.bind("<Expose>", self.default_value)

    def default_value(self, _event: Event) -> None:
        self.optionMenu.set(self.value) if self.value else ...

    def grid_widgets(self) -> None:
        self.optionMenu.grid(
            row=0, column=0, sticky="NSEW", pady=(
                (Theme.fontfactor * 18) + 30, 0))

    def get(self) -> str:
        value = self.optionMenu.get()
        if self.value is not None:
            self.value = value
        return value

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
            fill=Theme.text_color,
            font=(
                Theme.wow_font,
                Theme.fontfactor *
                18),
            anchor="nw")
        self.menuButton = CTkOptionMenu(
            self,
            text_color=Theme.text_color,
            fg_color=Theme.primary_dark,
            button_color=Theme.primary_middle,
            button_hover_color=Theme.primary_light,
            values=[
                self.label],
            text_font=(
                Theme.wow_font,
                Theme.fontfactor *
                18))
        self.menuButton.dropdown_menu.configure(
            tearoff=False,
            bg=Theme.background2,
            text_color=Theme.text_color,
            hover_color=Theme.background1,
            activeforeground=Theme.text_color)

        self.selection = {}
        for value in self.values:
            self.selection[value] = IntVar(value=0)
            self.menuButton.dropdown_menu.add_checkbutton(
                label=value,
                variable=self.selection[value],
                selectcolor=Theme.text_color,
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
    from_to: list[int, int]
    command: Callable[[float], None]

    slider: CTkSlider

    def __init__(
            self,
            master: any,
            label: str,
            from_to: str,
            commmand: Callable[[float], None],
            *args: any,
            **kwargs: any) -> None:
        """
        Create custom slider and grid widgets
        :param master: Master widget
        :param label: Label to display
        :param from_to: Slider range in form: "from:to"
        :param command: Slider callback command (will pass float-value)
        """
        self.master = master
        self.label = label
        self.command = commmand
        self.from_to = [int(ran) for ran in from_to.split(":")]

        super().__init__(self.master, *args, **kwargs)

        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)

        self.lab = Label(
            self,
            text=self.label,
            font=(
                Theme.wow_font,
                Theme.fontfactor * 18),
            background=Theme.background3,
            fg=Theme.text_color)
        self.slider = CTkSlider(
            self,
            from_=self.from_to[0],
            to=self.from_to[1],
            bg_color=Theme.background3,
            button_color=Theme.primary_middle,
            button_hover_color=Theme.primary_light,
            progress_color=Theme.background0,
            fg_color=Theme.background2,
            command=self.command,
            number_of_steps=self.from_to[1] -
            self.from_to[0])

        self.grid_widgets()

    def grid_widgets(self) -> None:
        """
        Grid custom slider widgets
        """
        self.lab.grid(row=0, column=0, sticky="NSEW")
        self.slider.grid(row=1, column=0, sticky="NSEW", ipady=5)

        self.grid_columnconfigure(0, weight=1)
        for index, weight in enumerate([1, 1]):
            self.grid_rowconfigure(index, weight=weight)

    def get(self) -> float:
        """
        Get value of slider
        :return: Value of slider in float
        """
        return self.slider.get()

    def set(self, value: float) -> None:
        self.slider.set(value)

    def reset(self) -> None:
        """
        Reset slider to the left
        """
        self.slider.set(self.from_to[0])
