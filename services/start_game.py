import pony.orm as pony
import random


@pony.db_session()
def asignar_orden_aleatorio(partida):
    jugadores = partida.jugadores
    random.shuffle(list(jugadores))
    i = 1
    for jugador in jugadores:
        jugador.orden_turno = i
        i += 1
    return jugadores


def tirar_dado():
    return random.randint(1, 6)


@pony.db_session()
def pasar_turno(partida):
    jugadores = partida.jugadores
    partida.jugador_en_turno = (partida.jugador_en_turno % len(jugadores)) + 1


def jugador_esta_en_turno(jugador, partida):
    if jugador.orden_turno == partida.jugador_en_turno:
        return True
    else:
        return False
