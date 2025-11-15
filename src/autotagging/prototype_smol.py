import IPython
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers.image_utils import load_image
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
from pathlib import Path
from typing import List, Dict

from pydantic import BaseModel
import json
import base64
from rich import print
from enum import StrEnum, auto
import time 
import argparse

# My scripts
from src.autotagging.dataset_loader import VintedDataset

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-s", "--sample", type=int, help='An integer sample ID')
    return parser.parse_args()

def get_system_prompt():
    return """
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


def smol_message_json(images: List[Image.Image], product_info: Dict[str, str]) -> List[Dict]:
    # Documentation: https://huggingface.co/learn/smol-course/unit1/2
    # Roles: system, user, assistant (and tool for function calling)


    return [
        {   
            "role": "system",
            "content": get_system_prompt()
        },
        {
            "role": "user",
            "content": [
                *[{"type": "image"} for _ in range(len(images))],
                {"type": "text", "Product Title": product_info["title"]},
                {"type": "text", "Product Description": product_info["description"]}
            ]
        },
    ]


if __name__ == "__main__":
    args = parse_arguments()

    # Sample
    sample = args.sample
    sample_path = Path(f"dataset_auto/{sample}")

    images = [Image.open(img_path) for img_path in Path(sample_path / "images").rglob("*.jpg")]
    metadata = VintedDataset.load_json(sample_path / "metadata.json")


    # SmolVLM Model(https://huggingface.co/blog/smolvlm)
    model_id = "HuggingFaceTB/SmolVLM-Base"
    processor = AutoProcessor.from_pretrained(model_id)

    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        dtype=torch.bfloat16,
        _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
    ).to(DEVICE)

    # Prompt
    messages = smol_message_json(images, metadata)
    prompt = processor.apply_chat_template(messages, add_generation_prompt=False) #add_generation_prompt only appends a "Assistant:" at the end
    print("Messages:", messages)
    print("Prompt:", prompt)

    # Inputs
    inputs = processor(text=prompt, images=images, return_tensors="pt").to(DEVICE)

    # Generate
    start = time.time()
    generated_ids = model.generate(**inputs, max_new_tokens=500)
    end = time.time()
    print(f"Generation took {end - start:.2f} seconds")
    print("Generated IDs:", generated_ids)
    generated_texts = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )
    print(f"Decoding Batch Took: {time.time() - end:.2f} seconds")
    print("Generated Texts:", generated_texts)