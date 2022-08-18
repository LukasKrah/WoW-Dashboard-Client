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

from style import Theme
from .inputs import KEntry, KOptionMenu, KMenu


##################################################
#                     Code                       #
##################################################

class ContextMenu(Menu):
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


class PopUp(CTkToplevel):
    inputs: list[dict]
    input_elems: list[KEntry | KOptionMenu | KMenu]
    buttons: list[CTkButton]
    confirm_call: Callable

    def __init__(self, master, title: str, *args: any, inputs: list[dict], confirm_call: Callable, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(background=Theme.background1)

        self.withdraw()
        self.master = master
        self.inputs = inputs
        self.confirm_call = confirm_call
        self.input_elems = []
        self.buttons = []

        self.wm_iconbitmap("style/images/wow_icon.ico")

        for _input in self.inputs:
            if _input["type"] == "InputText":
                self.input_elems.append(KEntry(self, _input["label"]))

            elif _input["type"] == "OptionMenu":
                self.input_elems.append(KOptionMenu(self, _input["label"], values=_input["validValues"]))

            elif _input["type"] == "ComboBox":
                self.input_elems.append(KMenu(self, _input["label"], values=_input["validValues"]))

        for but, cmd in (["Erstellen", self.confirm], ["Abbrechen", self.close_popup]):
            self.buttons.append(CTkButton(self, text=but, command=cmd,
                                          text_font=(Theme.wow_font2, Theme.fontfactor*18)))

        self.grid_widgets()

    def grid_widgets(self) -> None:
        for index, input_elem in enumerate(self.input_elems):
            input_elem.grid(row=index, column=0, columnspan=len(self.buttons), sticky="NSEW")
            self.grid_rowconfigure(index, weight=1)

        for index, but in enumerate(self.buttons):
            but.grid(row=len(self.input_elems), column=index,
                     padx=(0, 10 if index+1 != len(self.buttons) else 0), sticky="NSEW")
            self.grid_columnconfigure(index, weight=1)

    def open_popup(self) -> None:
        self.deiconify()

    def close_popup(self) -> None:
        self.withdraw()

    def confirm(self) -> None:
        self.close_popup()
        values = [input_elem.get() for input_elem in self.input_elems]
        self.confirm_call(*values)


"""
- Freier Text
- OptionMenu

Char:
- Char
- Realm

ToDo:
- Name
- Typ
- Difficulty

"""





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
