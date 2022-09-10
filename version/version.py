"""
data/version.py

Project: WoW-Dashboard-Client
Created: 10.09.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from os import makedirs, rename, listdir
from json import dumps, loads
from shutil import copytree
from typing import Callable


##################################################
#                     Code                       #
##################################################

DEFAULTS = {
    "settings": {
        "program": {
            "version": "0_2_0"},
        "API": {
            "URL": "https://us.battle.net/oauth/token",
            "data": {
                "grant_type": "client_credentials"},
            "auth": [
                "f34246c0c509489e8231d340185a0920",
                "ZKvfQllQPILTgOzoVrAQabx0DiQTN5DJ"]},
        "myAccount": {
            "region": "eu",
            "realmSlug": "alleria",
            "characterName": "",
            "locale": "de_DE"},
        "friends": {},
        "add_char": {
            "last_realm": "Alleria"},
        "add_todo": {
            "last_typ": "Daily"}},
    "droplist": {},
    "droplist_columns": {
        "mount": {
            "label": "Mount",
            "column": 0,
            "active": True},
        "date": {
            "label": "Datum",
            "column": 1,
            "active": True},
        "trys": {
            "label": "Versuche",
            "column": 2,
            "active": True}}}


class VersionChanger:
    path: str = "./data/"

    @staticmethod
    def backup_folders(version: str) -> None:
        makedirs(f"{VersionChanger.path}backup_{version}")
        for folder in listdir(VersionChanger.path):
            if "." not in folder and "backup" not in folder:
                copytree(
                    f"{VersionChanger.path}{folder}",
                    f"{VersionChanger.path}backup_{version}/{folder}_{version}")

    @staticmethod
    def in_all_json(path: str, callback: Callable) -> None:
        for json_file in listdir(path):
            if json_file.endswith(".json"):
                with open(f"{path}{json_file}", "r") as data:
                    modified = callback(loads(data.read()))

                with open(f"{path}{json_file}", "w") as data:
                    data.write(dumps(modified, indent=4))

    @staticmethod
    def create_folder(path: str, file: str, content: dict) -> None:
        makedirs(path)
        with open(f"{path}{file}", "w") as data:
            data.write(dumps(content, indent=4))

    @staticmethod
    def update_none() -> None:
        rename(f"{VersionChanger.path}settings",
               f"{VersionChanger.path}weekly_settings")

        def modify_weekly_settings(data: dict) -> dict:
            for key in ["API", "myAccount", "friends", "add_char", "add_todo"]:
                del data[key]
            return data

        def modify_version(data: dict) -> dict:
            data["program"]["version"] = "0_2_0"
            return data

        VersionChanger.in_all_json(
            f"{VersionChanger.path}weekly_settings/",
            modify_weekly_settings)

        VersionChanger.create_folder(
            f"{VersionChanger.path}settings/",
            "default.json",
            DEFAULTS["settings"])
        VersionChanger.create_folder(
            f"{VersionChanger.path}droplist/",
            "default.json",
            DEFAULTS["droplist"])
        VersionChanger.create_folder(
            f"{VersionChanger.path}droplist_columns/",
            "default.json",
            DEFAULTS["droplist_columns"])

        VersionChanger.in_all_json(
            f"{VersionChanger.path}settings/",
            modify_version)

    @staticmethod
    def auto_update(version: str) -> None:
        versions = ["none", "0_2_0"]
        try:
            with open(f"{VersionChanger.path}settings/settings.json") as settings:
                cur_version = loads(settings.read())["program"]["version"]
        except (KeyError, FileNotFoundError):
            cur_version = "none"
        old_index = versions.index(cur_version)
        new_index = versions.index(version)
        if old_index < new_index:
            VersionChanger.backup_folders(cur_version)

            while old_index < new_index:
                VersionChanger.__dict__[f"update_{versions[old_index]}"]()
                old_index += 1
