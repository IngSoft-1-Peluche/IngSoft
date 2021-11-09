import pony.orm as pony

from models import db
from services.board_functions import posiciones_posibles_a_mover
from services.start_game import asignar_posiciones_iniciales, asignar_colores
from board.board import PUERTAS, COLORES


def test_posiciones_posibles_a_mover():
    assert posiciones_posibles_a_mover(83, 1) == [81]
    assert posiciones_posibles_a_mover(69, 2) == [67, 69]
    assert posiciones_posibles_a_mover(58, 3) == [48, 55, 57, 59, 61, 71, 72]

@pony.db_session
def test_posiciones_iniciales():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida para posiciones iniciales", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    asignar_posiciones_iniciales(p1)
    pony.commit()

    for jugador in p1.jugadores:
        assert jugador.posicion in PUERTAS

@pony.db_session
def test_posiciones_iniciales():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida para colores", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    asignar_colores(p1)
    pony.commit()

    assert j1.color != j2.color
    assert j1.color != j3.color
    assert j2.color != j3.color
    for jugador in p1.jugadores:
        assert jugador.color in COLORES