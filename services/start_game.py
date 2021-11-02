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