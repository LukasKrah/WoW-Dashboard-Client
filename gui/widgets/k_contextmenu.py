"""
widgets/k_contextmenu.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

# from customtkinter import *
from tkinter import *


##################################################
#                     Code                       #
##################################################

class KContextMenu(Menu):
    menu: list

    def __init__(self, master, menu: list, *args: any, **kwargs: any) -> None:
        super().__init__(master, tearoff=0, *args, **kwargs)
        self.menu = menu

        for menupoint in menu:
            self.add_command(label=menupoint["label"],
                             command=menupoint["command"])

    def change_label(self, index: int, newtext: str) -> None:
        self.delete(index)
        self.menu[index]["label"] = newtext
        self.insert_command(index, label=self.menu[index]["label"],
                            command=self.menu[index]["command"])

    def popup(self, event: Event) -> None:
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.grab_release()
