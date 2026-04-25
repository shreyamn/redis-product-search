from fastapi import APIRouter

from vector_os.api.routes import catalog

api_router = APIRouter()
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])

