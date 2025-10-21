import json
from pathlib import Path
from typing import List, Dict, Any

from vinted_scraper.models import VintedItem

from src.schema.item import Clothing
from src.schema.item_config import Condition, ClothSize, Gender
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader
import IPython

# Our scripts
from src.schema.item import Item

class VintedDataset(Dataset):
    def __init__(self, root: Path, category: str = None):
        super().__init__()
        self.root = Path(root)
        self.category = category

        assert self.root.exists(), f"Dataset directory {root} does not exist."

        items = self.fetch_available_items()



    def fetch_available_items(self, category:str = None) -> List[Item]:
        """Fetch available items from the dataset directory."""
        items_paths = self.root.rglob("*")


        items = self.load_metadata_files()
        return items


    def load_metadata_files(self) -> List[Clothing]:
        """Load all metadata.json files from the dataset directory."""
        items = []
        for metadata_file in self.root.glob("**/metadata.json"):
            item = self._process_metadata_file(metadata_file)
            if item:
                items.append(item)
        return items

    def _process_metadata_file(self, file_path: Path) -> Clothing:
        """Process a single metadata.json file and convert it to a Clothing object."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            return Clothing(
                title=data.get('type', ''),
                brand=data.get('brand', ''),
                condition=Condition.USED,  # Default value as per schema
                size=ClothSize(data.get('size')) if 'size' in data else None,
                gender=Gender(data.get('gender')) if 'gender' in data else None,
                images=[file_path.parent / img for img in data.get('images', [])]
            )
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return None
