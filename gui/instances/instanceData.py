"""
gui/instances/instanceData.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date, timedelta
from os import listdir
import json


##################################################
#                     Code                       #
##################################################

class _InstanceManager:
    __today: list
    __values: dict
    __path: str

    def __init__(self) -> None:
        self.__today = list(
            (date.today() +
             timedelta(
                days=5,
                hours=15)).isocalendar())
        self.__values = {}

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
                with open(f"data/instance_data/{self.__today[1]}_{self.__today[0]}.json", "r") as data:
                    self.__values = json.loads(data.read())
                    break

            except FileNotFoundError:
                # Should try last week but not for now
                with open(f"data/instance_data/{self.__today[1]}_{self.__today[0]}.json", "w+") as data:
                    youngest: list = []
                    for file in listdir("data/instance_data"):
                        if file.endswith(".json"):
                            splitfile = file.rstrip(".json").split("_")
                            age = int(f"{splitfile[1]}{splitfile[0]}")
                            try:
                                age_youngest = int(
                                    f"{youngest[1]}{youngest[0]}")
                                if age < age_youngest:
                                    youngest = splitfile
                            except IndexError:
                                youngest = splitfile

                    print("YOUNG:", youngest)
                    if youngest:
                        with open(f"data/instance_data/{youngest[0]}_{youngest[1]}.json", "r") as lastdata:
                            last = json.loads(lastdata.read())
                            print(last)
                            for instance in last:
                                for diff in last[instance]["difficulty"]:
                                    for char in last[instance]["difficulty"][diff]["chars"]:
                                        last[instance]["difficulty"][diff]["chars"][char]["done"] = None
                            print(last)
                            data.write(json.dumps(last, indent=4))

                    else:
                        data.write(json.dumps({}))

    def write(self) -> None:
        with open(f"data/instance_data/{self.__today[1]}_{self.__today[0]}.json", "w+") as data:
            data.write(json.dumps(self.__values, indent=4))


InstanceManager = _InstanceManager()
