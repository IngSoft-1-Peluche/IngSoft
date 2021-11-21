import pony.orm as pony
import random

from .board_functions import posiciones_posibles_a_mover
from board.board import RECINTOS
from models import db


def numero_dado():
    return random.randint(1, 6)


def pasar_turno(jugador, partida):
    if jugador.estado_turno == "F" or jugador.estado_turno == "SA":
        jugador_siguiente = partida.siguiente_jugador()
        partida.pasar_turno()
        jugador.estado_turno = "N"
        jugador_siguiente.estado_turno = "D"
        action1 = ""
        action2 = ""
        action3 = "tu_turno"
        action4 = "mensaje_sistema"
        data1 = ""
        data2 = ""
        data3 = ""
        data4 = {"message": f"El jugador {jugador.apodo} termino su turno. Ahora comienza el del jugador {jugador_siguiente.apodo}."}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {
            "id_jugador": jugador_siguiente.id_jugador,
            "action": action3,
            "data": data3,
        }
        system = {"action": action4, "data": data4}
    else: 
        action1 = "error_imp"
        data1 = {"message": "No estas en la etapa de pasar el turno"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {"action": "", "data": "", "id_jugador": -1}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
        "system": system,
    }


def jugador_esta_en_turno(jugador, partida):
    if jugador.orden_turno == partida.jugador_en_turno:
        return True
    else:
        return False


def tirar_dado(jugador, partida):
    if jugador_esta_en_turno(jugador, partida) and jugador.estado_turno == "D":
        action1 = "tire_dado"
        action2 = ""
        action3 = ""
        action4 = "mensaje_sistema"
        dado = numero_dado()
        jugador.ultima_tirada = dado
        casillas_a_mover = posiciones_posibles_a_mover(jugador.posicion, dado)
        jugador.estado_turno = "M"

        data1 = {"numero_dado": dado, "casillas_a_mover": casillas_a_mover}

        data2 = ""
        data3 = ""
        data4 = {"message": f"El jugador {jugador.apodo} tiro el dado y obtuvo un {dado}"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
        system = {"action": action4, "data": data4}
    elif jugador_esta_en_turno(jugador, partida) and jugador.estado_turno != "D":
        action1 = "error_imp"
        data1 = {"message": "Ya no estas en la etapa de tirar el dado"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {"action": "", "data": "", "id_jugador": -1}
    else:
        action1 = "error_imp"
        data1 = {"message": "No es tu turno"}
        personal_message = {"action": action1, "data": data1}
        action2 = ""
        data2 = ""
        to_broadcast = {"action": action2, "data": data2}
        action3 = ""
        data3 = ""
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
        "system": system,
    }


def mover_jugador(jugador, nueva_posicion):
    partida = jugador.partida
    posibles_casillas = posiciones_posibles_a_mover(
        jugador.posicion, jugador.ultima_tirada
    )
    if (
        jugador.orden_turno == partida.jugador_en_turno
        and nueva_posicion in posibles_casillas
        and jugador.estado_turno == "M"
    ):
        jugador.cambiar_posicion(nueva_posicion)
        jugador.estado_turno = "SA"
        action1 = "me_movi"
        action2 = "se_movio"
        action3 = ""
        action4 = ""
        data1 = {"posicion_final": nueva_posicion}
        data2 = {
            "nombre_jugador": jugador.apodo,
            "posicion_final": nueva_posicion,
            "lista_jugadores": lista_estado_jugadores(partida),
        }
        data3 = ""
        data4 = ""
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
        system = {"action": action4, "data": data4}
    elif jugador.orden_turno != partida.jugador_en_turno:
        action1 = "error_imp"
        data1 = {"message": "No es tu turno"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {"action": "", "data": "", "id_jugador": -1}
    elif jugador.estado_turno != "M":
        action1 = "error_imp"
        data1 = {"message": "No estas en la etapa de moverte"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {"action": "", "data": "", "id_jugador": -1}
    else:
        action1 = "casilla_invalida"
        action2 = ""
        action3 = ""
        data1 = {"message": "No es una posicion valida"}
        data2 = ""
        data3 = ""
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {"action": action3, "data": data3, "id_jugador": -1}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
        "system": system,
    }


def anunciar_sospecha(jugador, carta_monstruo, carta_victima):
    partida = jugador.partida
    if (
        jugador.orden_turno == partida.jugador_en_turno
        and jugador.posicion in RECINTOS.keys()
        and jugador.estado_turno == "SA"
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
            jugador.estado_turno = "F"
            action1 = ""
            action2 = "cartas_sospechadas_fail"
            action3 = ""
            action4 = "mensaje_sistema"
            data1 = ""
            data2 = {
                "nombre_sospechador": jugador.apodo,
                "cartas_sospechadas": [recinto, carta_monstruo, carta_victima],
            }
            data3 = ""
            data4 = f"El jugador {jugador.apodo} sospecho de las siguientes cartas: {recinto}, {carta_monstruo} y {carta_victima}. Ninguno de los jugadores tiene alguna de esas cartas."
            personal_message = {"action": action1, "data": data1}
            to_broadcast = {"action": action2, "data": data2}
            message_to = {
                "action": action3,
                "data": data3,
                "id_jugador": -1,
            }
            system = {"action": action4, "data": data4}
        else:
            partida.jugador_que_sospecha = jugador
            jugador.estado_turno = "F"
            jugador_que_muestra.estado_turno = "MS"
            action1 = ""
            action2 = "cartas_sospechadas"
            action3 = "muestra"
            data1 = ""
            data2 = {
                "nombre_sospechador": jugador.apodo,
                "nombre_sospechoso": jugador_que_muestra.apodo, 
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
    elif jugador.orden_turno != partida.jugador_en_turno:
        action1 = "error_imp"
        data1 = {"message": "No es tu turno"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {
            "action": "",
            "data": "",
            "id_jugador": -1,
        }
    elif jugador.estado_turno != "SA":
        action1 = "error_imp"
        data1 = {"message": "No estas en la etapa de sospechar o anunciar"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {"action": "", "data": "", "id_jugador": -1}
    elif jugador.posicion not in RECINTOS.keys():
        action1 = "error_imp"
        action2 = ""
        action3 = ""
        data1 = {"message": "No estas en un recinto"}
        data2 = ""
        data3 = ""
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
        "system": system,
    }


def responder_sospecha(jugador, carta):
    if jugador.estado_turno == "MS":
        partida = jugador.partida
        action1 = "no_carta"
        action2 = ""
        action3 = ""
        data1 = {"message": "No tienes esa carta para mostrar"}
        data2 = ""
        data3 = ""
        cartas = []
        jugador.estado_turno = "N"
        for c in jugador.cartas:
            cartas.append(c.nombre)
        if carta in cartas:
            action1 = "muestra_carta"
            data1 = {}
            action2 = "sospecha_respondida"
            data2 = {"nombre_jugador": jugador.apodo}
            action3 = "carta_seleccionada"
            data3 = {"carta_seleccionada": carta}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {
            "action": action3,
            "data": data3,
            "id_jugador": partida.jugador_que_sospecha.id_jugador,
        }
    elif jugador.estado_turno != "MS":
        action1 = "error_imp"
        data1 = {"message": "No estas en la etapa de mostrar carta en sospecha"}
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": "", "data": ""}
        message_to = {"action": "", "data": "", "id_jugador": -1}

    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
    }


@pony.db_session()
def acusar(jugador, partida, carta_monstruo, carta_victima, carta_recinto):
    if (
        jugador.orden_turno == partida.jugador_en_turno
        and jugador.estado_turno == "SA"
        and not jugador.acuso
    ):
        respuesta_personal = {"action": "acuse", "data": ""}
        respuesta_broadcast = {"action": "acuso", "data": ""}
        respuesta_to = {"id_jugador": "", "action": "", "data": ""}
        gano = comprobar_cartas_sobre(
            partida, [carta_monstruo, carta_victima, carta_recinto]
        )
        if gano:
            respuesta_personal["data"] = {"message": "ganaste"}
            respuesta_broadcast["data"] = {
                "ganador": jugador.apodo,
                "monstruo_en_sobre": carta_monstruo,
                "victima_en_sobre": carta_victima,
                "recinto_en_sobre": carta_recinto,
            }
            jugador.ganador = True
        else:
            respuesta_pasar_turno = pasar_turno(jugador, partida)
            respuesta_personal["data"] = {
                "message": "perdiste",
                "monstruo_en_sobre": partida.monstruo_en_sobre().nombre,
                "victima_en_sobre": partida.victima_en_sobre().nombre,
                "recinto_en_sobre": partida.recinto_en_sobre().nombre,
            }
            respuesta_broadcast["data"] = {
                "perdedor": jugador.apodo,
                "lista_jugadores": lista_estado_jugadores(partida),
                "jugador_sig_turno": respuesta_pasar_turno["to_broadcast"]["data"][
                    "nombre_jugador"
                ],
                "monstruo_acusado": carta_monstruo,
                "victima_acusado": carta_victima,
                "recinto_acusado": carta_recinto,
            }
            respuesta_to = respuesta_pasar_turno["message_to"]
        jugador.estado_turno = "N"
        jugador.acuso = True
    elif jugador.orden_turno != partida.jugador_en_turno:
        respuesta_personal = {
            "action": "error_imp",
            "data": {"message": "No es tu turno"},
        }
        respuesta_broadcast = {"action": "", "data": ""}
        respuesta_to = {"action": "", "data": "", "id_jugador": 0}
    elif jugador.estado_turno != "SA":
        action1 = "error_imp"
        data1 = {"message": "No estas en la etapa de sospechar o anunciar"}
        respuesta_personal = {"action": action1, "data": data1}
        respuesta_broadcast = {"action": "", "data": ""}
        respuesta_to = {"action": "", "data": "", "id_jugador": -1}
    elif jugador.acuso:
        action1 = "error_imp"
        data1 = {"message": "Ya acusaste previamente"}
        respuesta_personal = {"action": action1, "data": data1}
        respuesta_broadcast = {"action": "", "data": ""}
        respuesta_to = {"action": "", "data": "", "id_jugador": -1}
    return {
        "personal_message": respuesta_personal,
        "to_broadcast": respuesta_broadcast,
        "message_to": respuesta_to,
    }


@pony.db_session()
def comprobar_cartas_sobre(partida, cartas_acusadas):
    if len(cartas_acusadas) != 3:
        return False
    for c in partida.sobre:
        if c.nombre not in cartas_acusadas:
            return False
    return True


@pony.db_session()
def estado_jugadores(partida):
    lista = lista_estado_jugadores(partida)
    respuesta_personal = {
        "action": "estado_jugadores",
        "data": {"lista_jugadores": lista},
    }
    return {"personal_message": respuesta_personal}


@pony.db_session()
def lista_estado_jugadores(partida):
    lista = []
    for jugador in partida.jugadores:
        lista.append(
            {
                "id_jugador": jugador.id_jugador,
                "apodo": jugador.apodo,
                "color": jugador.color,
                "posicion": jugador.posicion,
                "orden": jugador.orden_turno,
                "estado_turno": jugador.estado_turno,
                "en_turno": jugador.orden_turno == partida.jugador_en_turno,
            }
        )
    return lista
