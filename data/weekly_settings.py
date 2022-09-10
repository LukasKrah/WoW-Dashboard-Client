"""
data/weekly_settings.py

Project: WoW-Dashboard-Client
Created: 13.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date, timedelta
from typing import TextIO, Callable
from observable import Observable
from json import dumps, loads
from os import listdir

from debug import Debugger


##################################################
#                     Code                       #
##################################################

class _WeeklySettingsManager:
    __today: list

    values: dict
    default: dict[str, str]
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
            self.default = loads(default.read())

        self.read()

    def __getitem__(self, item: str) -> dict:
        try:
            return self.values[item]
        except KeyError:
            self.values[item] = self.default[item]
            return self.values[item]

    def __setitem__(self, key: str, value: str):
        self.values[key] = value
        self.write()

    def _reset(self, week: TextIO):
        week.write(dumps(self.default, indent=2))

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
                    self.values = loads(data.read())
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
                            last = loads(lastdata.read())
                            if self.reset_callback:
                                last = self.reset_callback(last)
                            data.write(dumps(last, indent=4))
                    else:
                        self._reset(data)

    def write(self) -> None:
        with open(f"{self.path}{self.__today[1]}_{self.__today[0]}.json", "w+") as data:
            data.write(dumps(self.values, indent=2))


class _InstanceManager(_WeeklySettingsManager, Debugger):
    reload_observable: Observable

    def __init__(self):
        _WeeklySettingsManager.__init__(
            self, reset_callback=self.reset_instances)
        self.reload_observable = Observable()

    def __set_states(self, name: str, value: bool | str | None):
        for diff in self.values[name]["difficulty"]:
            if value == "del":
                self.values[name]["difficulty"][diff]["chars"] = {}
            else:
                for char in WeeklySettings["chars"]:
                    if char not in self.values[name]["difficulty"][diff]["chars"]:
                        self.values[name]["difficulty"][diff]["chars"]["char"] = {
                            "done": value}
        self.reload_observable.trigger("reload")

    def activate_whole(self, name: str) -> None:
        self.__set_states(name, None)

    def deactivate_whole(self, name: str) -> None:
        self.__set_states(name, "del")

    def delete_whole(self, name: str) -> None:
        self.values[name]["active"] = False
        for instance in self.values:
            if "row" in self.values[instance]:
                if self.values[instance]["row"] > self.values[name]["row"]:
                    self.values[instance]["row"] -= 1
        del self.values[name]["row"]
        self.reload_observable.trigger("reload")

    def move_row(self, name: str, cur_index: int, new_index: int) -> None:
        self.debug("ROW", name, new_index)
        if new_index != InstanceManager.values[name]["row"]:
            for instance in InstanceManager.values:
                if instance != name and InstanceManager.values[instance]["active"]:
                    if cur_index < InstanceManager.values[instance]["row"] < new_index + 1:
                        InstanceManager.values[instance]["row"] -= 1
                    elif cur_index >= InstanceManager.values[instance]["row"] >= new_index:
                        InstanceManager.values[instance]["row"] += 1
            InstanceManager.values[name]["row"] = new_index

    @staticmethod
    def reset_instances(instances: dict) -> dict:
        del_instances: list = []
        for instance in instances:
            if instances[instance]["active"]:
                for diff in instances[instance]["difficulty"]:
                    del_chars: list = []
                    for char in instances[instance]["difficulty"][diff]["chars"]:
                        instances[instance]["difficulty"][diff]["chars"][char]["done"] = None
                        if char not in WeeklySettings.values["chars"]:
                            del_chars.append(char)
                    for del_char in del_chars:
                        del instances[instance]["difficulty"][diff]["chars"][del_char]
            else:
                del_instances.append(instance)

        for del_instance in del_instances:
            del instances[del_instance]

        return instances


class _WeeklySettings(_WeeklySettingsManager, Debugger):
    reload_observable: Observable

    def __init__(self):
        _WeeklySettingsManager.__init__(
            self,
            path="data/weekly_settings/",
            reset_callback=self.reset_settings)
        self.reload_observable = Observable()

    def __set_states(self, name: str, value: str | bool | None) -> None:  # noqa
        for instance in InstanceManager.values:
            for diff in InstanceManager[instance]["difficulty"]:
                if name in InstanceManager[instance]["difficulty"][diff]["chars"]:
                    if value == "del":
                        del InstanceManager.values[instance]["difficulty"][diff]["chars"][name]
                else:
                    if value != "del":
                        InstanceManager.values[instance]["difficulty"][diff]["chars"][name] = {
                            "done": value}
        self.reload_observable.trigger("reload")

    def activate_whole(self, name: str) -> None:
        self.__set_states(name, None)

    def deactivate_whole(self, name: str) -> None:
        self.__set_states(name, "del")

    def delete_whole(self, name: str) -> None:
        self.values["chars"][name]["active"] = False
        for char in self.values["chars"]:
            if "column" in self.values["chars"][char]:
                if self.values["chars"][char]["column"] > self.values["chars"][name]["column"]:
                    self.values["chars"][char]["column"] -= 1
        del self.values["chars"][name]["column"]

        self.reload_observable.trigger("reload")

    def move_col(self, name: str, cur_index: int, new_index: int) -> None:
        self.debug("COL", name, new_index)
        if new_index != WeeklySettings["chars"][name]["column"]:
            for user in WeeklySettings.values["chars"]:
                if user != name and WeeklySettings.values["chars"][user]["active"]:
                    if cur_index < WeeklySettings.values["chars"][user]["column"] < new_index + 1:
                        WeeklySettings.values["chars"][user]["column"] -= 1
                    elif cur_index >= WeeklySettings.values["chars"][user]["column"] >= new_index:
                        WeeklySettings.values["chars"][user]["column"] += 1
            WeeklySettings.values["chars"][name]["column"] = new_index

    @staticmethod
    def reset_settings(settings: dict) -> dict:
        del_chars: list = []
        for char in settings["chars"]:
            if not settings["chars"][char]["active"]:
                del_chars.append(char)

        for del_char in del_chars:
            del settings["chars"][del_char]

        return settings


WeeklySettings: _WeeklySettings
InstanceManager: _InstanceManager

WeeklySettings = _WeeklySettings()
InstanceManager = _InstanceManager()
