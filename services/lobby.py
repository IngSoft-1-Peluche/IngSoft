import pony.orm as pony
from models import db

def jugador_conectado(jugador, partida):
    action1 = ""
    action2 = "nuevo_jugador"
    action3 = ""
    data1 = ""
    data2 = {"nombre_partida": partida.nombre, "id_jugador": jugador.id_jugador, "nombre_jugador": jugador.apodo}
    data3 = ""
    personal_message = {"action": action1, "data": data1}
    to_broadcast = {"action": action2, "data": data2}
    message_to = {
        "action": action3,
        "data": data3,
        "id_jugador": -1,
    }