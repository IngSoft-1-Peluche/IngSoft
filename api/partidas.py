import pony.orm as pony
from fastapi import status, APIRouter
from pydantic import BaseModel

from models import db
from models.partida import crear_partida
from models.jugador import crear_jugador

router = APIRouter()

class PartidaIn(BaseModel):
    nombre_partida: str
    apodo: str

class PartidaOut(BaseModel):
    id_partida: int
    nombre_partida: str
    id_jugador: int
    apodo: str
    jugador_creador: bool

@router.get("/")
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


@router.post("/", response_model=PartidaOut, status_code=status.HTTP_201_CREATED)
async def respuesta_creacion(nueva_partida: PartidaIn) -> int:
    nueva_partida_dicionario = nueva_partida.dict()
    jugador = crear_jugador(nueva_partida_dicionario["apodo"])
    partida = crear_partida(nueva_partida_dicionario["nombre_partida"], jugador)

    return PartidaOut(
        id_partida=partida.id_partida,
        nombre_partida=partida.nombre,
        id_jugador=jugador.id_jugador,
        apodo=jugador.apodo,
        jugador_creador=True,
    )
