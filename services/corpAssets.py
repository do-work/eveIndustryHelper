from typing import Set

from eveAPI import EveAPI
from services.itemLookup import ItemLookup


class CorpAssets:

    def __init__(self, eve_api: EveAPI, item_lookup: ItemLookup):
        self.item_lookup = item_lookup
        self.eve_api = eve_api

    def get_corp_assets(self, corp_id: int):
        return self.eve_api.get_corp_assets(corp_id)

    def get_location_ids_for_all_corp_assets(self, corp_id: int) -> Set:
        corp_assets_results = self.get_corp_assets(corp_id)
        location_ids = set()
        for corp_asset_result in corp_assets_results:
            location_ids.add(corp_asset_result.get("location_id"))
        return location_ids

    def get_items_location_ids_from_assets(self, assets, item_id) -> Set:
        """
        Get the locations for a specific item.

        The item_id is actually referred to as a type_id.
        :param assets:
        :param item_id:
        :return:
        """
        location_results = set()
        for asset in assets:
            if asset.get("type_id") == item_id:
                location_results.add(asset.get("location_id"))

        return location_results
