"""
styles/theme.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from dataclasses import dataclass
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


@dataclass(frozen=True)
class _DarkTheme:
    background0: str = "#888888"
    background1: str = "#555555"
    background2: str = "#333333"
    background3: str = "#222222"

    text_color_light: str = "#FFFFFF"
    text_color: str = "#CCCCCC"
    text_color_reverse: str = background3

    primary_light: str = "#253DA1"
    primary_middle: str = "#02057A"
    primary_dark: str = "#000137"

    positive_color: str = "#00FF00"
    positve_text: str = "#00CC00"
    negative_color: str = "#FF0000"
    negative_text: str = "#CC0000"

    fontfactor: float = 1
    font: str = "Arial"
    wow_font: str = "LifeCraft"


pyglet.font.add_file("style/LifeCraft_Font.ttf")
Theme = _DarkTheme()
