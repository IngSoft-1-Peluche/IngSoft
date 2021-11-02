import pony.orm as pony
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import db
from api import api_router

# línea que sirve para debug
pony.set_sql_debug(True)

# creación de tablas para los modelos
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

app = FastAPI()
app.include_router(api_router, prefix="")

@app.get("/home")
async def home():
    return {"message": "Project home Grupo Peluche"}

# Permisos para fetch de Front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
