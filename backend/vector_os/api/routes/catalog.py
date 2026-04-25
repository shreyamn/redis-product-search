from fastapi import APIRouter, Depends
from redisvl.index import AsyncSearchIndex

from vector_os.api.schema.product import (
    CatalogQueryResponse,
    CatalogSearchRequest,
    CatalogSimilarityResponse,
)
from vector_os.db.utils import get_async_index
from vector_os.services.catalog_service import CatalogService

router = APIRouter()


def get_catalog_service(index: AsyncSearchIndex = Depends(get_async_index)) -> CatalogService:
    return CatalogService(index)


@router.get(
    "/",
    response_model=CatalogQueryResponse,
    name="catalog:list_items",
    operation_id="list_catalog_items",
)
async def list_catalog_items(
    limit: int = 20,
    skip: int = 0,
    gender: str = "",
    category: str = "",
    catalog: CatalogService = Depends(get_catalog_service),
) -> CatalogQueryResponse:
    return await catalog.list_items(limit=limit, skip=skip, gender=gender, category=category)


@router.post(
    "/vectorsearch/image",
    response_model=CatalogSimilarityResponse,
    name="catalog:find_related_by_image",
    operation_id="find_related_by_image",
)
async def find_related_by_image(
    similarity_request: CatalogSearchRequest,
    catalog: CatalogService = Depends(get_catalog_service),
) -> CatalogSimilarityResponse:
    return await catalog.find_neighbors(
        product_id=similarity_request.product_id,
        vector_field_name="img_vector",
        number_of_results=similarity_request.number_of_results,
        gender=similarity_request.gender,
        category=similarity_request.category,
    )


@router.post(
    "/vectorsearch/text",
    response_model=CatalogSimilarityResponse,
    name="catalog:find_related_by_text",
    operation_id="find_related_by_text",
)
async def find_related_by_text(
    similarity_request: CatalogSearchRequest,
    catalog: CatalogService = Depends(get_catalog_service),
) -> CatalogSimilarityResponse:
    return await catalog.find_neighbors(
        product_id=similarity_request.product_id,
        vector_field_name="text_vector",
        number_of_results=similarity_request.number_of_results,
        gender=similarity_request.gender,
        category=similarity_request.category,
    )
