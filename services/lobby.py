import pony.orm as pony

def jugador_conectado(jugador, partida):
    action1 = ""
    action2 = "nuevo_jugador"
    action3 = ""
    data1 = ""
    data2 = {"id_partida": partida.id_partida, "nombre_partida": partida.nombre, "id_jugador": jugador.id_jugador, "nombre_jugador": jugador.apodo}
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