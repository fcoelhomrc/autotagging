# shop/models/item.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from pathlib import Path

from schema.item_config import *


@dataclass(kw_only=True)
class Item:
    """
    Represents an item in your shop.
    """

    def __init__(
        self,
        id: int,
        path: Path,
        category: str = "",
        title: str = "",
        description: str = "",
        **kwargs,
    ):
        self.id = id
        self.path = path
        self.category = category
        self.title = title
        self.description = description
        self.images = self.fetch_available_images()

    def __repr__(self):
        return f"<Item {self.id}>"

    # def __post_init__(self):
    #     pass

    def fetch_available_images(self) -> List[Path]:
        return list((self.path / "images").rglob("*"))


@dataclass
class Clothing(Item):
    """
    Represents a clothing item with specific attributes for apparel.
    """

    brand: str
    status: Condition
    color: List[str] = field(default_factory=list)
    material: Optional[str] = None
    # gender: Gender = Gender.UNISEX

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Clothe({len(self.images)}): {self.id}>"
