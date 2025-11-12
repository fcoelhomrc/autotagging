from pathlib import Path
import sys
import importlib
from typing import Optional
import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import IPython
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


def main():
    dataset = init_dataset(root=Path("dataset_auto/"))

    for sample in dataset:
        IPython.embed()
        time.sleep(0.2)
    


if __name__ == "__main__":
    main()

