"""
gui/instances/instance_headers.py

Project: WoW-Dashboard-Client
Created: 19.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from tkinter import Event

from gui.widgets import KTableHeader, KTable, KImage, KPopUp
from data import WeeklySettings, InstanceManager
from style import Theme, ImageManager


##################################################
#                     Code                       #
##################################################

class InstanceRowHeader(KTableHeader):
    """
    InstanceTable rowheader
    """

    def __init__(
            self,
            master: KTable,
            name: str,
            label: str,
            index: int,
            header_index: int,
            *_args: any,
            **_kwargs: any):
        """
        Create InstanceTable rowheader
        :param master: Master table passed by KTable
        :param name: Rowname passed by KTable
        """

        super().__init__(
            master,
            name,
            label.split(","),
            index,
            header_index,
            "row",
            image=KImage(InstanceManager[name]["image"])
            if InstanceManager[name]["image"] and header_index == 0 else None,
            move_callback=InstanceManager.move_row,
            context_menu=[
                {
                    "label": "Alle Aktivieren (ACHTUNG)", "command":
                    lambda n=name: InstanceManager.activate_whole(n)
                },
                {
                    "label": "Alle Deaktivieren (ACHTUNG)", "command":
                    lambda n=name: InstanceManager.deactivate_whole(n)
                },
                {
                    "label": "Löschen (ACHTUNG)", "command":
                    lambda n=name: InstanceManager.delete_whole(n)
                }
            ],
            edit_menu=KPopUp(master, "Instanz bearbeiten",
                             [
                                 {
                                     "type": "InputText",
                                     "label": "Name"
                                 }
                             ],
                             confirm_call=self.edit) if header_index == 0 else None,
            fg_color=Theme.background3,
            text_color=Theme.text_color,
            text_font=(Theme.wow_font, Theme.fontfactor * 18),
            move_fg_color=Theme.background2,
            move_text_color=Theme.text_color,
            move_text_font=(Theme.wow_font, Theme.fontfactor * 25),
            movemark_color=Theme.done_color,
            movemark_width=20
        )

        if self.header_index == 0:
            self.bind("<Button-2>", self.open_popup)

    def open_popup(self, _event: Event) -> None:
        self.edit_menu.open_popup()
        self.edit_menu.set_values(self.name)

    def edit(self, name: str) -> None:
        if name != self.name and self.header_index == 0:
            InstanceManager.values[name] = InstanceManager.values[self.name]
            del InstanceManager.values[self.name]
            self.master.rename_row(self.name, name)

            self.name = name
            self.master.row_headerwidgets[self.name][1].name = name

            if self.typ == "row":
                self.master.row_headerwidgets[self.name][0].set_labels([self.name])
            InstanceManager.reload_observable.trigger("reload")


class InstanceColHeader(KTableHeader):
    """
    InstanceTable columnheader
    """

    def __init__(
            self,
            master: KTable,
            name: str,
            label: str,
            index: int,
            header_index: int,
            *_args: any,
            **_kwargs: any):
        """
        Create InstanceTable columnheader
        :param master: Master table passed by KTable
        :param name: Columname passed by KTable
        """

        img = ImageManager.get_race_image(WeeklySettings["chars"][name]["race"])

        super().__init__(
            master,
            name,
            [label],
            index,
            header_index,
            "column",
            move_callback=WeeklySettings.move_col,
            context_menu=[
                {
                    "label": "Alle Aktivieren (ACHTUNG)", "command":
                    lambda n=name: WeeklySettings.activate_whole(n)
                },
                {
                    "label": "Alle Deaktivieren (ACHTUNG)", "command":
                    lambda n=name: WeeklySettings.deactivate_whole(n)
                },
                {
                    "label": "Löschen (ACHTUNG)", "command":
                    lambda n=name: WeeklySettings.delete_whole(n)
                }
            ],
            image=KImage(img) if img else None,
            fg_color=Theme.background3,
            text_color=Theme.text_color,
            text_font=(Theme.wow_font, Theme.fontfactor * 18),
            move_fg_color=Theme.background2,
            move_text_color=Theme.text_color,
            move_text_font=(Theme.wow_font, Theme.fontfactor * 25),
            movemark_color=Theme.done_color,
            movemark_width=20
        )
