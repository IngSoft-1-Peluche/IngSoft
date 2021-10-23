from fastapi import FastAPI, status
import pony.orm as pony
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models import db, crear_jugador, crear_partida, asociar_a_partida

app = FastAPI()

# Permisos para fetch de Front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PartidaIn(BaseModel):
    nombre_partida: str
    apodo: str


class PartidaOut(BaseModel):
    id_partida: int
    nombre_partida: str
    id_jugador: int
    apodo: str
    jugador_creador: bool


@app.get("/home")
async def home():
    return {"message": "Project home Grupo Peluche"}


@app.get("/partidas")
async def listar_partidas():
    with pony.db_session:
        partidas = db.Partida.select(
            lambda p: (not p.iniciada) and len(p.jugadores) < 6
        )
        return [
            {
                "id_partida": p.id_partida,
                "nombre_partida": p.nombre,
                "cantidad_jugadores": len(p.jugadores),
            }
            for p in partidas
        ]


@app.post("/partidas/", response_model=PartidaOut, status_code=status.HTTP_201_CREATED)
async def respuesta_creacion(nueva_partida: PartidaIn) -> int:
    nueva_partida_dicionario = nueva_partida.dict()
    jugador = crear_jugador(nueva_partida_dicionario["apodo"])
    partida = crear_partida(
        nueva_partida_dicionario["nombre_partida"], jugador.id_jugador
    )

    return PartidaOut(
        id_partida=partida.id_partida,
        nombre_partida=partida.nombre,
        id_jugador=jugador.id_jugador,
        apodo=jugador.apodo,
        jugador_creador=True,
    )


@app.get("/partidas/{id_partida}")
async def detalle_partida(id_partida: int):
    with pony.db_session:
        partida = db.Partida[id_partida]
        jugadores_json = [
            {
                "id_jugador": j.id_jugador,
                "apodo": j.apodo,
                "orden": j.orden_turno,
                "en_turno": j.orden_turno == partida.jugador_en_turno,
            }
            for j in partida.jugadores.order_by(db.Jugador.orden_turno)
        ]
        return {
            "id_partida": partida.id_partida,
            "nombre": partida.nombre,
            "jugadores": jugadores_json,
        }


@app.put("/partidas/{id_partida}")
async def unirse_a_partida(id_partida: int, apodo: str):
    with pony.db_session:
        partida = db.Partida[id_partida]
        if (len(partida.jugadores) < 6):
            jugador = crear_jugador(apodo)
            asociar_a_partida(partida, jugador)
        else:
            return 0

    return PartidaOut(
        id_partida=partida.id_partida,
        nombre_partida=partida.nombre,
        id_jugador=jugador.id_jugador,
        apodo=jugador.apodo,
        jugador_creador=False,
    )
