import csv
import pathlib
from pathlib import Path
from typing import List


class ItemLookup:

    def __init__(self, config: dict):
        self.parsed_file = None
        self.config = config

    def get_invtypes_path(self, filename) -> Path:
        return pathlib.Path(self.config['PROJECT_ROOT']).joinpath("static", filename)

    def parse_file(self, filepath):
        if self.parsed_file:
            return self.parsed_file
        with open(filepath) as file:
            reader = csv.DictReader(file)
            self.parsed_file = list(reader)
        return self.parsed_file

    def add_item_id(self, items: List[dict]) -> List[dict]:
        items_info = self.parse_file(self.get_invtypes_path(Path("invTypes.csv")))
        for item in items:
            found = False
            for item_info in items_info:
                if item_info.get("typeName") == item.get("item_name"):
                    found = True
                    item["id"] = int(item_info.get("typeID"))
                    break
            if not found:
                raise KeyError(f"item_name:'{item}' not found in item info master file.")

        return items
