"""
widgets/k_contextmenu.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

# from customtkinter import *
from tkinter import *

from style import Theme


##################################################
#                     Code                       #
##################################################

class KContextMenu(Menu):
    """
    Custum ContextMenu (Menu) mainly for right click
    """
    menu: list

    def __init__(self, master, menu: list, *args: any, **kwargs: any) -> None:
        """
        Create ContextMenu and add commands

        :param master: master widget
        :param menu: Command List
        """
        super().__init__(master, tearoff=0, *args, **kwargs)
        self.configure(background=Theme.background0, activebackground="red")
        self.menu = menu

        for menupoint in menu:
            self.add_command(label=menupoint["label"],
                             command=menupoint["command"], font=(Theme.wow_font, Theme.fontfactor*18))

    def change_label(self, index: int, newtext: str) -> None:
        """
        Change command label

        :param index: Index of the command in list
        :param newtext: New text
        :return:
        """
        self.delete(index)
        self.menu[index]["label"] = newtext
        self.insert_command(index, label=self.menu[index]["label"],
                            command=self.menu[index]["command"],
                            font=(Theme.wow_font, Theme.fontfactor*18))

    def popup(self, event: Event) -> None:
        """
        Open PopUp

        :param event: Event with x_root, y_root coors
        """
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.grab_release()
