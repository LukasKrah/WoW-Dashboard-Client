"""
style/imageManager.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from concurrent.futures import ThreadPoolExecutor
from typing import Literal

from PIL import Image, ImageTk
from json import loads


##################################################
#                     Code                       #
##################################################

class KImage:
    img: Image.open
    imgTk: ImageTk.PhotoImage

    thread: ThreadPoolExecutor

    def __init__(self, path: str):
        img = Image.open(path)
        self.img = img
        self.imgTk = ImageTk.PhotoImage(self.img)

        self.thread = ThreadPoolExecutor(max_workers=1)

    def resize(self,
               width: int,
               height: int,
               mode: Literal["cover",
                             "fitx",
                             "normal"] | None = "normal") -> None:
        x, y = 0, 0
        img_width, img_height = self.img.size

        match mode:
            case "cover" | "contain":
                factx = width / img_width
                facty = height / img_height

                if mode == "contain":
                    fact = min(factx, facty)
                else:
                    fact = max(factx, facty)

                x = int(img_width * fact)
                y = int(img_height * fact)

            case "fitx":
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
