from eveAPI import EveAPI


class Restock:

    def __init__(self, eve_api: EveAPI):
        self.eve_api = eve_api

    def run(self):
        character_id = self.eve_api.get_character_id()
        corp_id = self.eve_api.get_corp_id(character_id)
        corp_asset_location_ids = self.get_corp_asset_location_ids(corp_id)

        return corp_asset_location_ids

    def get_corp_asset_location_ids(self, corp_id: int):
        corp_assets_results = self.eve_api.get_corp_assets(corp_id)

        location_ids = set()
        for corp_asset_result in corp_assets_results:
            location_id = corp_asset_result.get("location_id")
            if location_id not in location_ids:
                location_ids.add(location_id)
        return location_ids

    def get_location_name(self, location_id: int):
        pass
