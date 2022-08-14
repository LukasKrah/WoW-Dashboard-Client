"""
data/settings.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from dataclasses import dataclass
import pyglet
import json


##################################################
#                     Code                       #
##################################################

class _Settings:
    settings: dict[str, str]
    default: dict[str, str]
    path: str

    def __init__(self, path: str | None = "data/settings.json") -> None:
        self.path = path
        self.settings = {}
        self.default = {}
        pathsplit = self.path.split(".")
        with open(f"{''.join(pathsplit[:-1])}_default.{pathsplit[-1]}", "r") as default:
            self.default = json.loads(default.read())

        self.__read()

    def __getitem__(self, item: str) -> str:
        try:
            return self.settings[item]
        except KeyError:
            print("KEY")
            self.settings[item] = self.default[item]
            return self.settings[item]

    def __setitem__(self, key: str, value: str):
        self.settings[key] = value
        self.__write()

    def _reset(self):
        with open(self.path, "w") as data:
            data.write(json.dumps(self.default, indent=2))

    def __write(self):
        with open(self.path, "w") as data:
            data.write(json.dumps(self.settings, indent=2))

    def __read(self):
        for index in range(2):
            try:
                with open(self.path, "r") as data:
                    self.settings = json.loads(data.read())
                    break
            except json.decoder.JSONDecodeError:
                self._reset()


Settings = _Settings()


@dataclass(frozen=True)
class _Theme:
    background1: str = "#555555"
    background2: str = "#333333"
    background3: str = "#111111"

    font: str = "Arial 18"
    wow_font: str = "WoW-plexus 18"


pyglet.font.add_file("style/WoW-plexus.ttf")
Theme = _Theme()
