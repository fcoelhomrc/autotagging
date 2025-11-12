from ollama import generate
from ollama import GenerateResponse
from pydantic import BaseModel
import json
import base64
from rich import print
from enum import StrEnum, auto
import time 


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
  gender: str - Is it male, female, or unisex clothing? 

"""


class Color(StrEnum):
    blue = auto()
    red  = auto()
    cream = auto()
    beige = auto()
    white = auto() 

class Status(StrEnum):
    new_with_tags = auto()
    new_without_tags = auto()
    very_good = auto()
    good = auto()
    satisfactory = auto()


class Gender(StrEnum):
    male = auto()
    female = auto()
    unisex = auto()


class Category(StrEnum):
    coat = auto()
    skirt = auto()
    tshirt = auto()
    scarf = auto()
    pants = auto()


class ClassificationOutput(BaseModel):
    category: Category = Field(
        description="The type of clothing item."
    )
    status: Status = Field(
        description="The condition of the item: satisfactory, good, very good, new without tags, new with tags."
    )
    gender: Gender = Field(
        description="The target gender: male, female, or unisex."
    )
    color: List[Color] = Field(
        description="One or more colors present on the item."
    )

#
# def post_processing(output):
#     if not output.brand_is_visible:
#         output.brand = None


class ProductDescription(BaseModel):
    summary: str
    category: str
    size: int
    brand: str
    status: str
    color: list[str]
    gender: str


def encode_images_to_base64(img_paths):
    encoded_images = []
    for path in img_paths:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            encoded_images.append(encoded)
    return encoded_images


image_paths = [
    "dataset_auto/7416537936/images/1761519527.webp?s=0ff11b3b427eef3f803bae50e7e4f5acc0af57a5.jpg",
    "dataset_auto/7416537936/images/1761519527.webp?s=2637a1cb98f4266d799cb51f4ae958a5f9d77ec7.jpg",
    "dataset_auto/7416537936/images/1761519527.webp?s=c42ba871d6010c94df28c00d9dfa3985509ce6d8.jpg",
]

images = encode_images_to_base64(image_paths)

ground_truth_path = "dataset_auto/7416537936/metadata.json"

with open(ground_truth_path, "r") as file:
    ground_truth = json.load(file)

start_time = time.time()
model = "gemma3"
response: GenerateResponse = generate(
    model=model,
    system=system_prompt,
    prompt="my prompt",
    images=images,
    format=ProductDescription.model_json_schema(),
    stream=False,
    options={"temperature": 0},
)
print(f"Execution time: {time.time() - start_time:.2f}s\n")
print(f"Ground Truth: {ground_truth}")
print(f"Prediction: {response.response}")
