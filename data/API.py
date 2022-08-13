"""
data/API.py

Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from requests import Response
import requests
import json

from .settings import Settings


##################################################
#                     Code                       #
##################################################

# {'access_token': 'USXjGZhVfgRXy63Jk9XIhNA6ZyTAgy1wQU', 'token_type': 'bearer', 'expires_in': 86399, 'sub': 'f34246c0c509489e8231d340185a0920'} # noqa
class _API:
    token: dict

    def __init__(self) -> None:
        self.token = {}
        self.auth()

    def getTokenPrice(self) -> int:
        return self.request("/data/wow/token/index", f'dynamic-{Settings["myAccount"]["region"]}').json()["price"]

    def request(self, path: str, namespace: str | None = None) -> Response:
        if namespace is None:
            namespace = Settings["myAccount"]["namespace"]

        path = path.replace("{realmSlug}", Settings["myAccount"]["realmSlug"].lower())
        path = path.replace("{characterName}", Settings["myAccount"]["characterName"].lower())
        return requests.get(f'https://{Settings["myAccount"]["region"]}.api.blizzard.com{path}'
                            f'?namespace={namespace}'
                            f'&locale={Settings["myAccount"]["locale"]}'
                            f'&access_token={self.token["access_token"]}')

    def auth(self) -> None:
        auth_req = requests.post(url=Settings["API"]["URL"],
                                 data=Settings["API"]["data"],
                                 auth=("f34246c0c509489e8231d340185a0920","ZKvfQllQPILTgOzoVrAQabx0DiQTN5DJ"))
        self.token = auth_req.json()


API = _API()
