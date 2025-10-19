import json
from pathlib import Path
from typing import List, Dict, Any
from src.schema.item import Clothing
from src.schema.item_config import Condition, ClothSize, Gender

import torch
from torch.utils.data import Dataset, DataLoader


class VintedDataset(Dataset):
    def __init__(self, dataset_path: str):
        super().__init__()

        self.dataset_path = Path(dataset_path)

    def load_metadata_files(self) -> List[Clothing]:
        """Load all metadata.json files from the dataset directory."""
        items = []
        for metadata_file in self.dataset_path.glob("**/metadata.json"):
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
