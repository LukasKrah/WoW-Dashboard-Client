"""
.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable
from customtkinter import *
from tkinter import *


##################################################
#                     Code                       #
##################################################

class KCanvas(CTkCanvas):
    """
    CTKCanvas with small additions
    """

    def __init__(self, master, *args, **kwargs) -> None:
        """
        Create CTKCanvas

        :param master: Master widget
        """
        super().__init__(master, *args, **kwargs)
        self.configure(bd=0, highlightthickness=0, width=0, height=0)

    def bind_all_widgets(self: Widget, sequence: str | None = ..., func: Callable[[
            any], any] | None = ..., add: bool | None = ...) -> None:
        """
        Recursive widget bind function

        :param sequence: Bind (e.g: <Button-1>)
        :param func: callback
        :param add: IDK
        """
        for widget in self.grid_slaves():
            KCanvas.bind_all_widgets(widget, sequence, func, add)
            widget.bind(sequence, func, add)
