import logging
import os
from typing import Optional, List, Dict
from pathlib import Path
from time import sleep
import random

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

from vinted_scraper import VintedScraper
from vinted_scraper.models import VintedItem, VintedImage


DATASET_ROOT_DIR = "dataset_auto"
IMAGE_EXT = "jpg"  # TODO: check this
RATE_LIMIT_WAIT = 2  # seconds

logger = logging.getLogger(__name__)


def create_dir(item: VintedItem) -> Path:
    """
    Creates a directory entry for the item.
    """
    if item.id is None:
        raise ValueError("No Item ID found!")

    dir_name = Path(DATASET_ROOT_DIR) / str(item.id)
    dir_name.mkdir(exist_ok=True, parents=True)
    return dir_name


def query(search_text: str) -> List[VintedItem]:
    """
    Passes text query to Vinted and extracts information from search results page.
    """
    scraper = VintedScraper(
        "https://www.vinted.com"
    )  # init the scraper with the baseurl
    params = {
        "search_text": search_text
        # Add other query parameters like the pagination and so on
    }
    logger.info(f"Searching for {params['search_text']}")
    items = scraper.search(params)  # get all the items
    if len(items) < 1:
        logger.error(f"Query {params['search_text']} did not return any items")
    return items


def process_response(items: List[VintedItem]):
    """
    Extracts data from each item obtained from query.
    """
    for item in items:
        dir_name = create_dir(item)
        # Extract information
        soup = get_item_listing_from_vinted_item(item)
        metadata = get_metadata_from_vinted_item(item)

        metadata_from_listing = parse_metadata_from_listing(soup)
        image_urls = parse_image_urls_from_listing(item, soup)

        logger.info(f"Original metadata: {metadata}")
        logger.info(f"Extracted metadata: {metadata_from_listing}")

        # Merge dicts
        metadata.update(metadata_from_listing)
        logger.info(f"Merged metadata: {metadata}")

        # Write to file
        with open(dir_name / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        # Download images
        request_images(image_urls, dir_name)


def get_metadata_from_vinted_item(item: VintedItem) -> dict:
    """
    Extracts metadata from Vinted item.
    TODO: Missing data only available in listing page!
    """
    metadata = {
        "category": "clothing",
        "id": item.id,
        "url": item.url,
        "title": item.title,
        "description": item.description,
        "brand": None,
        "status": item.status,
        "size": item.size,
        "color": None,
        # TODO: no attribute gender is available!
    }

    try:
        json_string = json.dumps(metadata)
    except TypeError as e:
        logger.error("Cannot convert metadata to JSON format!")
        return
    return metadata


def headers():
    """
    Request headers to avoid being blocked as bot.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    return headers


def avoid_rate_limit():
    """
    Randomized wait time between requests.
    """
    sleep(random.uniform(0.75 * RATE_LIMIT_WAIT, 1.25 * RATE_LIMIT_WAIT))


def get_item_listing_from_vinted_item(item: VintedItem) -> BeautifulSoup:
    response = requests.get(item.url, headers=headers())
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_child_tag_from_class(
    parent_tag, tag_name: str, class_name: str | List[str]
) -> Optional[str]:
    match_ = parent_tag.find(tag_name, class_=class_name)
    return match_


def get_value_from_tag(tag):
    return tag.get_text(strip=True) if tag else None


def get_child_value_from_class(
    parent_tag, tag_name: str, class_name: str | List[str]
) -> Optional[str]:
    match_ = get_child_tag_from_class(parent_tag, tag_name, class_name)
    return get_value_from_tag(match_)


def get_child_value_from_itemprop(
    parent_tag, tag_name: str, itemprop: str
) -> Optional[str]:
    match_ = parent_tag.find(tag_name, itemprop=itemprop)
    return get_value_from_tag(match_)


def parse_metadata_from_listing(soup: BeautifulSoup) -> Dict[str, str]:

    # Metadata
    metadata = {}

    # Status
    status_tag = soup.find("div", itemprop="status")
    value = get_child_value_from_class(
        status_tag,
        tag_name="span",
        class_name=[
            "web_ui__Text__text",
            "web_ui__Text__subtitle",
            "web_ui__Text__left",
            "web_ui__Text__bold",
        ],
    )
    metadata["status"] = value

    # Size
    size_tag = soup.find("div", itemprop="size")
    value = get_child_value_from_class(
        size_tag,
        tag_name="span",
        class_name=[
            "web_ui__Text__text",
            "web_ui__Text__subtitle",
            "web_ui__Text__left",
            "web_ui__Text__bold",
        ],
    )
    metadata["size"] = value

    # Color
    color_tag = soup.find("div", class_="details-list__item-value", itemprop="color")
    value = get_child_value_from_class(
        color_tag,
        tag_name="span",
        class_name=[
            "web_ui__Text__text",
            "web_ui__Text__subtitle",
            "web_ui__Text__left",
            "web_ui__Text__bold",
        ],
    )
    metadata["color"] = value

    # Color
    color_tag = soup.find("div", class_="details-list__item-value", itemprop="color")
    value = get_child_value_from_class(
        color_tag,
        tag_name="span",
        class_name=[
            "web_ui__Text__text",
            "web_ui__Text__subtitle",
            "web_ui__Text__left",
            "web_ui__Text__bold",
        ],
    )
    metadata["color"] = value

    # Brand
    brand_tag = soup.find(
        "a", class_=["inverse", "u-disable-underline-without-hover"], itemprop="url"
    )
    value = get_child_value_from_itemprop(
        brand_tag,
        tag_name="span",
        itemprop="name",
    )
    metadata["brand"] = value

    # Description
    description_tag = soup.find("div", class_="u-text-wrap", itemprop="description")
    description_tag = get_child_tag_from_class(
        description_tag,
        tag_name="span",
        class_name=[
            "web_ui__Text__text",
            "web_ui__Text__body",
            "web_ui__Text__left",
            "web_ui__Text__format",
        ],
    )
    value = get_value_from_tag(description_tag.find("span"))
    metadata["description"] = value

    return metadata


def parse_image_urls_from_listing(item: VintedItem, soup: BeautifulSoup) -> List[str]:
    """
    Attempts to find all product photos in the listing.
    """
    img_tags = soup.find_all("img")

    urls = []
    for img in img_tags:
        img_url = img.get("src")

        # Filters
        if not img_url:
            continue  # No image found
        if img_url.endswith(".svg"):
            continue  # Likely to be frontend asset
        if img.find_parent("div", class_="item-page-sidebar-content"):
            continue  # Likely to be user profile picture

        full_img_url = urljoin(item.url, img_url)
        urls.append(full_img_url)

    logger.info(f"Found {len(urls)} in listing {item.id}")
    return urls


def request_images(urls: str, base_dir: Path):
    """
    Downloads images from list of urls.
    """

    download_dir = base_dir / "images"
    download_dir.mkdir(exist_ok=True)
    downloaded = 0
    for url in urls:
        try:
            logger.info(f"Downloading {url}")

            image_data = requests.get(url).content
            filename = os.path.basename(url)
            file_path = download_dir / f"{filename}.{IMAGE_EXT}"

            if file_path.exists():
                logger.info(f"Found existing file at {file_path}, skipping...")
                continue

            with open(file_path, "wb") as f:
                f.write(image_data)

            downloaded += 1
            avoid_rate_limit()
        except Exception as error:
            logger.exception(
                f"Failed downloading {url}",
            )
    logger.info(f"Downloaded {downloaded}/{len(urls)} images!")
    return
