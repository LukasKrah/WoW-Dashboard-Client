"""
.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date, timedelta
from typing import Callable
from customtkinter import *
from os import listdir
from tkinter import *

from style import Theme

##################################################
#                     Code                       #
##################################################


class NavBar(CTkCanvas):
    weeks: dict[str, str]
    week_call: Callable

    def __init__(self, master, week_call: Callable, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1,
            height=50)
        self.master = master
        self.week_call = week_call

        self.new_ToDo = CTkButton(
            self, text="Neues ToDo", text_font=(
                Theme.wow_font2, Theme.fontfactor * 18))
        self.new_char = CTkButton(
            self, text="Neuer Char", text_font=(
                Theme.wow_font2, Theme.fontfactor * 18))

        self.weeks = {}
        today = list(
            (date.today() +
             timedelta(
                days=5,
                hours=15)).isocalendar())
        thisweek = f"{today[1]}_{today[0]}.json"
        for file in listdir("data/instance_data"):
            if file.endswith(".json"):
                if file == thisweek:
                    self.weeks["Diese Woche"] = file
                else:
                    self.weeks[file.rstrip(".json")] = file

        self.weekvar = StringVar()
        self.week = CTkOptionMenu(
            self,
            values=list(
                self.weeks.keys()),
            command=self.week_call)
        self.week.set("Diese Woche")

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.new_ToDo.grid(row=0, column=0, sticky="NSEW", padx=(0, 20))
        self.new_char.grid(row=0, column=1, sticky="NSEW")
        self.week.grid(row=0, column=3, sticky="NSEW")

        for index, weight in enumerate([1, 1, 5, 1]):
            self.grid_columnconfigure(index, weight=weight)
        self.grid_rowconfigure(0, weight=1)
