from fastapi.routing import APIRouter

from api.currencies.views import router as currencies_router
from api.healthcheck.views import router as healthcheck_router

api_router = APIRouter()
api_router.include_router(healthcheck_router)
api_router.include_router(currencies_router)
