"""
gui/instances.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from customtkinter import *
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

from gui.widgets import Table, NavBar, ContextMenu
from style import Theme

from .instanceData import InstanceManager

##################################################
#                 Menu classes                   #
##################################################


class InstanceRowHeader(CTkCanvas):
    width: int
    height: int
    text: str
    image: Image

    def __init__(self, master: Table, text: str, image: str, *args: any, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.width, self.height = 0, 0
        self.text = text
        if image:
            self.image = Image.open(image)
        else:
            self.image = None

        self.configure(bd=5, highlightthickness=0, background=Theme.background3)
        self.bind("<Configure>", self.__resize)

    def _reload(self) -> None:
        self.delete("all")
        # 100, 100
        # 200,
        if self.image:
            fact = self.width / self.image.size[0]
            img = ImageTk.PhotoImage(self.image.resize((int(self.width), int(self.image.size[1]*fact))))
            self.create_image(self.width/2, self.height/2, image=img)
            self.photo = img

        self.create_text(self.width/2, self.height/2, text=self.text, anchor="center",
                         font=Theme.wow_font, fill="white")

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self._reload()


class InstanceCell(CTkCanvas):
    width: int
    height: int
    click_x: int
    click_y: int
    __state: str
    con: ContextMenu
    column: str
    row: str

    def __init__(self, master: Table, col: str, row: str, *args: any, **kwargs: any) -> None:
        super().__init__(master, *args, **kwargs)
        self.width, self.height = 0, 0
        self.click_x, self.click_y = 0, 0
        self.column, self.row = col, row
        self.con = ContextMenu(self, [{"label": "Aktivieren", "command": self.toggle}])

        self.__state = "disable"
        if self.column in self.master.values[self.row]["chars"]:
            self.con.change_label(0, "Deaktivieren")
            match self.master.values[self.row]["chars"][self.column]["done"]:
                case True:
                    self.__state = "done"
                case False:
                    self.__state = "cancel"
                case None:
                    self.__state = "neutral"
            self._reload()

        self.configure(bd=5, highlightthickness=0, background=Theme.background3)
        self.bind("<Configure>", self.__resize)
        self.bind("<Button-1>", self.__click)
        self.bind("<Button-3>", self.con.popup)

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str) -> None:
        self.__state = value
        self._reload()

    def toggle(self) -> None:
        if self.__state == "disable":
            self.__state = "neutral"
            self.master.values[self.row]["chars"][self.column] = {"done": None}
            self.con.change_label(0, "Deaktivieren")
        else:
            self.__state = "disable"
            del self.master.values[self.row]["chars"][self.column]
            self.con.change_label(0, "Aktivieren")
        self._reload()
        InstanceManager.write()

    def _reload(self) -> None:
        self.delete("all")
        eval(f"self._{self.__state}()")

    def __resize(self, event: Event) -> None:
        self.width, self.height = event.width, event.height
        self._reload()

    def __click(self, event) -> None:
        self.click_x, self.click_y = event.x, event.y
        eval(f"self._{self.__state}_click()")
        InstanceManager.write()

    def _disable_click(self) -> None:
        ...

    def _disable(self) -> None:
        self.create_rectangle(0, 0, self.width, self.height, fill="#555555")
        self.create_text(self.width/2, self.height/2, text="-", font=(Theme.font, Theme.fontfactor*18))

    def _neutral_click(self) -> None:
        if self.click_x < self.width/2:
            self.__state = "done"
            self.master.values[self.row]["chars"][self.column] = {"done": True}
        else:
            self.__state = "cancel"
            self.master.values[self.row]["chars"][self.column] = {"done": False}
        self._reload()

    def _neutral(self) -> None:
        self.create_rectangle(0, 0, self.width/2, self.height, fill="#00ff00")
        self.create_rectangle(self.width/2, 0, self.width, self.height, fill="#ff0000")

        self.create_text(self.width/4, self.height/2, text="✓", anchor="center",
                         font=(Theme.font, Theme.fontfactor*18))
        self.create_text(self.width/4*3, self.height/2, text="❌", anchor="center",
                         font=(Theme.font, Theme.fontfactor*18))

    def _done_click(self) -> None:
        if messagebox.askyesno("Zurücksetzen", "Sicher das du dieses Feld zurücksetzen willst?"):
            self.__state = "neutral"
            self._reload()

    def _done(self) -> None:
        self.create_rectangle(0, 0, self.width, self.height, fill="#00ff00")

        self.create_text(self.width/2, self.height/2, text="Erledigt!", anchor="center",
                         font=(Theme.font, Theme.fontfactor*18))

    def _cancel_click(self) -> None:
        if messagebox.askyesno("Zurücksetzen", "Sicher das du dieses Feld zurücksetzen willst?"):
            self.__state = "neutral"
            self._reload()

    def _cancel(self) -> None:
        self.create_rectangle(0, 0, self.width, self.height, fill="#ff0000")

        self.create_text(self.width / 2, self.height / 2, text="Machs gefällig\ndu KEK!",
                         anchor="center", font=(Theme.font, Theme.fontfactor*18), justify="center")


class InstanceTable(CTkCanvas):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        self.configure(bd=0, highlightthickness=0, background=Theme.background3)

        self.table = Table(self, cells=InstanceCell, rowheader=InstanceRowHeader, colheader=InstanceRowHeader)
        self.table.values = InstanceManager.values
        self.table.reload()
        self.navBar = NavBar(self)

        self.grid_widgets()

    def grid_widgets(self) -> None:
        self.table.grid(row=0, column=0, sticky="NSEW")
        self.navBar.grid(row=1, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



