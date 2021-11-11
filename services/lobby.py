import pony.orm as pony

def jugador_conectado(jugador, partida):
    jugadores = []
    for j in partida.jugadores:
        jugadores.add(j.apodo)
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