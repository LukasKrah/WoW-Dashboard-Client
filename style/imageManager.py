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


##################################################
#                     Code                       #
##################################################

class KImage:
    img: Image.open
    imgTk: ImageTk.PhotoImage

    def __init__(self, path: str):
        img = Image.open(path)
        self.img = img
        self.imgTk = ImageTk.PhotoImage(self.img)

    def resize(self, width: int, height: int,
               mode: Literal["fitx", "normal"] | None = "normal") -> None:
        x, y = 0, 0
        img_width, img_height = self.img.size
        match mode:
            case "fitx":
                # img_width = 20
                # img_height = 30
                # width = 10
                # 10/20
                # x = 10
                # y = 15
                fact = width / img_width
                x = width
                y = img_height * fact
            case "normal":
                x, y = width, height
        self.imgTk = ImageTk.PhotoImage(self.img.resize(size=(int(x), int(y))))


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
            if query.lower() in ",".join(image["keywords"]):
                return index

        for index, image in enumerate(self.images):
            for keyword in image["keywords"]:
                if keyword in query.lower():
                    return index

        return None

    def get_image(self, query: str) -> str | None:
        index = self.__search_image(query)
        if index is not None:
            return f'{self.path}{self.images[index]["path"]}'
        return None


ImageManager = _ImageManager()
