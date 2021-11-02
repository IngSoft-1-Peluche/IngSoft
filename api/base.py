from fastapi import FastAPI

from fastapi import APIRouter

from . import partidas

api_router = APIRouter()

app = FastAPI()

api_router.include_router(partidas.router, prefix="/partidas", tags=["partidas"])



@app.get("/home")
async def home():
    return {"message": "Project home Grupo Peluche"}

