import pytest
from httpx import AsyncClient

from vector_os.api.schema.product import CatalogSearchRequest


@pytest.fixture(scope="module")
def gender(test_data):
    return test_data[0]["gender"]


@pytest.fixture(scope="module")
def category(test_data):
    return test_data[0]["category"]


@pytest.fixture(scope="module")
def bad_req_json():
    return {"not": "valid"}


@pytest.fixture(scope="module")
def product_req(gender, category, test_data):
    return CatalogSearchRequest(
        gender=gender,
        category=category,
        product_id=test_data[0]["product_id"],
    )


@pytest.mark.asyncio(scope="session")
async def test_root_w_filters(async_client: AsyncClient, gender: str, category: str) -> None:
    response = await async_client.get(f"catalog/?gender={gender}&category={category}")

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["items"]) == 2
    for item in content["items"]:
        assert item["category"] == category
        assert item["gender"] == gender


@pytest.mark.asyncio(scope="session")
async def test_root_na_category(async_client: AsyncClient, gender: str):
    response = await async_client.get(f"catalog/?gender={gender}&category=NA")

    assert response.status_code == 200
    content = response.json()
    assert content["total"] == 0
    assert len(content["items"]) == 0


@pytest.mark.asyncio(scope="session")
async def test_vector_by_text(async_client: AsyncClient, gender: str, category: str, product_req: CatalogSearchRequest):
    response = await async_client.post("catalog/vectorsearch/text", json=product_req.model_dump())

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["items"]) == 2
    for item in content["items"]:
        assert item["category"] == category
        assert item["gender"] == gender


@pytest.mark.asyncio(scope="session")
async def test_vector_by_text_bad_input(async_client: AsyncClient, bad_req_json: dict):
    response = await async_client.post("catalog/vectorsearch/text", json=bad_req_json)
    assert response.status_code == 422


@pytest.mark.asyncio(scope="session")
async def test_vector_by_img(async_client: AsyncClient, product_req: CatalogSearchRequest):
    response = await async_client.post("catalog/vectorsearch/image", json=product_req.model_dump())

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["items"]) == 2


@pytest.mark.asyncio(scope="session")
async def test_vector_by_img_bad_input(async_client: AsyncClient, bad_req_json: dict):
    response = await async_client.post("catalog/vectorsearch/image", json=bad_req_json)
    assert response.status_code == 422
