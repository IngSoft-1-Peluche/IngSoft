import pony.orm as pony

from models import db
from services.start_game import iniciar_partida_service, mostrar_cartas


@pony.db_session
def test_distribuir_cartas():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida de juan", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    iniciar_partida_service(p1)
    pony.commit()

    assert len(p1.cartas) == 21
    assert len(p1.sobre) == 3
    assert len(j1.cartas) + len(j2.cartas) + len(j3.cartas) + len(p1.sobre) == len(
        p1.cartas
    )
    assert abs(len(j1.cartas) - len(j2.cartas)) < 2
    assert abs(len(j1.cartas) - len(j3.cartas)) < 2
    assert abs(len(j2.cartas) - len(j3.cartas)) < 2


@pony.db_session
def test_mostrar_cartas():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida de juan", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    iniciar_partida_service(p1)
    pony.commit()

    assert mostrar_cartas(j1)['personal_message']['data']['cartas'] == [c.nombre for c in j1.cartas]
    assert mostrar_cartas(j2)['personal_message']['data']['cartas'] == [c.nombre for c in j2.cartas]
    assert mostrar_cartas(j3)['personal_message']['data']['cartas'] == [c.nombre for c in j3.cartas]
