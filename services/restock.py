from typing import List

from eveAPI import EveAPI


class Restock:

    def __init__(self, eve_api: EveAPI):
        self.eve_api = eve_api

    def run(self):
        character_id = self.eve_api.get_character_id()
        corp_id = self.eve_api.get_corp_id(character_id)
        # assets = self.eve_api.get_corp_assets(corp_id)

        # this one worked
        # results = self.find_item_in_assets(assets, 25619)

        # results = self.get_asset_location_flags(assets)

        # corp_asset_location_ids = self.get_corp_asset_location_ids(assets, corp_id)
        # results = self.get_location_info(corp_asset_location_ids)

        # noobs mat hanger - 1030093382162
        results = self.get_corp_assets_by_location(corp_id, 1030093382162)
        # results = self.filter_assets(assets, 25605)

        return results

    def find_item_in_assets(self, assets, type_id):
        found = []
        for asset in assets:
            if asset.get("type_id") == type_id:
                found.append(asset)

        return found

    def get_asset_location_flags(self, assets):
        found_location_flags = []
        found = False
        for asset in assets:
            asset_location_flag = asset.get("location_flag")
            for i, found_location_flag in enumerate(found_location_flags):
                if asset_location_flag == found_location_flag["name"]:
                    found_location_flags[i]["qty"] += 1
                    found = True
                    break
            if not found:
                found_location_flags.append({"name": asset_location_flag, "qty": 1})

        return found_location_flags

    def get_corp_asset_location_ids(self, assets, corp_id: int) -> List[int]:
        """
        Get asset's unique location_ids.
        :param corp_id:
        :return:
        """
        location_ids = set()
        for corp_asset_result in assets:
            location_id = corp_asset_result.get("location_id")
            if location_id not in location_ids:
                location_ids.add(int(location_id))
        return list(location_ids)

    def get_location_info(self, location_ids: List[int]):
        """
        Get the location id and name for stations only.
        location_id is the same for structure or station but info for each uses a different endpoint.
        :param location_ids:
        :return:
        """
        station_names = []
        for location_id in location_ids:
            location_id_length = len(str(location_id))

            if location_id_length == 8:
                location_info = self.eve_api.get_station_info(location_id)
                station_names.append({"id": location_id, "name": location_info["name"]})
            elif location_id_length > 8:
                continue
        return station_names

    def get_corp_assets_by_location(self, corp_id: int, location_id: int):
        """
        Get the corp assets at a specific location.
        Non singletons.
        :param corp_id:
        :param location_id:
        :return:
        """
        corp_assets_results = self.eve_api.get_corp_assets(corp_id)

        assets = []
        for corp_assets_result in corp_assets_results:
            if not corp_assets_result.get("location_id") == location_id:
                continue
            if not corp_assets_result.get("is_singleton"):
                assets.append(corp_assets_result)
        return assets

    def filter_assets(self, assets: List[dict], type_id: int):
        results = []
        for asset in assets:
            if asset.get("type_id") == type_id:
                results.append(asset)

        return results
