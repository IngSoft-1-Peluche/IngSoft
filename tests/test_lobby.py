import pony.orm as pony
from services.start_game import iniciar_partida_service
from services.lobby import iniciar_partida_lobby
from services.board_functions import posiciones_posibles_a_mover
from models import Partida, Jugador, db

@pony.db_session
def test_iniciar_partida_lobby():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Mi partida", iniciada=False, creador=j1)
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


