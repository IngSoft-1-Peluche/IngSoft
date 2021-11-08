import pony.orm as pony

from .board_functions import posiciones_posibles_a_mover
from board.board import RECINTOS
import random


def numero_dado():
    return random.randint(1, 6)


def pasar_turno(partida):
    jugador_siguiente = siguiente_jugador(partida)
    action1 = ""
    action2 = "terminaron_turno"
    action3 = "tu_turno"
    data1 = {}
    data2 = {"nombre_jugador": jugador_siguiente.apodo}
    data3 = {}
    personal_message = {"action": action1, "data": data1}
    to_broadcast = {"action": action2, "data": data2}
    message_to = {
        "id_jugador": jugador_siguiente.id_jugador,
        "action": action3,
        "data": data3,
    }
    partida.jugador_en_turno = (partida.jugador_en_turno % len(partida.jugadores)) + 1
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
    }


def siguiente_jugador(partida):
    siguiente = (partida.jugador_en_turno % len(partida.jugadores)) + 1
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
        action3 = ""
        dado = numero_dado()
        jugador.ultima_tirada = dado
        casillas_a_mover = posiciones_posibles_a_mover(jugador.posicion, dado)

        data1 = {"numero_dado": dado, "casillas_a_mover": casillas_a_mover}

        data2 = {"nombre_jugador": jugador.apodo, "numero_dado": dado}
        data3 = {}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    else:
        action1 = "error_imp"
        data1 = {"message": "No es tu turno"}
        personal_message = {"action": action1, "data": data1}
        action2 = ""
        data2 = {}
        to_broadcast = {"action": action2, "data": data2}
        action3 = ""
        data3 = {}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
    }


def mover_jugador(jugador, nueva_posicion):
    partida = jugador.partida
    posibles_casillas = posiciones_posibles_a_mover(
        jugador.posicion, jugador.ultima_tirada
    )
    if (
        jugador.orden_turno == partida.jugador_en_turno
        and nueva_posicion in posibles_casillas
    ):
        jugador.cambiar_posicion(nueva_posicion)
        action1 = "me_movi"
        action2 = "se_movio"
        action3 = ""
        data1 = {"posicion_final": nueva_posicion}
        data2 = {"nombre_jugador": jugador.apodo, "posicion_final": nueva_posicion}
        data3 = {}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    elif jugador.orden_turno != partida.jugador_en_turno:
        action1 = "error_imp"
        action2 = ""
        action3 = ""
        data1 = {"message": "No es tu turno"}
        data2 = {}
        data3 = {}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    else:
        action1 = "casilla_invalida"
        action2 = ""
        action3 = ""
        data1 = {"message": "No es una posicion valida"}
        data2 = {}
        data3 = {}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
    }


def anunciar_sospecha(jugador, carta_monstruo, carta_victima):
    partida = jugador.partida
    if (
        jugador.orden_turno == partida.jugador_en_turno
        and jugador.posicion in RECINTOS.keys()
    ):
        recinto = RECINTOS[jugador.posicion]
        jugador_que_muestra = jugador
        contador = jugador.orden_turno % partida.cantidad_jugadores()
        jugadores_ordenados = sorted(partida.jugadores, key=lambda x: x.orden_turno)
        while contador != jugador.orden_turno - 1:
            cartas = []
            for c in jugadores_ordenados[contador].cartas:
                cartas.append(c.nombre)
            if recinto in cartas or carta_monstruo in cartas or carta_victima in cartas:
                jugador_que_muestra = jugadores_ordenados[contador]
                break
            contador = (contador + 1) % partida.cantidad_jugadores()
        if jugador == jugador_que_muestra:
            action1 = ""
            action2 = "cartas_sospechadas_fail"
            action3 = ""
            data1 = {}
            data2 = {
                "nombre_sospechador": jugador.apodo,
                "cartas_sospechadas": [recinto, carta_monstruo, carta_victima],
            }
            data3 = {}
            personal_message = {"action": action1, "data": data1}
            to_broadcast = {"action": action2, "data": data2}
            message_to = {
                "action": action3,
                "data": data3,
                "id_jugador": -1,
            }
        else:
            action1 = ""
            action2 = "cartas_sospechadas"
            action3 = "muestra"
            data1 = {}
            data2 = {
                "nombre_sospechador": jugador.apodo,
                "cartas_sospechadas": [recinto, carta_monstruo, carta_victima],
            }
            data3 = {}
            personal_message = {"action": action1, "data": data1}
            to_broadcast = {"action": action2, "data": data2}
            message_to = {
                "action": action3,
                "data": data3,
                "id_jugador": jugador_que_muestra.id_jugador,
            }
    elif jugador.posicion not in RECINTOS.keys():
        action1 = "no_recinto"
        action2 = ""
        action3 = ""
        data1 = {"message": "No estás en un recinto"}
        data2 = {}
        data3 = {}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {
            "action": action3,
            "data": data3,
            "id_jugador": -1,
        }
    else:
        action1 = "error_imp"
        action2 = ""
        action3 = ""
        data1 = {"message": "No es tu turno"}
        data2 = {}
        data3 = {}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {
            "action": action3,
            "data": data3,
            "id_jugador": -1,
        }
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
    }


def responder_sospecha(jugador, carta):
    action1 = "no_carta"
    action2 = ""
    action3 = ""
    data1 = {"message": "No tienes esa carta para mostrar"}
    data2 = {}
    data3 = {}
    cartas = []
    for c in jugador.cartas:
        cartas.append(c.nombre)
    if carta in cartas:
        action1 = "muestra_carta"
        data1 = {}
        action3 = "carta_seleccionada"
        data3 = {"carta_seleccionada": carta}
    personal_message = {"action": action1, "data": data1}
    to_broadcast = {"action": action2, "data": data2}
    message_to = {"action": action3, "data": data3, "id_jugador": jugador.id_jugador}

    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
    }
