from fastapi import APIRouter

from . import partidas_id

api_router = APIRouter()
api_router.include_router(partidas_id.router, prefix="/partidas", tags=["partidas"])
