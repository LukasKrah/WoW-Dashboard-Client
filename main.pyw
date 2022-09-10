"""
/main.py
Runs the GUI of the WoW-Dashboard without console

Project: WoW-Dashboard-Client
Created: 12.08.2022
Author: Lukas Krahbichler
"""

from version import VersionChanger

if __name__ == "__main__":
    VersionChanger.auto_update("0_2_0")

    from gui import Window

    Window().mainloop()
