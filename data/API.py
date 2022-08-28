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

    def get_token_history(self) -> int:
        return self.request(
            "/data/wow/token/index",
            f'dynamic-{Settings["myAccount"]["region"]}').json()["price"]

    def request(self, path: str, namespace: str | None = None) -> Response:
        if namespace is None:
            namespace = Settings["myAccount"]["namespace"]

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
