# shop/models/item.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from pathlib import Path

from src.schema.item_config import *


@dataclass
class Item:
    """
    Represents an item in your shop.
    """

    #id: str = field(default_factory=lambda: str(uuid4())) #TODO: Should we use it? I leave it for now
    title: str = ""
    description: str = ""
    price: float = 0.0
    images: List[Path] = field(default_factory=list)

    def __repr__(self):
        return f"<Item {self.title!r} ({self.brand}) - {self.condition}>"



@dataclass
class Clothing(Item):
    brand: str
    condition: Condition
    size: Optional[ClothSize] = None
    material: Optional[str] = None
    gender: Gender = None

