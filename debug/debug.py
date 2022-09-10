"""
debug/debug.py

Project: WoW-Dashboard-Client
Created: 30.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################


##################################################
#                     Code                       #
##################################################

class Debugger:
    debug_prints: bool = False

    def debug(self, *args: any) -> None:
        if self.debug_prints:
            print(self.__class__.__name__, "|", self, "|", *args)
