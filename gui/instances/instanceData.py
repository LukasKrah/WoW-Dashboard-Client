"""
gui/instances/instanceData.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from datetime import date
import json


##################################################
#                     Code                       #
##################################################

class _InstanceManager:
    today: list
    __values: dict

    def __init__(self) -> None:
        self.today = []
        self.__values = {}

    @property
    def values(self) -> dict:
        self.read()
        return self.__values

    def read(self) -> None:
        self.today = list(date.today().isocalendar())
        for index in range(2):
            try:
                with open(f"data/instance/{self.today[1]}_{self.today[0]}.json", "r") as data:
                    self.__values = json.loads(data.read())
                    break

            except FileNotFoundError:
                # Should try last week but not for now
                with open(f"data/instance/{self.today[1]}_{self.today[0]}.json", "w+") as data:
                    data.write(json.dumps({}))

    def write(self) -> None:
        with open(f"data/instance/{self.today[1]}_{self.today[0]}.json", "w+") as data:
            data.write(json.dumps(self.__values, indent=4))


InstanceManager = _InstanceManager()
