import pony.orm as pony
from models import db
from .board_functions import posiciones_posibles_a_mover
import random

def numero_dado():
    return random.randint(1, 6)


@pony.db_session()
def pasar_turno(partida):
    jugador_siguiente = siguiente_jugador(partida)
    action1 = ""
    action2 = "terminaron_turno"
    action3= "tu_turno"
    data1 = {}
    data2 = {"nombre_jugador": jugador_siguiente.apodo}
    data3 = {}
    personal_message = {"action": action1, "data": data1}
    to_broadcast = {"action": action2, "data": data2}
    message_to = {"id_jugador": jugador_siguiente.id_jugador, "action": action3, "data": data3}
    partida.jugador_en_turno = (partida.jugador_en_turno % len(partida.jugadores)) + 1
    return {"personal_message": personal_message, "to_broadcast":to_broadcast, "message_to": message_to}

@pony.db_session()
def siguiente_jugador(partida):
    siguiente = (partida.jugador_en_turno % len(partida.jugadores)) + 1 
    print("debug")
    print(siguiente)
    jugadores = partida.jugadores
    for j in jugadores:
        if j.orden_turno == siguiente:
            jugador_siguiente = j
    return jugador_siguiente
    

def jugador_esta_en_turno(jugador, partida):
    if jugador.orden_turno == partida.jugador_en_turno:
        return True
    else:
        return False


def tirar_dado(jugador, partida):
    if jugador_esta_en_turno(jugador, partida):
        action1 = "tire_dado"
        action2 = "tiraron_dado"
        action3= ""
        dado = numero_dado()
        casillas_a_mover = posiciones_posibles_a_mover(jugador.posicion, dado)
        data1 = {"numero_dado": dado, "casillas_a_mover": casillas_a_mover}
        data2 = {"nombre_jugador": jugador.apodo,"numero_dado": dado}
        data3 = ""
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": 0}
    else:
        action1 = "error_imp"
        data1 = {"message": "No es tu turno"}
        personal_message = {"action": action1, "data": data1}
        action2 = ""
        data2 = ""
        to_broadcast = {"action": action2, "data": data2}
        action3 = ""
        data3 = ""
        message_to = {"action": action3, "data": data3, "id_jugador": 0}
    return {"personal_message": personal_message, "to_broadcast":to_broadcast, "message_to": message_to}
        