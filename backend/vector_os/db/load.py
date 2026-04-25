#!/usr/bin/env python3
import asyncio
import json
from typing import List

import numpy as np
import requests
from redisvl.index import AsyncSearchIndex

from vector_os import config
from vector_os.db.utils import get_schema


def read_from_remote_source():
    response = requests.get(config.DATA_SOURCE_URL)
    return response.json()


def read_product_json_vectors() -> List:
    try:
        with open(config.DATA_LOCATION + "/products.json", encoding="utf-8") as file_handle:
            product_vectors = json.load(file_handle)
    except FileNotFoundError:
        print("Local dataset not found, downloading seed data")
        product_vectors = read_from_remote_source()

    return product_vectors


async def write_products(index: AsyncSearchIndex, products: List[dict]):
    def normalize_product(product: dict) -> dict:
        return {
            "product_id": product["product_id"],
            "gender": product["product_metadata"]["gender"],
            "category": product["product_metadata"]["master_category"],
            "name": product["product_metadata"]["name"],
            "img_url": product["product_metadata"]["img_url"],
            "img_vector": np.array(product["img_vector"], dtype=np.float32).tobytes(),
            "text_vector": np.array(product["text_vector"], dtype=np.float32).tobytes(),
        }

    await index.load(
        data=[normalize_product(product) for product in products],
        concurrency=config.WRITE_CONCURRENCY,
        id_field="product_id",
    )


async def load_data():
    schema = get_schema()
    index = AsyncSearchIndex(schema, redis_url=config.REDIS_URL)

    if await index.exists() and len((await index.search("*")).docs) > 0:
        print("Catalog index already exists and contains data")
        return

    await index.create(overwrite=True)
    print("Preparing Vector OS catalog data")
    products = read_product_json_vectors()
    print("Loading catalog entries into Redis")
    await write_products(index, products)
    print("Catalog load completed")


if __name__ == "__main__":
    asyncio.run(load_data())
