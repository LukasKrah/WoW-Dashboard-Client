"""
gui/instances/instance_navbar.py

Project: WoW-Dashboard-Client
Created: 13.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import CTkButton, CTkOptionMenu
from datetime import date, timedelta
from typing import Callable, Literal
from tkinter import StringVar
from os import listdir

from gui.widgets import KPopUp, KCanvas
from data import WeeklySettings, Settings
from style import Theme

##################################################
#                     Code                       #
##################################################


class InstanceNavBar(KCanvas):
    """
    Bottom NavBar of the InstanceTable
    """
    master: any
    week_call: Callable[[str], None]
    new_char_callback: Callable[[str, str], None]
    new_todo_callback: Callable[[str, Literal["Daily", "Weekly"], str], None]

    weeks: dict[str, str]

    new_char: CTkButton
    new_todo: CTkButton
    new_char_popup: KPopUp
    new_todo_popup: KPopUp
    weekvar = StringVar
    week: CTkOptionMenu

    def __init__(self,
                 master: any,
                 week_call: Callable[[str], None],
                 new_char_callback: Callable[[str, str], None],
                 new_todo_callback: Callable[[str, Literal["Daily", "Weekly"], str], None],
                 *args, **kwargs) -> None:
        """
        Test

        :param master: Master widget/frame
        :param week_call: Callback when week selection is changed (will pass week str)
        :param new_char_callback: Callback when new char is created (will pass name + realm)
        :param new_todo_callback: Callback when new isntance is created (will pass name + type + diff)
        """
        self.master = master
        self.week_call = week_call
        self.new_char_callback = new_char_callback
        self.new_todo_callback = new_todo_callback

        super().__init__(master, *args, **kwargs)

        self.configure(
            background=Theme.background1,
            height=50)

        # NewChar
        self.new_char_popup = KPopUp(self,
                                     "Neuer Char",
                                     inputs=[{"type": "InputText",
                                              "label": "Name"},
                                             {"type": "InputText",
                                              "label": "Realm",
                                              "value": Settings.values["add_char"]["last_realm"]}],
                                     confirm_call=self.new_char_callback)
        self.new_char = CTkButton(
            self,
            text="Neuer Char",
            fg_color=Theme.primary_middle,
            hover_color=Theme.primary_light,
            text_color=Theme.text_color,
            text_font=(
                Theme.wow_font,
                Theme.fontfactor * 18),
            command=self.new_char_popup.open_popup)

        # NewToDo
        self.new_todo_popup = KPopUp(self,
                                     "Neues ToDo",
                                     inputs=[{"type": "InputText",
                                              "label": "Name"},
                                             {"type": "OptionMenu",
                                              "label": "Typ",
                                              "value": Settings.values["add_todo"]["last_typ"],
                                              "validValues": ["Daily",
                                                              "Weekly"]},
                                             {"type": "ComboBox",
                                              "label": "Difficultys",
                                              "validValues": ["Normal 10",
                                                              "Normal 25",
                                                              "Heroisch 10",
                                                              "Heroisch 25",
                                                              "Mythisch"]}],
                                     confirm_call=self.new_todo_callback)
        self.new_todo = CTkButton(
            self,
            text="Neues ToDo",
            fg_color=Theme.primary_middle,
            hover_color=Theme.primary_light,
            text_color=Theme.text_color,
            text_font=(
                Theme.wow_font,
                Theme.fontfactor * 18),
            command=self.new_todo_popup.open_popup)

        # Week Selection
        self.weeks = {}
        today = list(
            (date.today() +
             timedelta(
                days=5,
                hours=15)).isocalendar())
        thisweek = f"{today[1]}_{today[0]}.json"
        for file in listdir("data/instance_data"):
            if file.endswith(".json") and "default" not in file:
                if file == thisweek:
                    self.weeks["Diese Woche"] = file
                else:
                    splitfile = file.rstrip(".json").split("_")
                    self.weeks[f"KW{splitfile[0]}-{splitfile[1]}"] = file

        self.weekvar = StringVar()
        self.week = CTkOptionMenu(
            self,
            fg_color=Theme.primary_dark,
            button_color=Theme.primary_middle,
            button_hover_color=Theme.primary_light,
            text_color=Theme.text_color,
            values=list(
                self.weeks.keys()),
            command=self.call_week,
            text_font=(
                Theme.wow_font,
                Theme.fontfactor * 18
            ))
        self.week.set("Diese Woche")

        # Grid widgets
        self.grid_widgets()

    def call_week(self, value: str) -> None:
        self.week_call(self.weeks[value])

    def grid_widgets(self) -> None:
        """
        Grid navBar widgets
        """
        self.new_todo.grid(row=0, column=0, sticky="NSEW", padx=(0, 20))
        self.new_char.grid(row=0, column=1, sticky="NSEW")
        self.week.grid(row=0, column=3, sticky="NSEW")

        for index, weight in enumerate([1, 1, 5, 1]):
            self.grid_columnconfigure(index, weight=weight)
        self.grid_rowconfigure(0, weight=1)
