from pathlib import Path
import argparse
import IPython

# Folder to process
root_folder = Path("dataset_bak")

if __name__ == "__main__":
    for file in root_folder.rglob("*"):
        if file.is_file() and file.suffix.lower() == ".jpg":
            
            new_name = str(file.stem).split("?s=")[-1] + file.suffix
            file.rename(file.with_name(new_name))
            print(f"Renamed: {file} -> {file.with_name(new_name)}")#