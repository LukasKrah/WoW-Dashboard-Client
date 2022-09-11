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
    race_configfilename: str
    valid_extenstions: list[str]

    images: list
    races: list

    def __init__(
            self,
            path: str | None = "style/images/",
            configfilename: str | None = "images.json",
            race_configfilename: str | None = "races/races.json",
            valid_extenstions=None) -> None:
        if valid_extenstions is None:
            valid_extenstions = []

        self.path = path
        self.configfilename = configfilename
        self.valid_extenstions = valid_extenstions
        self.race_configfilename = race_configfilename

        with open(self.path + self.configfilename, "r") as config:
            self.images = loads(config.read())

        with open(self.path + self.race_configfilename, "r") as race_config:
            self.races = loads(race_config.read())

    def __search_image(self, query: str, _list: list | None = ..., strict: bool | None = False) -> int | None:
        _list = self.images if _list is ... else _list

        for index, image in enumerate(_list):
            if strict:
                for keyword in image["keywords"]:
                    if keyword.lower() == query.lower():
                        return index
            else:
                if query.lower() in ",".join(image["keywords"]):
                    return index

        if not strict:
            for index, image in enumerate(_list):
                for keyword in image["keywords"]:
                    if keyword in query.lower():
                        return index
        return None

    def get_image(self, query: str) -> str | None:
        index = self.__search_image(query)
        if index is not None:
            return f'{self.path}{self.images[index]["path"]}'
        return None

    def get_race_image(self, query: str) -> str | None:
        index = self.__search_image(query, self.races, True)
        if index is not None:
            return f'{self.path}races/{self.races[index]["path"]}'
        return None


ImageManager = _ImageManager()
