from fastapi import status, HTTPException
import pony.orm as pony

from ..models import db
from ..models.jugador import asociar_a_partida, crear_jugador

from ..services.start_game import asignar_orden_aleatorio
from .partidas import router, PartidaOut

@router.get("/{id_partida}")
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



@router.put("/{id_partida}", response_model=PartidaOut)
async def unirse_a_partida(apodo: str, id_partida: int):
    with pony.db_session:
        partida = db.Partida[id_partida]
        if len(partida.jugadores) < 6:
            jugador = crear_jugador(apodo)
            asociar_a_partida(partida, jugador)
        else:
            raise HTTPException(
                status_code=500, detail="No puedes unirte a esta partida"
            )

    return PartidaOut(
        id_partida=partida.id_partida,
        nombre_partida=partida.nombre,
        id_jugador=jugador.id_jugador,
        apodo=jugador.apodo,
        jugador_creador=False,
    )

  
@router.patch("/{id_partida}", status_code=status.HTTP_201_CREATED)
async def iniciar_partida(id_jugador: int, id_partida: int):
    with pony.db_session:
        partida = db.Partida[id_partida]
        if (
            partida.iniciada == False
            and 1 < len(partida.jugadores) < 7
            and id_jugador == partida.creador.id_jugador
        ):
            partida.iniciada = True
            asignar_orden_aleatorio(partida)
            return status.HTTP_201_CREATED
        elif partida.iniciada == True:
            raise HTTPException(status_code=500, detail="La partida ya se esta jugando")
        elif id_jugador != partida.creador.id_jugador:
            raise HTTPException(
                status_code=500, detail="No eres el dueño de la partida"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="La partida no cumple con los jugadores necesarios para iniciarse",
            )
