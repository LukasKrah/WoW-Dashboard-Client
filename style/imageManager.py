"""
style/imageManager.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################
from typing import Literal

from PIL import Image, ImageTk
from json import loads
from os import listdir


##################################################
#                     Code                       #
##################################################

class KImage(ImageTk.PhotoImage):
    img: Image.open

    def __init__(self, img: Image.open):
        super().__init__(img)
        self.img = img

    def resize(self, width: int, height: int,
               mode: Literal["fitx", "normal"] | None = "normal") -> None:
        x, y = 0, 0
        match mode:
            case "fitx":
                fact = width / self.img.size[0]
                x = width
                y = height * fact
            case "normal":
                x, y = width, height
        super().__init__(self.img, (x, y))


class _ImageManager:
    path: str
    configfilename: str
    valid_extenstions: list[str]

    images: list

    def __init__(
            self,
            path: str | None = "style/images/",
            configfilename: str | None = "images.json",
            valid_extenstions=None) -> None:
        if valid_extenstions is None:
            valid_extenstions = []
        self.path = path
        self.configfilename = configfilename
        self.valid_extenstions = valid_extenstions
        with open(self.path + self.configfilename, "r") as config:
            self.images = loads(config.read())

    def __search_image(self, query: str) -> int | None:
        for index, image in enumerate(self.images):
            if query.lower() in image["keywords"]:
                return index
        return None

    def get_image(self, query: str) -> KImage | None:
        index = self.__search_image(query)
        if index:
            return KImage(
                Image.open(f'{self.path}{self.images[index]["path"]}'))
        return None


ImageManager = _ImageManager()
