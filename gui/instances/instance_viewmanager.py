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
    view_elems: list[any]

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

        self.view_elems = []
        for view in self.views:
            for prop in self.views[view]["propertys"]:
                match self.views[view]["propertys"][prop]["type"]:
                    case "slider":
                        self.view_elems.append(KSlider(
                            self,
                            self.views[view]["propertys"][prop]["name"],
                            self.views[view]["propertys"][prop]["valid_values"]
                        ))

        self.grid_widgets()

    def grid_widgets(self) -> None:
        ...
