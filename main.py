from fastapi import FastAPI, status
import pony.orm as pony

from models import db

app = FastAPI()

@app.get("/home")
async def home():
    return {"message" : "Project home Grupo Peluche"}

@app.get("/partidas")
async def listar_partidas():
    with pony.db_session:
        partidas = db.Partida.select(
                    lambda p: (not p.iniciada) and len(p.jugadores) < 6
                    )
        return [{
            'id_partida': p.id_partida,
            'nombre_partida': p.nombre,
            'cantidad_jugadores': len(p.jugadores)
                } for p in partidas]
