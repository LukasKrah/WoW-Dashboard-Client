"""
gui/instances/instance_table.py

Project: WoW-Dashboard-Client
Created: 19.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import messagebox, Event, DISABLED
from customtkinter import CTkCanvas
from typing import Literal

from data import WeeklySettings, InstanceManager, Settings
from gui.widgets import KTable, KCanvas, KImage
from style import Theme, ImageManager

from .instance_headers import InstanceColHeader, InstanceRowHeader
from .instance_viewmanager import InstanceViewManager
from .instance_navbar import InstanceNavBar
from .instance_cells import InstanceCell


##################################################
#                     Code                       #
##################################################

class InstanceTable(KCanvas):
    """
    Instances Table (colums: chars, rows: instances)
    """
    master: any

    table: KTable
    navBar: InstanceNavBar

    relheight: float

    def __init__(
            self,
            *args: any,
            **kwargs: any) -> None:
        """
        Create InstanceTable, grid widgets and load in __values
        """

        super().__init__(*args, **kwargs)
        self.configure(background=Theme.background3)

        self.relheight = 5.0

        self.table_frame = CTkCanvas(self)
        photo = KImage("style/images/shadowlands.jpg")
        photo.resize(self.winfo_screenwidth() // 11 * 10, 1, "cover")
        self.table_frame.create_image(0, 0, image=photo.imgTk, anchor="nw")
        self.table_frame.photo = photo.imgTk
        self.table_frame.configure(
            background=Theme.background1,
            bd=0,
            highlightthickness=0)
        self.table = KTable(
            self.table_frame,
            rowheaders=[
                InstanceRowHeader,
                InstanceRowHeader],
            colheaders=[InstanceColHeader],
            cells=InstanceCell)
        self.table.topleft = InstanceViewManager(
            self.table,
            set_view_callback=self.set_view,
            scale_view_callback=self.scale_view)

        self.reload_table()
        self.navBar = InstanceNavBar(self, self.set_week,
                                     new_char_callback=self.add_char_callback,
                                     new_todo_callback=self.add_todo_callback)

        InstanceManager.reload_observable.on("reload", self.reload_table)
        WeeklySettings.reload_observable.on("reload", self.reload_table)

        self._grid_widgets()

    def scale_view(self, value: float) -> None:
        self.relheight = value
        event = Event()
        event.delta = 0
        self.scroll(event)

    def set_view(self, view: str) -> None:
        match view:
            case "scrollable":
                self.table.bind_all("<MouseWheel>", self.scroll)
                self.scale_view(self.relheight)

            case "default":
                self.table.bind_all("<MouseWheel>", DISABLED)
                self.table.place(
                    x=0, y=0, anchor="nw", relwidth=1, relheight=1)

    def scroll(self, event: Event | None = None,
               null: bool | None = False) -> None:
        if WeeklySettings.values["view"]["selectedView"] != "scrollable":
            return
        new_y = self.table.winfo_y() + (event.delta if event else 0)

        if new_y > 0 or self.table.winfo_height() < self.table_frame.winfo_height() or null:
            new_y = 0
        elif new_y < (-self.table.winfo_height() + self.table_frame.winfo_height()):
            new_y = -self.table.winfo_height() + self.table_frame.winfo_height()
        self.table.place(
            x=0,
            y=new_y,
            anchor="nw",
            relwidth=1,
            relheight=(len([instance for instance in InstanceManager.values
                            if InstanceManager.values[instance]["active"]]) + 1) /
            self.relheight)

    def _grid_widgets(self) -> None:
        """
        Grid Widgets
        """

        self.table_frame.grid(row=0, column=0, sticky="NSEW")
        self.navBar.grid(row=1, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def reload_table(self) -> None:
        """
        Load rows, columns and __values and relaod table
        """
        rows = [{"row": InstanceManager.values[instance]["row"],
                 "headers": [{"label": instance,
                              "name": instance},
                             {"label": ','.join(InstanceManager.values[instance]["difficulty"].keys()),
                              "name": instance}]
                 } for instance in InstanceManager.values.keys() if InstanceManager[instance]["active"]]

        columns = [{"column": WeeklySettings["chars"][char]["column"],
                    "headers": [{'label': f'{WeeklySettings["chars"][char]["characterName"].lower()}:'
                                          f'{WeeklySettings["chars"][char]["realmSlug"].lower()}',
                                 "name": char}]}
                   for char in WeeklySettings["chars"] if WeeklySettings["chars"][char]["active"]]

        self.scroll()
        self.table.reload(
            rows=rows,
            columns=columns,
            values=InstanceManager.values)

    def add_char_callback(self, name: str, realm: str) -> None:
        """
        Add a char to the settings and reload table
        :param name: Name of the char
        :param realm: Realm on which the char is playing
        """
        Settings.values["add_char"]["last_realm"] = realm

        charname = f"{name}:{realm}".lower()

        add = True
        for char in WeeklySettings["chars"]:
            if charname == char and not WeeklySettings["chars"][char]["active"]:
                if not messagebox.askyesno(
                    "Char hinzufügen",
                    "Dieser Char befindet sich noch im Papierkorb!\n"
                    "Möchtest du ihn wiederherstellen?"
                ):
                    for instance in InstanceManager.values:
                        for diff in InstanceManager.values[instance]["difficulty"]:
                            if charname in InstanceManager.values[instance]["difficulty"][diff]["chars"]:
                                del InstanceManager.values[instance]["difficulty"][diff]["chars"][charname]

            elif charname == char:
                messagebox.showwarning(
                    "Char hinzufügen",
                    "Dieser Char existiert bereits!")
                add = False

        if add:
            try:
                column = max([WeeklySettings.values["chars"][char]["column"] for char in WeeklySettings.values["chars"]
                              if "column" in WeeklySettings.values["chars"][char]]) + 1
            except ValueError:
                column = 0
            WeeklySettings["chars"][charname] = {
                "characterName": name,
                "realmSlug": realm,
                "active": True,
                "column": column}

            for instance in InstanceManager.values:
                for diff in InstanceManager.values[instance]["difficulty"]:
                    InstanceManager.values[instance]["difficulty"][diff]["chars"][charname] = {
                        "done": None}

            WeeklySettings.write()
            InstanceManager.write()
            self.scroll(null=True)
            self.reload_table()

    def add_todo_callback(self,
                          name: str,
                          typ: Literal["Daily",
                                       "Weekly"],
                          diff: str) -> None:
        """
        Add an instance to the InstanceManager __values and reload table
        :param name: Name of the Instancce
        :param typ: Whether the instance is daily or weekly
        :param diff: Different difficultys of the instance
        """
        Settings.values["add_todo"]["last_typ"] = typ
        try:
            row = max([InstanceManager.values[instance]["row"] for instance in InstanceManager.values
                       if "row" in InstanceManager.values[instance]]) + 1
        except ValueError:
            row = 0

        if name not in InstanceManager.values:
            InstanceManager.values[name] = {
                "type": typ,
                "row": row,
                "image": ImageManager.get_image(name),
                "active": True,
                "difficulty": {
                    dif: {"chars": {
                        char: {"done": None} for char in WeeklySettings.values["chars"]
                    }} for dif in diff.split(", ")
                } if diff else {"": {"chars": {
                    char: {"done": None} for char in WeeklySettings.values["chars"]
                }}}
            }
        elif not InstanceManager.values[name]["active"]:
            InstanceManager.values[name]["active"] = True
            if not messagebox.askyesno(
                    "Instanz hinzufügen",
                    "Diese Instanz befindet sich noch im Papierkorb!\n"
                    "Möchtest du sie wiederherstellen?"):
                try:
                    row = max([InstanceManager.values[instance]["row"] for instance in InstanceManager.values
                               if "row" in InstanceManager.values[instance]]) + 1
                except ValueError:
                    row = 0
                InstanceManager.values[name] = {
                    "type": typ,
                    "row": row,
                    "image": ImageManager.get_image(name),
                    "active": True,
                    "difficulty": {
                        dif: {"chars": {
                            char: {"done": None} for char in WeeklySettings.values["chars"]
                        }} for dif in diff.split(", ")
                    } if diff else {"": {"chars": {
                        char: {"done": None} for char in WeeklySettings.values["chars"]
                    }}}
                }
            else:
                InstanceManager.values[name]["active"] = True
                try:
                    InstanceManager.values[name]["row"] = max([InstanceManager.values[instance]["row"]
                                                               for instance in InstanceManager.values
                                                               if "row" in InstanceManager.values[instance]]) + 1
                except ValueError:
                    InstanceManager.values[name]["row"] = 0
        else:
            messagebox.showwarning(
                "Instanz hinzufügen",
                "Dieses Instanz existiert bereits!")
        self.scroll(null=True)
        InstanceManager.write()
        self.reload_table()

    def set_week(self, week: str) -> None:
        """
        Set week to display in the table
        :param week: File name of the week (week_year.json)
        :return:
        """
        WeeklySettings.write()
        InstanceManager.write()
        WeeklySettings.today = week
        InstanceManager.today = week
        self.table.topleft.reload()
        self.scroll(null=True)
        self.reload_table()
