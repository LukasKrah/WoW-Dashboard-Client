"""
style/imageManager.py

Project: WoW-Dashboard-Client
Created: 18.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from json import loads


##################################################
#                     Code                       #
##################################################

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
