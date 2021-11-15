from backend.services.start_game import iniciar_partida_service
import pony.orm as pony
from start_game import iniciar_partida_service

def jugador_conectado_lobby(jugador, partida):
    jugadores = []
    for j in partida.jugadores:
        jugadores.append(j.apodo)
    action1 = ""
    action2 = "nuevo_jugador"
    action3 = ""
    data1 = ""
    data2 = {"jugador_conectado": jugador.apodo, "id_partida": partida.id_partida, "nombre_partida": partida.nombre, "jugadores": jugadores}
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

def jugador_desconectado_lobby(jugador, partida):
    jugadores = []
    for j in partida.jugadores:
        jugadores.append(j.apodo)
    action1 = ""
    action2 = "jugador_desconectado_lobby"
    action3 = ""
    data1 = ""
    data2 = {"jugador_desconectado": jugador.apodo, "id_partida": partida.id_partida, "nombre_partida": partida.nombre, "jugadores": jugadores}
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

def escribir_chat(jugador, mensage):
    action1 = ""
    action2 = "escribio_chat"
    action3 = ""
    data1 = ""
    data2 = {"nombre_jugador": jugador.apodo, "message": mensage}
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

def iniciar_partida_lobby(jugador, partida):
    with pony.db_session:
        action1 = ""
        action2 = ""
        action3 = ""
        data1 = ""
        data2 = ""
        data3 = ""
        if (
            partida.iniciada == False
            and 1 < len(partida.jugadores) < 7
            and jugador.id_jugador == partida.creador.id_jugador
        ):
            iniciar_partida_service(partida)
            action2 = "inciada"
            data2 = {}
        elif partida.iniciada == True:
            action1 = "error_imp"
            data1 = {"message": "La partida ya está iniciada"}
        elif jugador.id_jugador != partida.creador.id_jugador:
            action1 = "error_imp"
            data1 = {"message": "No eres el dueño de la partida"}
        else:
            action1 = "error_imp"
            data1 = {"message": "La partida no cumple con la cantidad de jugadores necesarios para iniciarse"}
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