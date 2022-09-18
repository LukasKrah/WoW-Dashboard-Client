"""
gui/widgets/k_canvas.py

Project: WoW-Dashboard-Client
Created: 20.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable, Literal
from customtkinter import CTkCanvas
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

    def __gen_new_tag(self) -> str:
        self.custom_tag_count += 1
        return f"k_elem_{self.custom_tag_count}"

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

    def create_gradient(
            self,
            x1: int | None = None,
            y1: int | None = None,
            x2: int | None = None,
            y2: int | None = None,
            resolution: int | None = 5,
            from_color: str | None = "#000000",
            to_color: str | None = None,
            to_factor: float | None = 0.5,
            tags: list | None = None,
            **kwargs: any
    ) -> str:
        """Draw the gradient"""
        tag = [self.__gen_new_tag()]

        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        x1 = x1 if x1 else 0
        y1 = y1 if y1 else 0
        x2 = x2 if x2 else canvas_width
        y2 = y2 if y2 else canvas_height

        width = x2 - x1
        height = y2 - y1

        limit = max(width, height) // resolution
        (r1, g1, b1) = self.winfo_rgb(from_color)

        if to_color:
            (r2, g2, b2) = self.winfo_rgb(to_color)
        else:
            r2 = r1 * to_factor
            g2 = g1 * to_factor
            b2 = b1 * to_factor

        if limit != 0:
            r_ratio = float(r2-r1) / limit
            g_ratio = float(g2-g1) / limit
            b_ratio = float(b2-b1) / limit

            for i in range(limit):
                nr = int(r1 + (r_ratio * i))
                ng = int(g1 + (g_ratio * i))
                nb = int(b1 + (b_ratio * i))

                color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)

                if i < limit/2:
                    self.create_polygon(x1 + width * i / limit * 2 - 1, y1,
                                        x1 + width * i / limit * 2 + resolution * 2, y1,
                                        x1, height * i / limit * 2 + resolution * 2 + y1,
                                        x1, height * i / limit * 2 - 1 + y1,
                                        outline=color,
                                        tags=tag + tags if tags else None, fill=color, **kwargs)
                else:
                    self.create_polygon(x1 + width * i / limit * 2 - width - 1, height + y1,
                                        x1 + width * i / limit * 2 - width + resolution * 2, height + y1,
                                        x1 + width, height * i / limit * 2 - height + resolution * 2 + y1,
                                        x1 + width, height * i / limit * 2 - height - 1 + y1,
                                        tags=tag + tags if tags else None, fill=color, width=resolution*2, **kwargs)

        return tag[0]

    def create_rounded_cornor(
            self,
            pos_x: float | None = 0,
            pos_y: float | None = 0,
            radius: int | None = 20,
            cornor: Literal["nw", "ne", "se", "sw"] | None = "nw",
            tags: list | None = None,
            **kwargs: any
    ) -> str:
        tag = [self.__gen_new_tag()]

        for rad in range(radius):
            calc_x: float
            calc_y: float

            if cornor == "nw":
                calc_x = pos_x + radius - rad
                calc_y = pos_y + rad
            elif cornor == "ne":
                calc_x = pos_x - radius + rad
                calc_y = pos_y + rad
            elif cornor == "se":
                calc_x = pos_x - radius + rad
                calc_y = pos_y - rad
            else:
                calc_x = pos_x + radius - rad
                calc_y = pos_y - rad

            self.create_line(pos_x, calc_y, calc_x, pos_y,
                             tags=tag + tags if tags else None, **kwargs)
        self.create_rectangle(pos_x-1, pos_y-1, pos_x, pos_y,
                              tags=tag + tags if tags else None, **kwargs)

        return tag[0]

    def rounded_cornors(
            self,
            x1: int | None = None,
            y1: int | None = None,
            x2: int | None = None,
            y2: int | None = None,
            radius: int | None = 50,
            **kwargs: any
    ) -> str:
        x1 = x1 if x1 else 0
        y1 = y1 if y1 else 0
        x2 = x2 if x2 else self.winfo_width()
        y2 = y2 if y2 else self.winfo_height()

        tag = self.__gen_new_tag()

        self.create_rounded_cornor(x1, y1, radius, "nw", **kwargs)
        self.create_rounded_cornor(x2, y1, radius, "ne", **kwargs)
        self.create_rounded_cornor(x2, y2, radius, "se", **kwargs)
        self.create_rounded_cornor(x1, y2, radius, "sw", **kwargs)

        return tag

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

        tag = self.__gen_new_tag()

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
