import pony.orm as pony

from models import db
from services.board_functions import posiciones_posibles_a_mover
from services.start_game import asignar_posiciones_iniciales, asignar_colores
from board.board import PUERTAS, COLORES


def test_posiciones_posibles_a_mover():
    assert posiciones_posibles_a_mover(83, 1) == [81, 83]
    assert posiciones_posibles_a_mover(69, 2) == [67, 68, 69]
    assert posiciones_posibles_a_mover(58, 3) == [48, 55, 56, 57, 58, 59, 60, 61, 71, 72]

def test_posiciones_posibles_a_mover_casilla_especial():
    assert posiciones_posibles_a_mover(10, 2) == [1, 6, 8, 10, 12, 14, 71]
    assert posiciones_posibles_a_mover(54, 1) == [53, 54, 55, 65]

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


@pony.db_session
def test_estado_turno_front():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida para estado turno", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    j1.estado_turno = "SA"
    j1.posicion = 39
    j2.estado_turno = "N"
    pony.commit()

    assert j1.estado_turno_front() == "SA"
    assert j2.estado_turno_front() == "N"
    j1.posicion = 40
    assert j1.estado_turno_front() == "A"