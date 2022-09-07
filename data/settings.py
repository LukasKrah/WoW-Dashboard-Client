"""
data/settings.py

Project: WoW-Dashboard-Client
Created: 30.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from json import dumps, loads

from debug import Debugger

##################################################
#                     Code                       #
##################################################


class _Settings(Debugger):
    path: str
    file: str
    default_file: str

    __default_values: dict
    __values: dict

    def __init__(
            self,
            path: str | None = "data/settings",
            file: str | None = "settings.json",
            default_file: str | None = "default.json"):
        """

        :param path:
        :param file:
        :param default_file:
        """
        self.path = path + ("/" if path[-1] != "/" else "")
        self.file = file
        self.default_file = default_file

        self.__values = {}

        self._get_default()
        self.read()

    @property
    def values(self) -> dict:
        return self.__values

    def __setitem__(self, key, value) -> None:
        self.write()
        self.__values[key] = value

    def __getitem__(self, item) -> dict:
        self.write()
        return self.__values[item]

    def _get_default(self) -> None:
        with open(f"{self.path}default.json", "r") as data:
            self.__default_values = loads(data.read())

    def read(self) -> None:
        for index in range(2):
            try:
                with open(f"{self.path}{self.file}", "r") as data:
                    self.__values = loads(data.read())
                break
            except FileNotFoundError:
                with open(f"{self.path}{self.file}", "w") as data:
                    data.write(dumps(self.__default_values, indent=4))

    def write(self) -> None:
        with open(f"{self.path}{self.file}", "w") as data:
            data.write(dumps(self.__values, indent=4))


Settings = _Settings()
