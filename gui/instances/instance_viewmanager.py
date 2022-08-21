"""
gui/instances/instance_viewmanager.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from json import loads, dumps
from typing import Callable
from customtkinter import *
from os import listdir

from gui.widgets.intern import KSlider
from gui.widgets import KContextMenu, KCanvas
from style import Theme
from data import Settings


##################################################
#                     Code                       #
##################################################

class InstanceViewManager(KCanvas):
    """
    ViewManager widget for InstanceTable
    """
    master: any
    set_view_callback: Callable[[str], None]
    scale_view_callback: Callable

    view_elems: dict[str, any]

    con: KContextMenu

    def __init__(
            self,
            master: any,
            *args: any,
            set_view_callback: Callable[[str], None] | None = None,
            scale_view_callback: Callable[[any], None] | None = None,
            **kwargs: any) -> None:
        """
        Create ViewManager and grid widgets

        :param master: Master widget
        :param out_frame: Outframe for sizes (not the scrolling object)
        :param in_frame: Scrolling object
        """
        self.master = master
        self.set_view_callback = set_view_callback
        self.scale_view_callback = scale_view_callback

        super().__init__(master, *args, **kwargs)

        self.con = KContextMenu(self,
                                [{"label": "Diese Ansicht für alle Wochen übernehmen",
                                  "command": self.set_view_all}])

        self.configure(bd=0, highlightthickness=0,
                       background=Theme.background3)

        self.reload()

    def reload(self) -> None:
        self.view_elems = {}
        for view in Settings["view"]["views"]:
            self.view_elems[view] = {
                "but": CTkButton(
                    self,
                    text=Settings["view"]["views"][view]["name"],
                    command=lambda v=view: self.set_view(v),
                    text_font=(
                        Theme.wow_font,
                        Theme.fontfactor * 18)),
                "propertys": {}}

            for index, prop in enumerate(
                    Settings["view"]["views"][view]["propertys"]):
                match Settings["view"]["views"][view]["propertys"][prop]["type"]:
                    case "slider":
                        self.view_elems[view]["propertys"][prop] = KSlider(
                            self,
                            Settings["view"]["views"][view]["propertys"][prop]["name"],
                            Settings["view"]["views"][view]["propertys"][prop]["valid_values"],
                            lambda v=view, i=index: self.set(view=view)
                        )
                        self.view_elems[view]["propertys"][prop].set(
                            Settings["view"]["views"][view]["propertys"][prop]["value"])

        self.set_view(Settings["view"]["selectedView"])

    def set(self, view: str) -> None:
        values = []
        for index, prop in enumerate(self.view_elems[view]["propertys"]):
            Settings["view"]["views"][view]["propertys"][prop]["value"] = \
                self.view_elems[view]["propertys"][prop].get()
            values.append(Settings["view"]["views"][view]
                          ["propertys"][prop]["value"])

        try:
            self.scale_view_callback(
                *values) if self.scale_view_callback else None
        except TypeError:
            ...

    def grid_widgets(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        for index, view in enumerate(self.view_elems):
            self.view_elems[view]["but"].grid(
                row=0, column=index, sticky="NSEW")
            self.grid_columnconfigure(index, weight=1)

    def set_view(self, view: str) -> None:
        Settings.values["view"]["selectedView"] = view
        Settings.write()
        for widget in self.grid_slaves():
            gridinfos = widget.grid_info()
            self.grid_rowconfigure(gridinfos["row"], weight=0)
            self.grid_columnconfigure(gridinfos["column"], weight=0)
            widget.grid_forget()
            del widget

        self.grid_widgets()

        for propindex, prop in enumerate(self.view_elems[view]["propertys"]):
            self.view_elems[view]["propertys"][prop].grid(
                row=propindex + 1,
                column=0,
                columnspan=len(
                    Settings["view"]["views"][view]),
                sticky="NSEW")
            self.grid_rowconfigure(propindex + 1, weight=1)
        self.set_view_callback(view) if self.set_view_callback else None
        self.set(view)

        self.bind_all_widgets("<Button-3>", self.con.popup)

    def set_view_all(self) -> None:  # noqa
        for file in listdir("data/settings"):
            if file.endswith(".json") and file != "default.json":
                with open(f"data/settings/{file}", "r") as data:
                    values = loads(data.read())
                    selected_view = Settings["view"]["selectedView"]
                    values["view"]["selectedView"] = selected_view
                    values["view"]["views"][selected_view] = Settings["view"]["views"][selected_view]
                with open(f"data/settings/{file}", "w") as data:
                    data.write(dumps(values))
