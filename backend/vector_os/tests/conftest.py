import json
from pathlib import Path

import httpx
import numpy as np
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from redis import Redis
from redisvl.index import SearchIndex

from vector_os import config
from vector_os.db.utils import get_schema
from vector_os.main import app


@pytest.fixture(scope="session")
def index():
    Redis.from_url(config.REDIS_URL).flushdb()
    index = SearchIndex(schema=get_schema(), redis_url=config.REDIS_URL)
    index.create(overwrite=True)
    yield index
    index.disconnect()


@pytest.fixture(scope="session", autouse=True)
def test_data(index):
    fixture_path = Path(__file__).resolve().parent / "test_vectors.json"
    with open(fixture_path, "r", encoding="utf-8") as file_handle:
        products = json.load(file_handle)

    parsed_products = []
    for product in products:
        parsed_products.append(
            {
                "text_vector": np.array(product["text_vector"], dtype=np.float32).tobytes(),
                "img_vector": np.array(product["img_vector"], dtype=np.float32).tobytes(),
                "category": product["product_metadata"]["master_category"],
                "img_url": product["product_metadata"]["img_url"],
                "name": product["product_metadata"]["name"],
                "gender": product["product_metadata"]["gender"],
                "product_id": product["product_id"],
            }
        )

    index.load(data=parsed_products, id_field="product_id")
    return parsed_products


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with LifespanManager(app=app):
        async with AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test/api/v1/"  # type: ignore[arg-type]
        ) as client:
            yield client
