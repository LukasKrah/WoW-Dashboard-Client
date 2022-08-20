"""
gui/instances/k_table.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import messagebox
from customtkinter import *
from tkinter import *
from typing import Literal

from gui.widgets import KTable
from style import Theme, ImageManager
from data import Settings, InstanceManager

from .instance_headers import InstanceColHeader, InstanceRowHeader
from .instance_cells import InstanceCell
from .instance_navbar import InstanceNavBar
from .instance_viewmanager import InstanceViewManager


##################################################
#                 Menu classes                   #
##################################################


class InstanceTable(CTkCanvas):
    """
    Instances Table (colums: chars, rows: instances)
    """
    table: KTable
    navBar: InstanceNavBar

    relheight: float

    def __init__(self, *args: any, **kwargs: any) -> None:
        """
        Create InstanceTable, grid widgets and load in __values
        """
        super().__init__(*args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            background=Theme.background3)

        self.relheight = 5.0

        self.table_frame = CTkFrame(self)
        self.table = KTable(
            self.table_frame,
            rowheaders=[
                InstanceRowHeader,
                InstanceColHeader],
            colheaders=[InstanceColHeader],
            cells=InstanceCell)
        self.table.topleft = InstanceViewManager(self.table, {
            "default": {
                "name": "Tabelle (Gesamt)",
                "command": lambda view="default": self.set_view(view),
                "propertys": {
                }
            },
            "scrollable": {
                "name": "Tabelle (scrollbar)",
                "command": lambda view="scrollable": self.set_view(view),
                "propertys": {
                    "sizing": {
                        "name": "Skalierung",
                        "type": "slider",
                        "valid_values": "3:12",
                        "command": self.scale_view
                    }
                }
            }
        })

        self.reload_table()
        self.navBar = InstanceNavBar(self, self.set_week,
                                     new_char_callback=self.add_char_callback,
                                     new_todo_callback=self.add_todo_callback)

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
                self.table.place(x=0, y=0, anchor="nw", relwidth=1, relheight=1)

    def scroll(self, event: Event) -> None:
        new_y = self.table.winfo_y() + event.delta

        if new_y > 0:
            new_y = 0
        elif new_y < (-self.table.winfo_height() + self.table_frame.winfo_height()):
            new_y = -self.table.winfo_height() + self.table_frame.winfo_height()
        self.table.place(
            x=0,
            y=new_y,
            anchor="nw",
            relwidth=1,
            relheight=len(
                InstanceManager.values) /
            self.relheight)

    def _grid_widgets(self) -> None:
        """
        Grid Widgets
        """
        self.table.place(
            x=0,
            y=0,
            anchor="nw",
            relwidth=1,
            relheight=len(
                InstanceManager.values) /
            10)

        self.table_frame.grid(row=0, column=0, sticky="NSEW")
        self.navBar.grid(row=1, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def reload_table(self) -> None:
        """
        Load rows, columns and __values and relaod table
        """
        rows = [[instance, ",".join(InstanceManager.values[instance]["difficulty"].keys(
        ))] for instance in InstanceManager.values.keys() if InstanceManager[instance]["active"]]
        columns = [[f'{Settings["chars"][char]["characterName"].lower()}:{Settings["chars"][char]["realmSlug"].lower()}']
                   for char in Settings["chars"]]

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
        charname = f"{name}:{realm}".lower()

        add = True
        for char in Settings["chars"]:
            if charname == char:
                messagebox.showwarning(
                    "Char hinzufügen",
                    "Dieser Char existiert bereits!")
                add = False

        if add:
            Settings["chars"][charname] = {
                "characterName": name, "realmSlug": realm}
            Settings.write()
            self.reload_table()

    def add_todo_callback(self,
                          name: str,
                          typ: Literal["daily",
                                       "weekly"],
                          diff: str) -> None:
        """
        Add an instance to the InstanceManager __values and reload table

        :param name: Name of the Instancce
        :param typ: Whether the instance is daily or weekly
        :param diff: Different difficultys of the instance
        """
        for index in range(2):
            if name not in InstanceManager.values or index == 1:
                InstanceManager.values[name] = {
                    "type": typ,
                    "image": ImageManager.get_image(name),
                    "active": True,
                    "difficulty": {
                        dif: {"chars": {}} for dif in diff.split(", ")
                    } if diff else {"": {"chars": {}}}
                }
                break
            elif not InstanceManager.values[name]["active"]:
                if messagebox.askyesno(
                    "ToDo hinzufügen",
                    "Dieses ToDo befindet sich noch im Papierkorb!\n"
                        "Möchtest du es überschreiben?"):
                    continue
                break
            else:
                messagebox.showwarning(
                    "ToDo hinzufügen",
                    "Dieses ToDo existiert bereits!")
                break

        InstanceManager.write()
        self.reload_table()

    def set_week(self, week: str) -> None:
        """
        Set week to display in the table

        :param week: File name of the week (week_year.json)
        :return:
        """
        InstanceManager.today = week
        Settings.today = week
        self.reload_table()
