"""
.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date, timedelta
from typing import Callable, Union
from customtkinter import *
from os import listdir
from tkinter import *

from style import Theme

from .popup import PopUp

##################################################
#                     Code                       #
##################################################


class NavBar(CTkCanvas):
    weeks: dict[str, str]
    week_call: Callable
    new_char_popup: PopUp
    new_ToDo_popup: PopUp

    def __init__(self, master, week_call: Callable,
                 new_char_callback: Callable[[str, str], None],
                 new_todo_callback: Callable[[str, str, str], None],
                 *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.new_char_callback = new_char_callback
        self.new_todo_callback = new_todo_callback

        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background1,
            height=50)
        self.master = master
        self.week_call = week_call

        self.new_char_popup = PopUp(self, "Neuer Char", inputs=[{"type": "InputText", "label": "Name"},
                                                  {"type": "InputText", "label": "Realm"}],
                                    confirm_call=self.new_char_callback)
        self.new_ToDo_popup = PopUp(self, "Neuer Char",
                                    inputs=[{"type": "InputText", "label": "Name"},
                                            {"type": "OptionMenu", "label": "Typ", "validValues": ["Daily", "Weekly"]},
                                            {"type": "ComboBox", "label": "Difficultys", "validValues": ["NHC 10", "NHC 25", "HC 10", "HC 25", "M"]}],
                                    confirm_call=self.new_todo_callback)
        self.new_ToDo = CTkButton(self, text="Neues ToDo", text_font=(Theme.wow_font2, Theme.fontfactor*18),
                                  command=self.new_ToDo_popup.open_popup)
        self.new_char = CTkButton(self, text="Neuer Char", text_font=(Theme.wow_font2, Theme.fontfactor*18),
                                  command=self.new_char_popup.open_popup)

        self.weeks = {}
        today = list((date.today() + timedelta(days=5, hours=15)).isocalendar())
        thisweek = f"{today[1]}_{today[0]}.json"
        for file in listdir("data/instance_data"):
            if file.endswith(".json") and "default" not in file:
                if file == thisweek:
                    self.weeks["Diese Woche"] = file
                else:
                    self.weeks[file.rstrip(".json")] = file

        self.weekvar = StringVar()
        self.week = CTkOptionMenu(self, values=list(self.weeks.keys()), command=self.week_call)
        self.week.set("Diese Woche")

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.new_ToDo.grid(row=0, column=0, sticky="NSEW", padx=(0, 20))
        self.new_char.grid(row=0, column=1, sticky="NSEW")
        self.week.grid(row=0, column=3, sticky="NSEW")

        for index, weight in enumerate([1, 1, 5, 1]):
            self.grid_columnconfigure(index, weight=weight)
        self.grid_rowconfigure(0, weight=1)
