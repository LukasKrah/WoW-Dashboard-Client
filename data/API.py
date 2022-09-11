"""
data/API.py

Project: WoW-Dashboard-Client
Created: 13.08.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from requests import Response
from typing import Literal
import requests

from .settings import Settings


##################################################
#                     Code                       #
##################################################

class _API:
    token: dict

    def __init__(self) -> None:
        self.token = {}
        self.auth()

    def get_all_mounts(self) -> dict:
        return self.request(
            "/data/wow/mount/index",
            "static"
        ).json()["mounts"]

    def get_mount(self, mount_id: int) -> dict:
        return self.request(f"/data/wow/mount/{mount_id}",
                            namespace="static").json()

    def get_create_display_media(self, creature_display_id) -> dict:
        return self.request(
            f"/data/wow/media/creature-display/{creature_display_id}",
            namespace="static").json()["assets"]["value"]

    def get_char_race(self, realm_slug: str, character_name: str) -> str | None:
        try:
            return self.request(f"/profile/wow/character/{realm_slug}/{character_name}/appearance",
                                namespace="profile"
                                ).json()["playable_race"]["name"]
        except KeyError:
            return ""

    def get_token_history(self) -> int:
        return self.request(
            "/data/wow/token/index",
            "dynamic").json()["price"]

    def request(self,
                path: str,
                namespace: Literal["profile",
                                   "dynamic",
                                   "static"]) -> Response:
        namespace = f'{namespace}-{Settings["myAccount"]["region"]}'

        path = path.replace(
            "{realmSlug}",
            Settings["myAccount"]["realmSlug"].lower())
        path = path.replace("{characterName}",
                            Settings["myAccount"]["characterName"].lower())
        return requests.get(
            f'https://{Settings["myAccount"]["region"]}.api.blizzard.com{path}'
            f'?namespace={namespace}'
            f'&locale={Settings["myAccount"]["locale"]}'
            f'&access_token={self.token["access_token"]}')

    def auth(self) -> None:
        auth_req = requests.post(
            url=Settings["API"]["URL"],
            data=Settings["API"]["data"],
            auth=(
                "f34246c0c509489e8231d340185a0920",
                "ZKvfQllQPILTgOzoVrAQabx0DiQTN5DJ"))
        self.token = auth_req.json()


API = _API()
