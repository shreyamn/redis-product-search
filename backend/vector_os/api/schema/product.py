from pydantic import BaseModel


class CatalogItem(BaseModel):
    product_id: str
    name: str
    gender: str
    category: str
    img_url: str
    text_vector: str
    img_vector: str


class SimilarityCatalogItem(CatalogItem):
    vector_distance: float
    similarity_score: float

    def __init__(self, *args, **kwargs):
        kwargs["similarity_score"] = 1 - float(kwargs["vector_distance"])
        super().__init__(*args, **kwargs)


class CatalogSearchRequest(BaseModel):
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""
    product_id: int


class CatalogQueryResponse(BaseModel):
    total: int
    items: list[CatalogItem]


class CatalogSimilarityResponse(BaseModel):
    total: int
    items: list[SimilarityCatalogItem]
