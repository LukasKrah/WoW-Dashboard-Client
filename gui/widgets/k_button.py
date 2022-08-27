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

class KButton(CTkButton):
    def __init__(self, master: any, *args: any, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)

    def stop_scaling(self) -> None:
        self.bind('<Configure>', DISABLED)

    def resume_scaling(self) -> None:
        self.bind('<Configure>', self.update_dimensions_event)

    def bind_all_widgets(self: Widget, sequence: str | None = ..., func: Callable[[
            any], any] | None = ..., add: bool | None = ...) -> None:
        """
        Recursive widget bind function

        :param sequence: Bind (e.g: <Button-1>)
        :param func: callback
        :param add: IDK
        """
        for widget in self.grid_slaves():
            KButton.bind_all_widgets(widget, sequence, func, add)
            widget.bind(sequence, func, add)
