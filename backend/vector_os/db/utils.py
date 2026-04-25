import logging

from redisvl.index import AsyncSearchIndex
from redisvl.schema import IndexSchema

from vector_os import config
from vector_os.oslayer import runtime_profile

logger = logging.getLogger(__name__)
_runtime = runtime_profile()
_global_index = None


def get_schema() -> IndexSchema:
    schema_file = _runtime.schema_dir / "products.yml"
    return IndexSchema.from_yaml(str(schema_file))


async def get_async_index():
    global _global_index
    if _global_index is None:
        _global_index = AsyncSearchIndex(get_schema(), redis_url=config.REDIS_URL)
    return _global_index
