import json
from pathlib import Path
from typing import List, Dict, Any

from vinted_scraper.models import VintedItem
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader
import IPython
from box import Box

# Our scripts
from schema.item import Item


class VintedLoader(DataLoader):
    """DataLoader wrapper for VintedDataset."""

    def __init__(
        self,
        root: Path,
        batch_size: int = 32,
        shuffle: bool = True,
        num_workers: int = 0,
        category: str = None,
    ):
        self.dataset = VintedDataset(root=root, category=category)

        super().__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
        )


class VintedDataset(Dataset):
    def __init__(self, root: Path, category: str = None, compute_class_sets: bool = False):
        super().__init__()
        # Dataset directory
        self.root = Path(root)
        assert self.root.exists(), f"Dataset directory {root} does not exist."

        self.items = self.fetch_available_items(category=category)
        self.remove_none_items()

        if compute_class_sets:
            self._compute_class_sets()
    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]

    def fetch_available_items(self, category: str = None) -> List[Item]:
        """Fetch available items from the dataset directory."""
        items_paths = self.root.glob("*")

        items = []
        for path in items_paths:
            full_path = path / "metadata.json"
            j = self.load_json(full_path)

            if category is None or j.category == category:
                items.append(self.init_item(j, path))
        return items

    def remove_none_items(self):
        dataset_size_before = len(self.items)
        self.items = [item for item in self.items if item is not None]
        
        print(f"Removed {dataset_size_before - len(self.items)} items from the dataset due to category not found.")

    @staticmethod
    def load_json(file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return Box(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading JSON file {file_path}: {str(e)}")
            return {}

    @staticmethod
    def init_item(json_data: Dict[str, Any], path: Path):
        items_map = {
            "clothing": Clothing,
        }

        category = json_data.category.split('/')[0]
        item_obj = items_map.get(category, None)
        return item_obj(**json_data, path=path) if item_obj is not None else None

    def load_metadata_files(self) -> List[Clothing]:
        """Load all metadata.json files from the dataset directory."""
        items = []
        for metadata_file in self.root.glob("*/metadata.json"):
            item = self._process_metadata_file(metadata_file)
            if item:
                items.append(item)
        return items

    def _process_metadata_file(self, file_path: Path) -> Clothing:
        """Process a single metadata.json file and convert it to a Clothing object."""
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            return Clothing(
                title=data.get("type", ""),
                brand=data.get("brand", ""),
                condition=Condition.USED,  # Default value as per schema
                size=ClothSize(data.get("size")) if "size" in data else None,
                gender=Gender(data.get("gender")) if "gender" in data else None,
                images=[file_path.parent / img for img in data.get("images", [])],
            )
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return None

    def _compute_class_sets(self) -> Dict[str, List[str]]:
        """Get unique class sets for categorical attributes."""
        
        class_sets = {
            "category": set(),
            "status": set(),
            "color": set(),
            "size": set(),
        }

        for item in self.items:
            class_sets["category"].add(item.category)

            if isinstance(item, Clothing):
                class_sets["status"].add(item.status)
                for color in item.color:
                    class_sets["color"].add(color)
                if item.size:
                    class_sets["size"].add(item.size.name)

class ComputeDatasetStats:
    """Compute dataset statistics such as number of items per category."""

    def __init__(self, dataset: VintedDataset):
        self.dataset = dataset

        # TODO: fds depois melhor isto
        print(self.compute_category_distribution("brand"))
        print(self.compute_category_distribution("color"))
        print(self.compute_category_distribution("status"))
        print(self.compute_category_distribution("size"))
        print(self.compute_category_distribution("gender"))
        print(self.compute_category_distribution("material"))

    def compute_category_distribution(self, category) -> Dict[str, int]:
        print(f"Computing distribution for category: {category}")
        counts = {"nan": 0}
        for sample in self.dataset:
            value = sample[category]

            if value is None:
                counts["nan"] += 1
                continue

            elif category == "color" or category == "material":
                items = value.split(", ")

                for idx_item in items:
                    if idx_item not in counts.keys():
                        counts[idx_item] = 0
                    counts[idx_item] += 1
                    
            else:
                if value not in counts.keys() and value is not None:
                    counts[value] = 0

                counts[value if value is not None else "nan"] += 1
        return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)) # return dict ordered by values

if __name__ == "__main__":
    dataset = VintedDataset(Path("dataset_auto/"))
    print(len(dataset))
    for item in iter(dataset):
        print(item)
