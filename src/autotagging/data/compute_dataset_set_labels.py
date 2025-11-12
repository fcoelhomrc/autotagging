from pathlib import Path
import sys
import importlib
from typing import Optional, Dict, Set
import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import IPython
import json
import time

#!/usr/bin/env python3
"""
Initialize a dataset (from dataset_loader.py if available, otherwise fallback to torchvision.datasets.ImageFolder)
with root in "dataset_auto/" and iterate it with a DataLoader.

Save this file as:
 /home/leonardomf12/git-repos/autotagging/src/autotagging/data/compute_dataset_set_labels.py
"""

def init_dataset(root: Path):
    assert root.exists(), f"Dataset root {root} does not exist."
    from src.autotagging.dataset_loader import VintedDataset

    return VintedDataset(root=root)

def save_to_json(sets: Dict[str, Set]):
    output_path = Path(__file__).parent / "class_label_sets.json"
    data = {key: sorted(list(values)) for key, values in sets.items()}

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved labels to {output_path}")


def main():
    dataset = init_dataset(root=Path("dataset_auto/"))

    sets = {
        "category": set(),
        "brand": set(),
        "color": set(),
        "material": set(),
        "status": set(),
    }
    
    for sample in dataset:
        for attr in ["category", "brand", "color", "material", "status"]:
            value = getattr(sample, attr, "")
            if value is not None and value != "":
                value_clean = value.strip() if attr != "category" else value.strip().split('/')[2]
                sets[attr].add(value_clean)
    return save_to_json(sets)


if __name__ == "__main__":
    main()

