from item_config import Enum

class Category(Enum):
    Clothes = "clothes"

class Condition(Enum):
    NEW_TAGS = "new_with_tags"
    NEW_WO_TAGS = "new_without_tags"
    VERY_GOOD = "very good"
    GOOD = "good"
    SATISFACTORY = "satisfactory"

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"

class ClothSize(Enum):
    XXXS = "XXXS"
    XXS = "XXS"
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXXL"
    XXXXL = "4XL"
    XXXXXL = "5XL"
    XXXXXXL = "6XL"
    XXXXXXXL = "7XL"
    XXXXXXXXL = "8XL"
    XXXXXXXXXL = "9XL"

class SizeSystem(Enum):
    EU = "EU"
    US = "US"
    UK = "UK"
    INTL = "INTL"

class SizeNormalizer:
    """Converts various size systems (EU/US/UK) to internal ClothSize."""

    _EU_MAP = {
        "30": ClothSize.XXXS,
        "32": ClothSize.XXS,
        "34": ClothSize.XXS,
        "36": ClothSize.XS,
        "38": ClothSize.S,
        "40": ClothSize.M,
        "42": ClothSize.L,
        "44": ClothSize.XL,
        "46": ClothSize.XXL,
        "48": ClothSize.XXXL,
        "50": ClothSize.XXXXL,
        "52": ClothSize.XXXXXL,
        "54": ClothSize.XXXXXXL,
        "56": ClothSize.XXXXXXXL,
        "58": ClothSize.XXXXXXXXL,
    }

    _US_MAP = {
        "00": ClothSize.XXXS,
        "0": ClothSize.XXS,
        "2": ClothSize.XS,
        "4": ClothSize.S,
        "6": ClothSize.M,
        "8": ClothSize.L,
        "10": ClothSize.XL,
        "12": ClothSize.XXL,
        "14": ClothSize.XXXL,
        "16": ClothSize.XXXXL,
        "18": ClothSize.XXXXXL,
        "20": ClothSize.XXXXXXL,
        "22": ClothSize.XXXXXXXL,
        "24": ClothSize.XXXXXXXXL,
        "26": ClothSize.XXXXXXXXXL
    }

    _UK_MAP = {
        "2": ClothSize.XXXS,
        "4": ClothSize.XXS,
        "6": ClothSize.XS,
        "8": ClothSize.S,
        "10": ClothSize.M,
        "12": ClothSize.L,
        "14": ClothSize.XL,
        "16": ClothSize.XXL,
        "18": ClothSize.XXXL,
        "20": ClothSize.XXXXL,
        "22": ClothSize.XXXXXL,
        "24": ClothSize.XXXXXXL,
        "26": ClothSize.XXXXXXXL,
        "28": ClothSize.XXXXXXXXL,
        "30": ClothSize.XXXXXXXXXL
    }

    def convert(self, size: str, system: SizeSystem) -> ClothSize:
        size_maps = {
            SizeSystem.EU: self._EU_MAP,
            SizeSystem.US: self._US_MAP,
            SizeSystem.UK: self._UK_MAP
        }

        if system not in size_maps:
            raise ValueError(f"Invalid size system: {system}")

        return size_maps[system][size]
