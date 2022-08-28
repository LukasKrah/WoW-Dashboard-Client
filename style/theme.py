"""
styles/theme.py

Project: WoW-Dashboard-Client
Created: 14.08.2022
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
    background0: str
    background1: str
    background2: str
    background3: str

    text_color_light: str
    text_color: str
    text_color_reverse: str

    primary_light: str
    primary_middle: str
    primary_dark: str

    done_color: str
    done_color_light: str
    done_text: str
    cancel_color: str
    cancel_color_light: str
    cancel_text: str

    positive_color: str
    positive_color_light: str
    positive_text: str
    negative_color: str
    negative_color_light: str
    negative_text: str

    fontfactor: FontFactor
    font: str
    wow_font: str

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
