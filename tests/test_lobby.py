import pony.orm as pony
from services.start_game import iniciar_partida_service
from services.lobby import iniciar_partida_lobby, jugador_conectado_lobby, escribir_chat
from services.board_functions import posiciones_posibles_a_mover
from models import Partida, Jugador, db


@pony.db_session
def test_jugador_conectado_lobby_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1

    respuesta = jugador_conectado_lobby(j2, p1)

    assert respuesta["personal_message"]["action"] == ""
    assert respuesta["personal_message"]["data"] == ""
    assert respuesta["to_broadcast"]["action"] == "nuevo_jugador"
    assert respuesta["to_broadcast"]["data"]["jugador_conectado"] == "j2"
    assert respuesta["to_broadcast"]["data"]["id_partida"] == p1.id_partida
    assert respuesta["to_broadcast"]["data"]["nombre_partida"] == p1.nombre
    assert type(respuesta["to_broadcast"]["data"]["jugadores"]) == type(
        [j1.apodo, j2.apodo]
    )
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""


@pony.db_session
def test_escribir_chat():
    j1 = db.Jugador(apodo="j1")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida", iniciada=False, creador=j1)
    j1.partida = p1

    respuesta = escribir_chat(j1, "Probando chat")

    assert respuesta["personal_message"]["action"] == ""
    assert respuesta["personal_message"]["data"] == ""
    assert respuesta["to_broadcast"]["action"] == "escribio_chat"
    assert respuesta["to_broadcast"]["data"]["nombre_jugador"] == j1.apodo
    assert respuesta["to_broadcast"]["data"]["message"] == "Probando chat"
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert respuesta["system"]["action"] == ""
    assert respuesta["system"]["data"] == ""


@pony.db_session
def test_iniciar_partida_lobby_vale():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida a iniciar", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    respuesta = iniciar_partida_lobby(j1, p1)

    assert respuesta["personal_message"]["action"] == ""
    assert respuesta["personal_message"]["data"] == ""
    assert respuesta["to_broadcast"]["action"] == "iniciada"
    assert respuesta["to_broadcast"]["data"] == {}
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert respuesta["system"]["action"] == ""
    assert respuesta["system"]["data"] == ""


@pony.db_session
def test_iniciar_partida_lobby_no_creador():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida a iniciar", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    respuesta = iniciar_partida_lobby(j2, p1)
    assert respuesta["personal_message"]["action"] == "error_imp"
    assert (
        respuesta["personal_message"]["data"]["message"]
        == "No eres el dueño de la partida"
    )
    assert respuesta["to_broadcast"]["action"] == ""
    assert respuesta["to_broadcast"]["data"] == ""
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert respuesta["system"]["action"] == ""
    assert respuesta["system"]["data"] == ""


@pony.db_session
def test_iniciar_partida_lobby_de_uno():
    j1 = db.Jugador(apodo="juan")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida a iniciar", iniciada=False, creador=j1)
    j1.partida = p1

    respuesta = iniciar_partida_lobby(j1, p1)
    assert respuesta["personal_message"]["action"] == "error_imp"
    assert (
        respuesta["personal_message"]["data"]["message"]
        == "La partida no cumple con la cantidad de jugadores necesarios para iniciarse"
    )
    assert respuesta["to_broadcast"]["action"] == ""
    assert respuesta["to_broadcast"]["data"] == ""
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert respuesta["system"]["action"] == ""
    assert respuesta["system"]["data"] == ""


@pony.db_session
def test_iniciar_partida_lobby_arrancada():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida a iniciar", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    _ = iniciar_partida_lobby(j1, p1)

    respuesta = iniciar_partida_lobby(j1, p1)
    assert respuesta["personal_message"]["action"] == "error_imp"
    assert (
        respuesta["personal_message"]["data"]["message"]
        == "La partida ya está iniciada"
    )
    assert respuesta["to_broadcast"]["action"] == ""
    assert respuesta["to_broadcast"]["data"] == ""
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert respuesta["system"]["action"] == ""
    assert respuesta["system"]["data"] == ""
