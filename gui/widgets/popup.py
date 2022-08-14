"""
.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import *


##################################################
#                     Code                       #
##################################################

class ContextMenu(Menu):
    menu: list

    def __init__(self, master, menu: list, *args, **kwargs):
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


"""
import tkinter # Tkinter -> tkinter in Python 3

class FancyListbox(tkinter.Listbox):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Listbox.__init__(self, parent, *args, **kwargs)

        self.popup_menu = tkinter.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Delete",
                                    command=self.delete_selected)
        self.popup_menu.add_command(label="Select All",
                                    command=self.select_all)

        self.bind("<Button-3>", self.popup)  # Button-2 on Aqua

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        for i in self.curselection()[::-1]:
            self.delete(i)

    def select_all(self):
    
        self.selection_set(0, 'end')


root = tkinter.Tk()
flb = FancyListbox(root, selectmode='single')
for n in range(10):
    flb.insert('end', n)
flb.pack()
root.mainloop()"""