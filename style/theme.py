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
    background1: str = "#555555"
    background2: str = "#333333"
    background3: str = "#111111"

    fontfactor: float = 1
    font: str = "Arial"
    wow_font: str = "LifeCraft"


pyglet.font.add_file("style/LifeCraft_Font.ttf")
Theme = _DarkTheme()
