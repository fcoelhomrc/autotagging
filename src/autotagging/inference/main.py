# main.py

import json
from pipeline.document import ItemDocument
from pipeline.runner import InferencePipeline

from stages.ner_stage import NERStage
from stages.detection_stage import DetectionStage
from stages.ocr_stage import OCRStage
from stages.fusion_stage import FusionStage
from stages.categorization_stage import CategorizationStage

from validators.output_validator import validate_output
from config import CONFIG


def main(input_data):
    """
    Run inference pipeline on a single item.

    input_data: dict with keys:
        - title: str
        - description: str
        - images: list of image paths or PIL Images
    """
    # 1. Build the document
    doc = ItemDocument(
        title=input_data["title"],
        description=input_data["description"],
        images=input_data["images"]
    )

    # 2. Build the pipeline
    stages = [
        NERStage(),
        DetectionStage(),
        OCRStage(),
        FusionStage(),
        CategorizationStage()
    ]
    pipeline = InferencePipeline(stages=stages)

    # 3. Run the pipeline
    doc = pipeline.run(doc)

    # 4. Validate output
    valid, errors = validate_output(doc.final_json)
    if not valid:
        raise ValueError(f"Pipeline output failed schema validation:\n{errors}")

    # 5. Return clean JSON
    return doc.final_json


if __name__ == "__main__":
    # Example usage
    sample_input = {
        "title": "Men's Black Hoodie",
        "description": "A warm black hoodie with front pocket, size L",
        "images": ["./images/hoodie_1.jpg", "./images/hoodie_2.jpg"]
    }

    result = main(sample_input)
    print(json.dumps(result, indent=2))
