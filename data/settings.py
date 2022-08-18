"""
gui/instances/instanceData.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date, timedelta
from typing import TextIO, Callable
from dataclasses import dataclass
from os import listdir

import pyglet
import json


##################################################
#                     Code                       #
##################################################

class _SettingsManager:
    __today: list
    __values: dict
    __path: str
    __default: dict[str, str]
    path: str
    reset_callback: Callable[[dict], dict] | None

    def __init__(self, path: str | None = "data/instance_data/", reset_callback: Callable[[dict], dict] | None = None) -> None:
        self.reset_callback = reset_callback
        self.path = path

        self.__today = list(
            (date.today() +
             timedelta(
                days=5,
                hours=15)).isocalendar())
        self.__values = {}

        pathsplit = self.path.split(".")
        with open(f"{path}default.json", "r") as default:
            self.default = json.loads(default.read())
        print("DEFAULT", self.default)

    def __getitem__(self, item: str) -> str:
        try:
            return self.values[item]
        except KeyError:
            print("KEY")
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

    @property
    def values(self) -> dict:
        self.read()
        return self.__values

    def read(self) -> None:
        for index in range(2):
            try:
                with open(f"{self.path}{self.__today[1]}_{self.__today[0]}.json", "r") as data:
                    self.__values = json.loads(data.read())
                    break

            except (FileNotFoundError, json.decoder.JSONDecodeError):
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
                            print(last)
                            if self.reset_callback:
                                last = self.reset_callback(last)
                            data.write(json.dumps(last, indent=4))
                    else:
                        self._reset(data)
                        print("RESET", self.default)

    def write(self) -> None:
        with open(f"{self.path}{self.__today[1]}_{self.__today[0]}.json", "w+") as data:
            data.write(json.dumps(self.__values, indent=2))


def reset_instances(instances: dict) -> dict:
    for instance in instances:
        for diff in instances[instance]["difficulty"]:
            for char in instances[instance]["difficulty"][diff]["chars"]:
                instances[instance]["difficulty"][diff]["chars"][char]["done"] = None
    return instances


InstanceManager = _SettingsManager(reset_callback=reset_instances)
Settings = _SettingsManager(path="data/settings/")
