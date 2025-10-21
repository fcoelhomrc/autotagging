from ollama import chat, generate
from ollama import ChatResponse, GenerateResponse
from pydantic import BaseModel
import json
import base64
from rich import print


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
    "dataset_mini/sample0001/images/1760113128.webp",
    "dataset_mini/sample0001/images/1760113128-2.webp",
    "dataset_mini/sample0001/images/1760113128-3.webp",
    "dataset_mini/sample0001/images/1760113128-4.webp",
    "dataset_mini/sample0001/images/1760113128-5.webp",
    "dataset_mini/sample0001/images/1760113128-6.webp",
    "dataset_mini/sample0001/images/1760113128-7.webp",
    "dataset_mini/sample0001/images/1760113128-8.webp",
]

images = encode_images_to_base64(image_paths)

ground_truth_path = "dataset_mini/sample0001/metadata.json"

with open(ground_truth_path, "r") as file:
    ground_truth = json.load(file)

model = "gemma3"
response: GenerateResponse = generate(
    model=model,
    prompt=system_prompt,
    images=images,
    format=ProductDescription.model_json_schema(),
    stream=False,
    options={"temperature": 0},
)

print(f"Ground Truth: {ground_truth}")
print(f"Prediction: {response.response}")
