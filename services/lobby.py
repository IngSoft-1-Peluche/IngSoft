import pony.orm as pony
from .start_game import iniciar_partida_service
from models import Jugador


def jugador_conectado_lobby(jugador, partida):
    jugadores = []
    for j in partida.jugadores:
        jugadores.append(j.apodo)
    action1 = ""
    action2 = "nuevo_jugador"
    action3 = ""
    data1 = ""
    data2 = {
        "jugador_conectado": jugador.apodo,
        "id_partida": partida.id_partida,
        "nombre_partida": partida.nombre,
        "jugadores": jugadores,
    }
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
    }


@pony.db_session()
def jugador_desconectado_lobby(jugador, partida, manager):
    id_jugador = jugador.id_jugador
    if (partida.iniciada == False):
        jugador.eliminar_de_partida(partida)
        pony.commit()
    jugadores = []
    for j in partida.jugadores:
        jugadores.append(j.apodo)
    action1 = ""
    action2 = "jugador_desconectado_lobby"
    action3 = ""
    action4 = ""
    if (manager.count_id_jugador_websockets(id_jugador) == 0):
        action4 = "mensaje_sistema"
    data1 = ""
    data2 = {
        "jugador_desconectado": jugador.apodo,
        "id_partida": partida.id_partida,
        "nombre_partida": partida.nombre,
        "jugadores": jugadores,
    }
    data3 = ""
    data4 = ""
    if (manager.count_id_jugador_websockets(id_jugador) == 0):
        data4 = {"message": f"El jugador {jugador.apodo} se desconecto de la partida"}
    personal_message = {"action": action1, "data": data1}
    to_broadcast = {"action": action2, "data": data2}
    message_to = {
        "action": action3,
        "data": data3,
        "id_jugador": -1,
    }
    system = {"action": action4, "data": data4}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
        "system": system,
    }


def escribir_chat(jugador, message):
    action1 = ""
    action2 = "escribio_chat"
    action3 = ""
    action4 = ""
    data1 = ""
    data2 = {"nombre_jugador": jugador.apodo, "message": message}
    data3 = ""
    data4 = ""
    personal_message = {"action": action1, "data": data1}
    to_broadcast = {"action": action2, "data": data2}
    message_to = {
        "action": action3,
        "data": data3,
        "id_jugador": -1,
    }
    system = {"action": action4, "data": data4}
    return {
        "personal_message": personal_message,
        "to_broadcast": to_broadcast,
        "message_to": message_to,
        "system": system,
    }


def iniciar_partida_lobby(jugador, partida):
    with pony.db_session:
        action1 = ""
        action2 = ""
        action3 = ""
        action4 = ""
        data1 = ""
        data2 = ""
        data3 = ""
        data4 = ""
        if (
            partida.iniciada == False
            and 1 < len(partida.jugadores) < 7
            and jugador.id_jugador == partida.creador.id_jugador
        ):
            iniciar_partida_service(partida)
            action2 = "iniciada"
            data2 = {}
        elif partida.iniciada == True:
            action1 = "error_imp"
            data1 = {"message": "La partida ya está iniciada"}
        elif jugador.id_jugador != partida.creador.id_jugador:
            action1 = "error_imp"
            data1 = {"message": "No eres el dueño de la partida"}
        else:
            action1 = "error_imp"
            data1 = {
                "message": "La partida no cumple con la cantidad de jugadores necesarios para iniciarse"
            }
        personal_message = {"action": action1, "data": data1}
        to_broadcast = {"action": action2, "data": data2}
        message_to = {
            "action": action3,
            "data": data3,
            "id_jugador": -1,
        }
        system = {"action": action4, "data": data4}
        return {
            "personal_message": personal_message,
            "to_broadcast": to_broadcast,
            "message_to": message_to,
            "system": system,
        }
