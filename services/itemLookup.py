import csv
import pathlib
from os import PathLike
from pathlib import Path

from settings import PROJECT_ROOT


class ItemLookup:

    def get_invtypes_path(self, filename: str) -> Path:
        return pathlib.Path(PROJECT_ROOT).joinpath("static", filename)

    def parse_file(self, filepath: PathLike):
        with open(filepath) as file:
            reader = csv.DictReader(file)
            return list(reader)
