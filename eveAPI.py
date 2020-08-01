import requests

from controllers.oauth import Oauth


class EveAPI:

    ESI_BASE = "https://esi.evetech.net"

    def __init__(self, oauth: Oauth, config: dict):
        self.auth = oauth
        self.config = config
        self.header = None
        self.token = None

    def _get_token(self):
        # todo -> validate the refresh token
        if not self.token:
            self.token = self.auth.get_refreshed_access_token()
        return self.token

    def _get_header(self):
        if not self.header:
            self.header = {"authorization": f"Bearer {self._get_token()}"}
        return self.header

    def make_request(self, method: str, endpoint: str, base_url=ESI_BASE, params: dict = None):
        full_url = f"{base_url}{endpoint}"

        method = method.lower()
        if method == 'get':
            return requests.get(full_url, headers=self._get_header(), params=params)

    def get_character_id(self):
        url = "/oauth/verify"
        response = self.make_request("get", url, base_url=self.config['LOGIN_SERVER_BASE']).json()
        return response.get("CharacterID")

    def get_corp_id(self, character_id: str):
        url = f"/v4/characters/{character_id}"
        return self.make_request("get", url).json().get("corporation_id")

    def get_corp_assets(self, corp_id: int):
        url = f"/v5/corporations/{corp_id}/assets"
        res = self.make_request("get", url)
        pages = int(res.headers["x-pages"])

        corp_assets = res.json()
        if pages == 1:
            return corp_assets
        for page in range(2, pages + 1):
            page_results = self.make_request("get", url, params={"page": page}).json()
            for page_result in page_results:
                corp_assets.append(page_result)

        # todo -> combine duplicates if the item was not stacked - use logic at Restock.consolidate_duplicate_assets

        return corp_assets

    def get_station_info(self, station_id: int):
        url = f"/v2/universe/stations/{station_id}"
        return self.make_request("get", url).json()

    def get_corp_contracts(self, corp_id: int):
        url = f"/v1/corporations/{corp_id}/contracts/"
        response = self.make_request("get", url)
        return response.json()
