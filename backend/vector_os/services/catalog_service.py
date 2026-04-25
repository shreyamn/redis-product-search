import asyncio

import numpy as np
from redisvl.index import AsyncSearchIndex
from redisvl.query import CountQuery, FilterQuery, VectorQuery
from redisvl.query.filter import Tag

from vector_os import config
from vector_os.api.schema.product import CatalogQueryResponse, CatalogSimilarityResponse


class CatalogService:
    def __init__(self, index: AsyncSearchIndex):
        self.index = index

    @staticmethod
    def _build_filter(gender: str = "", category: str = ""):
        expression = None
        if gender:
            expression = Tag("gender") == gender
        if category:
            category_filter = Tag("category") == category
            expression = category_filter if expression is None else expression & category_filter
        return expression

    async def list_items(self, limit: int, skip: int, gender: str, category: str) -> CatalogQueryResponse:
        filter_expression = self._build_filter(gender, category)
        filter_query = FilterQuery(
            return_fields=[],
            filter_expression=filter_expression,
            num_results=limit,
        )
        result = await self.index.search(filter_query.query.paging(skip, limit))
        docs = result.docs
        return CatalogQueryResponse(total=result.total, items=[doc.__dict__ for doc in docs])

    async def find_neighbors(self, product_id: int, vector_field_name: str, number_of_results: int, gender: str, category: str) -> CatalogSimilarityResponse:
        product = await self.index.fetch(product_id)
        vector_blob = np.frombuffer(product[vector_field_name], dtype=np.float32)
        filter_expression = self._build_filter(gender, category)

        vector_query = VectorQuery(
            vector=vector_blob,
            vector_field_name=vector_field_name,
            num_results=number_of_results,
            return_fields=config.RETURN_FIELDS,
            filter_expression=filter_expression,
        )

        count_query = CountQuery(filter_expression) if filter_expression is not None else "*"
        total, matches = await asyncio.gather(
            self._count_matches(count_query),
            self.index.query(vector_query),
        )
        return CatalogSimilarityResponse(total=total, items=matches)

    async def _count_matches(self, count_query) -> int:
        if count_query == "*":
            return (await self.index.search("*")).total
        return await self.index.query(count_query)
