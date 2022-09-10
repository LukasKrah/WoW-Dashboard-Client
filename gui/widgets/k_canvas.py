"""
gui/widgets/k_canvas.py

Project: WoW-Dashboard-Client
Created: 20.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import CTkCanvas
from typing import Callable
from tkinter import Widget


##################################################
#                     Code                       #
##################################################

class KCanvas(CTkCanvas):
    """
    CTKCanvas with small additions
    """
    custom_tag_count: int

    def __init__(self, master, *args, **kwargs) -> None:
        """
        Create CTKCanvas

        :param master: Master widget
        """
        super().__init__(master, *args, **kwargs)
        self.configure(
            bd=0,
            highlightthickness=0,
            width=0,
            height=0,
            background="snow")

        self.custom_tag_count = 0

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

    def create_rectangle_rounded_filled(
            self,
            x1: float,
            y1: float,
            x2: float,
            y2: float,
            *_args: any,
            r: float | None = 0,
            r_nw: float | None = None,
            r_ne: float | None = None,
            r_se: float | None = None,
            r_sw: float | None = None,
            **kwargs: any) -> str:
        """

        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param args:
        :param r: If a single cornor radius is not given this radius is used for it
        :param r_nw:
        :param r_ne:
        :param r_se:
        :param r_sw:
        :param kwargs:
        :return:
        """
        r_nw = r_nw if r_nw else r
        r_ne = r_ne if r_ne else r
        r_se = r_se if r_se else r
        r_sw = r_sw if r_sw else r

        self.custom_tag_count += 1
        tag = f"k_elem_{self.custom_tag_count}"

        self.create_rectangle(x1 + r_nw, y1, x2 - r_ne, y1 + max(r_nw, r_ne),
                              **kwargs, outline="", tags=[tag])
        self.create_rectangle(x2, y1 + r_ne, x2 - max(r_ne, r_se), y2 - r_se,
                              **kwargs, outline="", tags=[tag])
        self.create_rectangle(x1 + r_sw, y2, x2 - r_se, y2 - max(r_sw, r_se),
                              **kwargs, outline="", tags=[tag])
        self.create_rectangle(x1, y1 + r_nw, x1 + max(r_nw, r_sw), y2 - r_sw,
                              **kwargs, outline="", tags=[tag])
        self.create_rectangle(x1 + max(r_nw, r_sw), y1 + max(r_nw, r_ne),
                              x2 - max(r_ne, r_se), y2 - max(r_se, r_sw),
                              **kwargs, outline="", tags=[tag])

        bd = 0

        self.create_arc(x1 + bd,
                        y1 + bd,
                        x1 + (r_nw * 2),
                        y1 + (r_nw * 2),
                        start=90,
                        **kwargs,
                        outline="",
                        tags=[tag])
        self.create_arc(x2 - bd,
                        y1 + bd,
                        x2 - (r_ne * 2),
                        y1 + (r_ne * 2),
                        start=0,
                        **kwargs,
                        outline="",
                        tags=[tag])
        self.create_arc(x2 - bd,
                        y2 - bd,
                        x2 - (r_se * 2),
                        y2 - (r_se * 2),
                        start=270,
                        **kwargs,
                        outline="",
                        tags=[tag])
        self.create_arc(x1 + bd,
                        y2 - bd,
                        x1 + (r_sw * 2),
                        y2 - (r_sw * 2),
                        start=180,
                        **kwargs,
                        outline="",
                        tags=[tag])

        return tag
