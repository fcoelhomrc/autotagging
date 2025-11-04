from ollama import generate
from ollama import GenerateResponse
from pydantic import BaseModel
import json
import base64
from rich import print
from enum import Enum


system_prompt = """
Your job is to fill out information about new product listings at second-hand online marketplaces.
You will receive a list with images of the product, and your task is to fill out the provided JSON template with the necessary information.
Here is a short description of each field:

  summary: str - A brief description of the images
  category: str - Which type of clothing
  size: int - Clothing size in EU number system
  brand: str - Clothing brand
  status: str - Wear signs?
  color: List[str] - List of all dominant colors

"""


class Color(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    BEIGE = "beige"
    CREAM = "cream"
    BROWN = "brown"
    YELLOW = "yellow"
    WHITE = "white"


# def post_processing(output):
#     if not output.brand_is_visible:
#         output.brand = None


class ProductDescription(BaseModel):
    summary: str
    category: str
    size: int

    brand_is_visible: bool
    brand: str

    status: str
    color: list[Color]
    # gender: str


def encode_images_to_base64(img_paths):
    encoded_images = []
    for path in img_paths:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            encoded_images.append(encoded)
    return encoded_images


image_paths = [
    "/home/felipe/Datasets/VINTED_DATASET_V1/1367673551/images/1630429595.webp?s=4d7f1c50736da261cc52c7e9e2fdbcae0b3f2740.jpg",
    "/home/felipe/Datasets/VINTED_DATASET_V1/1367673551/images/1630429595.webp?s=7c56237cac152ef7a574f4a1c0ba335f499c336a.jpg",
    "/home/felipe/Datasets/VINTED_DATASET_V1/1367673551/images/1630429595.webp?s=ad8b7b0c38973130e69b6f1756064153150b2817.jpg",
    "/home/felipe/Datasets/VINTED_DATASET_V1/1367673551/images/1630429595.webp?s=e0dd60951f0f6326f2c2c37bc365a276c95c5791.jpg",
    "/home/felipe/Datasets/VINTED_DATASET_V1/1367673551/images/1688060904.webp?s=56b8000acfe93ebd71429996d86d78727413e041.jpg",
]

images = encode_images_to_base64(image_paths)

ground_truth_path = "/home/felipe/Datasets/VINTED_DATASET_V1/1367673551/metadata.json"

with open(ground_truth_path, "r") as file:
    ground_truth = json.load(file)

model = "gemma3"
response: GenerateResponse = generate(
    model=model,
    system=system_prompt,
    prompt=ground_truth.get("description", ""),
    images=images,
    format=ProductDescription.model_json_schema(),
    stream=False,
    options={"temperature": 0},
)

print(f"Ground Truth: {ground_truth}")
print(f"Prediction: {response.response}")
