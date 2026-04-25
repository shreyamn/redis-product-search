from vector_os.oslayer import runtime_profile

DATA_SOURCE_URL = "https://redis-product-search.s3.us-east-2.amazonaws.com/products.json"
PROJECT_NAME = "Vector OS"
CATALOG_INDEX_NAME = "vector_os_catalog"
RETURN_FIELDS = [
    "product_id",
    "name",
    "gender",
    "category",
    "img_url",
    "img_vector",
    "text_vector",
]

RUNTIME = runtime_profile()
API_V1_STR = RUNTIME.api_prefix
API_DOCS = RUNTIME.docs_url
OPENAPI_DOCS = RUNTIME.openapi_url
REDIS_URL = RUNTIME.redis_url
DEPLOYMENT_ENV = RUNTIME.deployment_env
WRITE_CONCURRENCY = RUNTIME.write_concurrency
DATA_LOCATION = str(RUNTIME.data_dir)
