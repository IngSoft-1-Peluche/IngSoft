import pony.orm as pony
from models import db
import random
import numpy as np

from board.board import CARTAS, PUERTAS, COLORES


@pony.db_session()
def iniciar_partida_service(partida):
    partida.iniciada = True
    asignar_orden_aleatorio(partida)
    asignar_posiciones_iniciales(partida)
    asignar_colores(partida)
    crear_cartas(partida)
    generar_sobre(partida)
    distribuir_cartas(partida)


@pony.db_session()
def asignar_orden_aleatorio(partida):
    jugadores = partida.jugadores
    random.shuffle(list(jugadores))
    i = 1
    for jugador in jugadores:
        jugador.orden_turno = i
        if i == 1:
            jugador.estado_turno = "D"
        i += 1
    return jugadores


@pony.db_session()
def asignar_posiciones_iniciales(partida):
    jugadores = partida.jugadores
    random.shuffle(list(jugadores))
    for jugador in jugadores:
        jugador.posicion = random.choice(PUERTAS)
    return jugadores


@pony.db_session()
def asignar_colores(partida):
    jugadores = partida.jugadores
    random.shuffle(list(jugadores))
    i = 0
    for jugador in jugadores:
        jugador.color = COLORES[i]
        i += 1
    return jugadores


def tirar_dado():
    return random.randint(1, 6)


@pony.db_session()
def crear_cartas(partida):
    for carta in CARTAS:
        carta_objeto = db.Carta(partida=partida, nombre=carta[0], tipo=carta[1])
        partida.cartas.add(carta_objeto)


@pony.db_session()
def generar_sobre(partida):
    recintos = list(partida.cartas.select(lambda c: c.tipo == "R"))
    recinto = random.choice(recintos)
    partida.sobre.add(recinto)
    victimas = list(partida.cartas.select(lambda c: c.tipo == "V"))
    victima = random.choice(victimas)
    partida.sobre.add(victima)
    monstruos = list(partida.cartas.select(lambda c: c.tipo == "M"))
    monstruo = random.choice(monstruos)
    partida.sobre.add(monstruo)


@pony.db_session()
def distribuir_cartas(partida):
    cartas = list(partida.cartas.select(lambda c: c not in partida.sobre))
    random.shuffle(cartas)
    cant_jugadores = partida.cantidad_jugadores()
    grupos_cartas = np.array_split(cartas, cant_jugadores)
    for jugador in partida.jugadores.order_by(db.Jugador.orden_turno):
        for carta in grupos_cartas[jugador.orden_turno - 1]:
            jugador.cartas.add(carta)


@pony.db_session()
def mostrar_cartas(jugador):
    respuesta = {"action": "", "data": ""}
    respuesta_broadcast = {"action": "", "data": ""}
    respuesta_to = {"action": "", "data": "", "id_jugador": -1}
    respuesta["action"] = "mostrar_cartas"
    data = {"cartas": []}
    for carta in jugador.cartas:
        data["cartas"].append(carta.nombre)
    respuesta["data"] = data
    return {
        "personal_message": respuesta,
        "to_broadcast": respuesta_broadcast,
        "message_to": respuesta_to,
    }
