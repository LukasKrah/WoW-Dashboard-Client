"""
gui/instances/instanceData.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date, timedelta
from typing import TextIO, Callable
from os import listdir

import json


##################################################
#                     Code                       #
##################################################

class _SettingsManager:
    __today: list
    values: dict
    __path: str
    __default: dict[str, str]
    path: str
    reset_callback: Callable[[dict], dict] | None

    def __init__(self, path: str | None = "data/instance_data/",
                 reset_callback: Callable[[dict], dict] | None = None) -> None:
        self.reset_callback = reset_callback
        self.path = path

        self.__today = list(
            (date.today() +
             timedelta(
                days=5,
                hours=15)).isocalendar())
        self.values = {}

        with open(f"{path}default.json", "r") as default:
            self.default = json.loads(default.read())

        self.read()

    def __getitem__(self, item: str) -> str:
        try:
            return self.values[item]
        except KeyError:
            self.values[item] = self.default[item]
            return self.values[item]

    def __setitem__(self, key: str, value: str):
        self.values[key] = value
        self.write()

    def _reset(self, week: TextIO):
        week.write(json.dumps(self.default, indent=2))

    @property
    def today(self) -> list:
        return self.__today

    @today.setter
    def today(self, value: str | None) -> None:
        if value == "Diese Woche":
            self.__today = list(
                (date.today() +
                 timedelta(
                    days=5,
                    hours=15)).isocalendar())
        else:
            splitvalue = [int(splitter)
                          for splitter in value.rstrip(".json").split("_")]
            self.__today = list(
                date.fromisocalendar(
                    year=splitvalue[1],
                    week=splitvalue[0],
                    day=1).isocalendar())
        self.read()

    def read(self) -> None:
        for index in range(2):
            try:
                with open(f"{self.path}{self.__today[1]}_{self.__today[0]}.json", "r") as data:
                    self.values = json.loads(data.read())
                    break

            except FileNotFoundError:
                # Should try last week but not for now
                with open(f"{self.path}{self.__today[1]}_{self.__today[0]}.json", "w+") as data:
                    youngest: list = []
                    for file in listdir(self.path):
                        if file.endswith(".json") and "default" not in file \
                                and file != f"{self.__today[1]}_{self.__today[0]}.json":
                            splitfile = file.rstrip(".json").split("_")
                            age = int(f"{splitfile[1]}{splitfile[0]}")
                            try:
                                age_youngest = int(
                                    f"{youngest[1]}{youngest[0]}")
                                if age > age_youngest:
                                    youngest = splitfile
                            except IndexError:
                                youngest = splitfile

                    if youngest:
                        with open(f"{self.path}{youngest[0]}_{youngest[1]}.json", "r") as lastdata:
                            last = json.loads(lastdata.read())
                            if self.reset_callback:
                                last = self.reset_callback(last)
                            data.write(json.dumps(last, indent=4))
                    else:
                        self._reset(data)

    def write(self) -> None:
        with open(f"{self.path}{self.__today[1]}_{self.__today[0]}.json", "w+") as data:
            data.write(json.dumps(self.values, indent=2))


def reset_instances(instances: dict) -> dict:
    del_instances: list = []
    for instance in instances:
        if instances[instance]["active"]:
            for diff in instances[instance]["difficulty"]:
                del_chars: list = []
                for char in instances[instance]["difficulty"][diff]["chars"]:
                    instances[instance]["difficulty"][diff]["chars"][char]["done"] = None
                    if char not in Settings.values["chars"]:
                        del_chars.append(char)
                for del_char in del_chars:
                    del instances[instance]["difficulty"][diff]["chars"][del_char]
        else:
            del_instances.append(instance)

    for del_instance in del_instances:
        del instances[del_instance]

    return instances


def reset_settings(settings: dict) -> dict:
    del_chars: list = []
    for char in settings["chars"]:
        if not settings["chars"][char]["active"]:
            del_chars.append(char)

    for del_char in del_chars:
        del settings["chars"][del_char]

    return settings


Settings = _SettingsManager(path="data/settings/", reset_callback=reset_settings)
InstanceManager = _SettingsManager(reset_callback=reset_instances)
