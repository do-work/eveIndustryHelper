from typing import List

from eveAPI import EveAPI
from services.itemLookup import ItemLookup


class Restock:

    def __init__(self, eve_api: EveAPI, item_lookup: ItemLookup):
        self.item_lookup = item_lookup
        self.eve_api = eve_api

    # todo -> make restock_items into a namedTuple
    def run(self, stock_items: List[dict]) -> List[dict]:
        # todo -> cache this
        stock_items = self.item_lookup.add_item_id(stock_items)
        character_id = self.eve_api.get_character_id()
        corp_id = self.eve_api.get_corp_id(character_id)
        corp_assets = self.get_corp_assets_by_location(corp_id, 1030093382162)
        corp_assets_consolidated = self.consolidate_duplicate_assets(corp_assets)
        stock_items_id = [int(stock_item["id"]) for stock_item in stock_items]
        current_stock = self.filter_assets(corp_assets_consolidated, stock_items_id)
        results = self.restock_qty(stock_items, current_stock)

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

    def get_corp_asset_location_ids(self, assets) -> List[int]:
        """
        Get asset's unique location_ids.
        :param assets:
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

    def consolidate_duplicate_assets(self, assets: List[dict]):
        results = []
        for asset in assets:
            found_duplicate = False
            for result in results:
                if result.get("type_id") == asset.get("type_id"):
                    current_qty = result.get("quantity")
                    result["quantity"] = current_qty + asset.get("quantity")
                    found_duplicate = True
                    break
            if not found_duplicate:
                results.append(asset)
                continue
        return results

    def filter_assets(self, assets: List[dict], items_id: List[int]) -> List[dict]:
        results = []
        for item_id in items_id:
            for asset in assets:
                if asset.get("type_id") == item_id:
                    results.append(asset)

        return results

    def restock_qty(self, stock_items: List[dict], current_stock: List[dict]) -> List[dict]:
        restock = []
        for stock_item in stock_items:
            stock_item_min = stock_item.get("min")
            stock_item_max = stock_item.get("max")
            for current_stock_item in current_stock:
                if current_stock_item.get("type_id") != stock_item.get("id"):
                    continue
                current_stock_qty = current_stock_item.get("quantity")
                if current_stock_qty < stock_item_min:
                    restock_qty = stock_item_max - current_stock_qty
                    restock.append({
                        "name": stock_item.get("item_name"),
                        "id": stock_item.get("id"),
                        "restock_qty": restock_qty
                    })
        return restock

    def format_for_clipboard(self, restock_results: List[dict]) -> str:
        results = ''
        for restock_result in restock_results:
            results += f"{restock_result['name']} {restock_result['restock_qty']}\n"
        return results
