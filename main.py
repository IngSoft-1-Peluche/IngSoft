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

@app.get("/partidas/{id_partida}")
async def detalle_partida(id_partida: int):
    with pony.db_session:
        partida = db.Partida[id_partida]
        jugadores_json = [{
            'id_jugador': j.id_jugador,
            'apodo': j.apodo,
            'orden': j.orden_turno,
            'en_turno': j.orden_turno == partida.jugador_en_turno
        } for j in partida.jugadores.order_by(db.Jugador.orden_turno)]
        return {
            'id_partida': partida.id_partida,
            'nombre': partida.nombre,
            'jugadores': jugadores_json
                }
