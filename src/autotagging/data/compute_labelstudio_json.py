from pathlib import Path
import json
import IPython


if __name__ == "__main__":
    dataset_path = Path("./dataset_bak")
    assert dataset_path.exists(), f"Dataset path {dataset_path} does not exist."

    labelstudio_json = []
    prefix_labelstudio_file = "/data/local-files/?d=" # Mandatory prefix for local files to be detected in Label Studio
    for sample in dataset_path.iterdir():
        if sample.is_file():
            continue

        metadata_path = sample / "metadata.json"
        print(f"{metadata_path} doesn't exist") if not metadata_path.exists() else None

        with open(metadata_path, "r") as f:
            metadata = json.load(f)

            description = metadata.get("description", "")
            title = metadata.get("title", "")
        
        sample_json = {"data": {}}
        sample_json["data"]["title"] = title
        sample_json["data"]["description"] = description
        sample_json["data"]["images"] = ["dataset/" + str(Path(*img.parts[1:-1])) + "/" + img.stem + ".jpg" for img in sample.rglob("*.jpg")]

        labelstudio_json.append(sample_json)

    output_path = dataset_path / "labelstudio.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(labelstudio_json, f, ensure_ascii=False, indent=2, default=str)
    print(f"Saved {len(labelstudio_json)} entries to {output_path}")