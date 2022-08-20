"""
gui/instances/instance_viewmanager.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *

from gui.widgets.intern import KSlider
from style import Theme


##################################################
#                     Code                       #
##################################################

class InstanceViewManager(CTkCanvas):
    """
    ViewManager widget for InstanceTable
    """
    master: any
    views: dict
    view_elems: dict[str, any]

    def __init__(
            self,
            master: any,
            views: dict,
            *args: any,
            **kwargs: any) -> None:
        """
        Create ViewManager and grid widgets
        :param master: Master widget
        :param out_frame: Outframe for sizes (not the scrolling object)
        :param in_frame: Scrolling object
        """
        self.master = master
        self.views = views

        super().__init__(master, *args, **kwargs)

        self.configure(bd=0, highlightthickness=0,
                       background=Theme.background3)

        self.view_elems = {}
        for view in self.views:
            self.view_elems[view] = {"but": CTkButton(self, text=self.views[view]["name"],
                                                      command=lambda v=view: self.set_view(v)),
                                     "elems": []}

            for prop in self.views[view]["propertys"]:
                match self.views[view]["propertys"][prop]["type"]:
                    case "slider":
                        self.view_elems[view]["elems"].append(KSlider(
                            self,
                            self.views[view]["propertys"][prop]["name"],
                            self.views[view]["propertys"][prop]["valid_values"],
                            self.views[view]["propertys"][prop]["command"]
                        ))

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        for index, view in enumerate(self.view_elems):
            self.view_elems[view]["but"].grid(row=0, column=index, sticky="NSEW")
            self.grid_columnconfigure(index, weight=1)

    def set_view(self, view: str) -> None:
        for widget in self.grid_slaves():
            widget.grid_forget()
            del widget

        self.grid_widgets()

        for propindex, prop in enumerate(self.view_elems[view]["elems"]):
            prop.grid(row=propindex + 1, column=0, columnspan=len(self.views), sticky="NSEW")
            self.grid_rowconfigure(propindex + 1, weight=1)
        self.views[view]["command"]()
