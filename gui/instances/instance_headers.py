"""
gui/instances/instance_headers.py

Project: WoW-Dashboard-Client
Created: 19.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from gui.widgets import KTableHeader, KTable, KImage
from data import WeeklySettings, InstanceManager
from style import Theme


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
            image=KImage(InstanceManager[name]["image"]) if InstanceManager[name]["image"] and header_index == 0 else None,
            move_callback=InstanceManager.move_row,
            context_menu=[{"label": "Alle Aktivieren (ACHTUNG)", "command": WeeklySettings.activate_whole},
                          {"label": "Alle Deaktivieren (ACHTUNG)", "command": WeeklySettings.deactivate_whole},
                          {"label": "Löschen (ACHTUNG)", "command": WeeklySettings.delete_whole}],
            fg_color=Theme.background3,
            text_color=Theme.text_color,
            text_font=(Theme.wow_font, Theme.fontfactor*18),
            move_fg_color=Theme.background2,
            move_text_color=Theme.text_color,
            move_text_font=(Theme.wow_font, Theme.fontfactor*25),
            movemark_color=Theme.done_color,
            movemark_width=20
        )


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
        super().__init__(
            master,
            name,
            label.split(":")[:-1],
            index,
            header_index,
            "column",
            move_callback=WeeklySettings.move_col,
            context_menu=[{"label": "Alle Aktivieren (ACHTUNG)", "command": WeeklySettings.activate_whole},
                          {"label": "Alle Deaktivieren (ACHTUNG)", "command": WeeklySettings.deactivate_whole},
                          {"label": "Löschen (ACHTUNG)", "command": WeeklySettings.delete_whole}],
            fg_color=Theme.background3,
            text_color=Theme.text_color,
            text_font=(Theme.wow_font, Theme.fontfactor*18),
            move_fg_color=Theme.background2,
            move_text_color=Theme.text_color,
            move_text_font=(Theme.wow_font, Theme.fontfactor*25),
            movemark_color=Theme.done_color,
            movemark_width=20
        )
