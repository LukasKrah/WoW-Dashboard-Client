"""
gui/widgets/k_image.py

Project: WoW-Dashboard-Client
Created: 30.08.2022
Author: Lukas Krahbichler
"""


##################################################
#                    Imports                     #
##################################################

from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageTk, ImageEnhance
from typing import Literal


##################################################
#                     Code                       #
##################################################

class KImage:
    prepare_grey_out: bool
    grey_out_alpha: float

    img: Image.open
    imgTk: ImageTk.PhotoImage

    enhancer: ImageEnhance.Brightness
    imgTk_greyout: ImageTk.PhotoImage

    thread: ThreadPoolExecutor

    def __init__(self, path: str, prepare_grey_out: bool | None = True, grey_out_alpha: float | None = 0.2):
        self.prepare_grey_out = prepare_grey_out
        self.grey_out_alpha = grey_out_alpha

        img = Image.open(path)
        self.img = img
        self.imgTk = ImageTk.PhotoImage(self.img)

        if self.prepare_grey_out:
            self.enhancer = ImageEnhance.Brightness(self.img)
            self.imgTk_greyout = ImageTk.PhotoImage(self.enhancer.enhance(self.grey_out_alpha))

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
        if self.prepare_grey_out:
            self.enhancer = ImageEnhance.Brightness(
                self.img.resize(size=(int(x), int(y))))
            self.imgTk_greyout = ImageTk.PhotoImage(self.enhancer.enhance(self.grey_out_alpha))
