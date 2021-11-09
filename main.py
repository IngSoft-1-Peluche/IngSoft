from fastapi import FastAPI, status, HTTPException, WebSocket, WebSocketDisconnect
import pony.orm as pony
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models import db, crear_jugador, crear_partida, get_partida, get_jugador
from my_sockets import ConnectionManager
from services.start_game import (
    iniciar_partida_service,
    mostrar_cartas,
)
from services.in_game import (
    tirar_dado,
    pasar_turno,
    mover_jugador,
    anunciar_sospecha,
    responder_sospecha,
    acusar
)

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
                "cantidad_jugadores": p.cantidad_jugadores(),
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
        partida = get_partida(id_partida)
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
            "iniciada": partida.iniciada,
            "jugadores": jugadores_json,
        }


@app.put("/partidas/{id_partida}", response_model=PartidaOut)
async def unirse_a_partida(apodo: str, id_partida: int):
    with pony.db_session:
        partida = get_partida(id_partida)
        if len(partida.jugadores) < 6:
            jugador = crear_jugador(apodo)
            jugador.asociar_a_partida(partida)
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


@app.patch("/partidas/{id_partida}", status_code=status.HTTP_201_CREATED)
async def iniciar_partida(id_jugador: int, id_partida: int):
    with pony.db_session:
        partida = get_partida(id_partida)
        if (
            partida.iniciada == False
            and 1 < len(partida.jugadores) < 7
            and id_jugador == partida.creador.id_jugador
        ):
            iniciar_partida_service(partida)
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


# Toda la parte de WEBSockets

manager = ConnectionManager()


@app.websocket("/ws/{id_jugador}")
async def websocket_endpoint(websocket: WebSocket, id_jugador: int):
    with pony.db_session:
        jugador = get_jugador(id_jugador)
        partida = jugador.partida
        await manager.connect(jugador.id_jugador, partida.id_partida, websocket)
        try:
            while True:
                entrada = await websocket.receive_json()
                respuesta = {
                    "personal_message": {"action": "error_imp", "data": "No existe esa accion"},
                    "to_broadcast": {"action": "", "data": ""},
                    "message_to": {"action": "", "data": "", "id_jugador": ""},
                }
                if entrada["action"] == "tirar_dado":
                    respuesta = tirar_dado(jugador, partida)
                if entrada["action"] == "mover_jugador":
                    respuesta = mover_jugador(
                        jugador, entrada["data"]["nueva_posicion"]
                    )
                if entrada["action"] == "terminar_turno":
                    respuesta = pasar_turno(partida)
                if entrada["action"] == "sospechan":
                    respuesta = anunciar_sospecha(
                        jugador,
                        entrada["data"]["carta_monstruo"],
                        entrada["data"]["carta_victima"],
                    )
                if entrada["action"] == "respuesta_sospecha":
                    respuesta = responder_sospecha(jugador, entrada["data"]["carta"])
                if entrada["action"] == "acusar":
                    respuesta = acusar(
                        jugador,
                        partida,
                        entrada["data"]["carta_monstruo"],
                        entrada["data"]["carta_victima"],
                        entrada["data"]["carta_recinto"]
                    )
                if entrada["action"] == "mostrar_cartas":
                    respuesta = mostrar_cartas(jugador)
                await manager.send_personal_message(
                    respuesta["personal_message"]["action"],
                    respuesta["personal_message"]["data"],
                    websocket,
                )
                await manager.broadcast(
                    respuesta["to_broadcast"]["action"],
                    respuesta["to_broadcast"]["data"],
                    partida.id_partida,
                )
                await manager.send_message_to(
                    respuesta["message_to"]["action"],
                    respuesta["message_to"]["data"],
                    respuesta["message_to"]["id_jugador"],
                )
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast(
                f"Desconectado",
                f"El jugador #{id_jugador} se fue de la partida",
                partida.id_partida,
            )
