"""
styles/theme.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from json import loads
import pyglet


##################################################
#                     Code                       #
##################################################

class FontFactor:
    value: float

    def __init__(self, value: float | None = 0) -> None:
        self.value = value

    def __mul__(self, other: int) -> int:
        return int(other * self.value)


class _Theme:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path

        self.read()

    def read(self) -> None:
        with open(self.path, "r") as data:
            readdata = loads(data.read())
            for value in readdata:
                if isinstance(readdata[value], int):
                    self.__dict__[value] = FontFactor(readdata[value])
                else:
                    self.__dict__[value] = readdata[value]


pyglet.font.add_file("style/LifeCraft_Font.ttf")
Theme = _Theme("style/themes/dark_theme.json")
