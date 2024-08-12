from fastapi import APIRouter

from api.gsw.router import router as gsw_router


def health_check():
    return {}


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(gsw_router)
