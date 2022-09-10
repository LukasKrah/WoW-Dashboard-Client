"""
data/droplist_settings.py

Project: WoW-Dashboard-Client
Created: 07.09.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from .settings import _Settings


##################################################
#                     Code                       #
##################################################

class _SettingsWithMove(_Settings):
    move_key: str

    def __init__(self, path: str, move_key: str):
        self.move_key = move_key

        super().__init__(path)

    def move(self, name: str, cur_index: int, new_index: int) -> None:
        if cur_index != new_index:
            for elem in self.values:
                if elem != name:
                    if cur_index < self.values[elem][self.move_key] < new_index + 1:
                        self.values[elem][self.move_key] -= 1
                    elif cur_index >= self.values[elem][self.move_key] >= new_index:
                        self.values[elem][self.move_key] += 1
            self.values[name][self.move_key] = new_index


DroplistSettings = _SettingsWithMove("data/droplist", "row")
DroplistColumns = _SettingsWithMove("data/droplist_columns", "column")
