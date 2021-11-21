import pony.orm as pony
from services.start_game import iniciar_partida_service
from services.in_game import (
    estado_jugadores,
    numero_dado,
    pasar_turno,
    jugador_esta_en_turno,
    tirar_dado,
    mover_jugador,
    anunciar_sospecha,
    responder_sospecha,
)
from services.board_functions import posiciones_posibles_a_mover
from models import Partida, Jugador, db


@pony.db_session
def test_siguiente_jugador_de_a_2():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    jugador_siguiente = mi_partida_de_2.siguiente_jugador()
    assert jugador_siguiente == j1


@pony.db_session
def test_siguiente_jugador_de_a_6():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    j4 = db.Jugador(apodo="j4")
    j5 = db.Jugador(apodo="j5")
    j6 = db.Jugador(apodo="j6")
    pony.flush()
    mi_partida_de_6 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_6)
    j2.asociar_a_partida(mi_partida_de_6)
    j3.asociar_a_partida(mi_partida_de_6)
    j4.asociar_a_partida(mi_partida_de_6)
    j5.asociar_a_partida(mi_partida_de_6)
    j6.asociar_a_partida(mi_partida_de_6)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j4.orden_turno = 4
    j5.orden_turno = 5
    j6.orden_turno = 6
    mi_partida_de_6.jugador_en_turno = 6
    pony.commit()
    jugador_siguiente = mi_partida_de_6.siguiente_jugador()
    assert jugador_siguiente == j1


@pony.db_session
def test_siguiente_jugador_salteando():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    j4 = db.Jugador(apodo="j4")
    j5 = db.Jugador(apodo="j5")
    j6 = db.Jugador(apodo="j6")
    pony.flush()
    mi_partida_de_6 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_6)
    j2.asociar_a_partida(mi_partida_de_6)
    j3.asociar_a_partida(mi_partida_de_6)
    j4.asociar_a_partida(mi_partida_de_6)
    j5.asociar_a_partida(mi_partida_de_6)
    j6.asociar_a_partida(mi_partida_de_6)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j4.orden_turno = 4
    j5.orden_turno = 5
    j6.orden_turno = 6
    mi_partida_de_6.jugador_en_turno = 6
    j1.acuso = True
    j2.acuso = True
    pony.commit()
    jugador_siguiente = mi_partida_de_6.siguiente_jugador()
    assert jugador_siguiente == j3


@pony.db_session
def test_pasar_turno():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    mi_partida_de_2.jugador_en_turno = 2
    j2.estado_turno = "F"
    respuesta = pasar_turno(j2, mi_partida_de_2)
    pony.commit()
    assert mi_partida_de_2.jugador_en_turno == 1
    assert respuesta["personal_message"]["action"] == ""
    assert respuesta["personal_message"]["data"] == ""
    assert respuesta["to_broadcast"]["action"] == "terminaron_turno"
    assert respuesta["to_broadcast"]["data"]["nombre_jugador"] == j1.apodo
    assert "lista_jugadores" in respuesta["to_broadcast"]["data"].keys()
    assert respuesta["message_to"]["action"] == "tu_turno"
    assert respuesta["message_to"]["data"] == ""
    assert respuesta["message_to"]["id_jugador"] == j1.id_jugador
    assert j2.estado_turno == "N"


@pony.db_session
def test_jugador_esta_en_turno():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    assert jugador_esta_en_turno(j1, mi_partida_de_2) == False
    assert jugador_esta_en_turno(j2, mi_partida_de_2) == True


@pony.db_session
def test_tirar_dado_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j2.posicion = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    j2.estado_turno = "D"
    respuesta = tirar_dado(j2, mi_partida_de_2)

    assert respuesta["personal_message"]["action"] == "tire_dado"
    assert type(respuesta["personal_message"]["data"]["numero_dado"]) == int
    assert 0 < respuesta["personal_message"]["data"]["numero_dado"] < 7
    assert respuesta["personal_message"]["data"]["casillas_a_mover"] != None
    assert respuesta["to_broadcast"]["action"] == "tiraron_dado"
    assert respuesta["to_broadcast"]["data"]["nombre_jugador"] == j2.apodo
    assert 0 < respuesta["to_broadcast"]["data"]["numero_dado"] < 7
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert type(respuesta["message_to"]["id_jugador"]) == int
    assert j2.estado_turno == "M"


@pony.db_session
def test_tirar_dado_no_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    estado_jugador = j1.estado_turno
    respuesta = tirar_dado(j1, mi_partida_de_2)
    assert respuesta["personal_message"]["action"] == "error_imp"
    assert respuesta["personal_message"]["data"]["message"] == "No es tu turno"
    assert respuesta["to_broadcast"]["action"] == ""
    assert respuesta["to_broadcast"]["data"] == ""
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert type(respuesta["message_to"]["id_jugador"]) == int
    assert j1.estado_turno == estado_jugador


@pony.db_session
def test_mover_jugador_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j1.posicion = 1
    j2.posicion = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    j2.estado_turno = "D"
    _ = tirar_dado(j2, mi_partida_de_2)
    posibles_casillas = posiciones_posibles_a_mover(j2.posicion, j2.ultima_tirada)
    respuesta = mover_jugador(j2, posibles_casillas[0])
    assert (j2.posicion in posibles_casillas) == True
    assert respuesta["personal_message"]["action"] == "me_movi"
    assert respuesta["personal_message"]["data"]["posicion_final"] == j2.posicion
    assert respuesta["to_broadcast"]["action"] == "se_movio"
    assert respuesta["to_broadcast"]["data"]["nombre_jugador"] == j2.apodo
    assert respuesta["to_broadcast"]["data"]["posicion_final"] == j2.posicion
    assert "lista_jugadores" in respuesta["to_broadcast"]["data"].keys()
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert type(respuesta["message_to"]["id_jugador"]) == int
    assert j2.estado_turno == "SA"


@pony.db_session
def test_mover_jugador_no_turno():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j1.posicion = 1
    j2.posicion = 2
    j1.ultima_tirada = numero_dado()
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    respuesta = mover_jugador(j1, 1)
    assert respuesta["personal_message"]["action"] == "error_imp"
    assert respuesta["personal_message"]["data"]["message"] == "No es tu turno"
    assert respuesta["to_broadcast"]["action"] == ""
    assert respuesta["to_broadcast"]["data"] == ""
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert type(respuesta["message_to"]["id_jugador"]) == int
    assert j1.estado_turno == "N"


@pony.db_session
def test_mover_jugador_no_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j1.posicion = 1
    j2.posicion = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    j2.estado_turno = "D"
    _ = tirar_dado(j2, mi_partida_de_2)
    posibles_casillas = posiciones_posibles_a_mover(j2.posicion, j2.ultima_tirada)
    respuesta = mover_jugador(j2, 100)
    assert respuesta["personal_message"]["action"] == "casilla_invalida"
    assert (
        respuesta["personal_message"]["data"]["message"] == "No es una posicion valida"
    )
    assert respuesta["to_broadcast"]["action"] == ""
    assert respuesta["to_broadcast"]["data"] == ""
    assert respuesta["message_to"]["action"] == ""
    assert respuesta["message_to"]["data"] == ""
    assert type(respuesta["message_to"]["id_jugador"]) == int
    assert j2.estado_turno == "M"


@pony.db_session
def test_mover_a_trampa():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j1.posicion = 2
    j2.posicion = 2
    mi_partida_de_2.jugador_en_turno = 2
    pony.commit()
    j2.estado_turno = "M"
    j2.ultima_tirada = 6
    _ = mover_jugador(j2, 22)
    assert j2.en_trampa == True
    assert mi_partida_de_2.siguiente_jugador() == j1
    mi_partida_de_2.pasar_turno()
    assert mi_partida_de_2.siguiente_jugador() == j1
    mi_partida_de_2.pasar_turno()
    assert mi_partida_de_2.siguiente_jugador() == j2


@pony.db_session
def test_anunciar_sospecha_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    carta1 = db.Carta(nombre="carta_prueba_1", tipo="M")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j3.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j1.posicion = 1
    j2.posicion = 2
    j2.posicion = 3
    j3.cartas.add(carta1)
    mi_partida_de_2.jugador_en_turno = 1
    pony.commit()
    j1.estado_turno = "SA"
    respuesta = anunciar_sospecha(j1, "carta_prueba_1", "carta_prueba_2")
    assert respuesta["message_to"]["action"] == "muestra"
    assert respuesta["message_to"]["id_jugador"] == j3.id_jugador
    assert j1.estado_turno == "EC"
    assert j3.estado_turno == "MS"


@pony.db_session
def test_anunciar_sospecha_no_turno():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    carta1 = db.Carta(nombre="carta_prueba_1", tipo="M")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j3.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j1.posicion = 1
    j2.posicion = 2
    j2.posicion = 3
    j3.cartas.add(carta1)
    mi_partida_de_2.jugador_en_turno = 1
    pony.commit()
    respuesta = anunciar_sospecha(j2, "carta_prueba_1", "carta_prueba_2")
    assert respuesta["personal_message"]["action"] == "error_imp"
    assert respuesta["personal_message"]["data"]["message"] == "No es tu turno"
    assert j2.estado_turno == "N"


@pony.db_session
def test_anunciar_sospecha_fail():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    carta1 = db.Carta(nombre="carta_prueba_1", tipo="M")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j3.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j1.posicion = 1
    j2.posicion = 2
    j2.posicion = 3
    j3.cartas.add(carta1)
    mi_partida_de_2.jugador_en_turno = 1
    pony.commit()
    j1.estado_turno = "SA"
    respuesta = anunciar_sospecha(j1, "carta_prueba_3", "carta_prueba_2")
    assert respuesta["to_broadcast"]["action"] == "cartas_sospechadas_fail"
    assert respuesta["to_broadcast"]["data"]["nombre_sospechador"] == j1.apodo
    assert respuesta["to_broadcast"]["data"]["cartas_sospechadas"] == [
        "Cochera",
        "carta_prueba_3",
        "carta_prueba_2",
    ]
    assert j1.estado_turno == "F"


@pony.db_session
def test_responder_sospecha_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    carta1 = db.Carta(nombre="carta_prueba_1", tipo="M")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j3.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j1.posicion = 1
    j2.posicion = 2
    j2.posicion = 3
    j3.cartas.add(carta1)
    mi_partida_de_2.jugador_en_turno = 1
    j1.estado_turno = "SA"
    _ = anunciar_sospecha(j1, "carta_prueba_1", "carta_prueba_2")
    pony.commit()
    respuesta = responder_sospecha(j3, "carta_prueba_1")
    pony.commit()
    assert respuesta["message_to"]["action"] == "carta_seleccionada"
    assert respuesta["message_to"]["data"]["carta_seleccionada"] == "carta_prueba_1"
    assert respuesta["message_to"]["id_jugador"] == j1.id_jugador
    assert j1.estado_turno == "F"


@pony.db_session
def test_responder_sospecha_no_vale():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    carta1 = db.Carta(nombre="carta_prueba_1", tipo="M")
    pony.flush()
    mi_partida_de_2 = db.Partida(nombre="mi_partida", creador=j1.id_jugador)
    j1.asociar_a_partida(mi_partida_de_2)
    j2.asociar_a_partida(mi_partida_de_2)
    j3.asociar_a_partida(mi_partida_de_2)
    j1.orden_turno = 1
    j2.orden_turno = 2
    j3.orden_turno = 3
    j1.posicion = 1
    j2.posicion = 2
    j2.posicion = 3
    j3.cartas.add(carta1)
    mi_partida_de_2.jugador_en_turno = 1
    j1.estado_turno = "SA"
    _ = anunciar_sospecha(j1, "carta_prueba_1", "carta_prueba_2")
    pony.commit()
    assert j3.estado_turno == "MS"
    respuesta = responder_sospecha(j3, "carta_prueba_2")
    pony.commit()
    assert respuesta["personal_message"]["action"] == "no_carta"
    assert (
        respuesta["personal_message"]["data"]["message"]
        == "No tienes esa carta para mostrar"
    )
    assert j3.estado_turno == "N"


@pony.db_session
def test_estado_jugadores():
    j1 = db.Jugador(apodo="j1")
    j2 = db.Jugador(apodo="j2")
    j3 = db.Jugador(apodo="j3")
    pony.flush()
    partida = db.Partida(nombre="Partida para estado jugadores", creador=j1)
    j1.asociar_a_partida(partida)
    j2.asociar_a_partida(partida)
    j3.asociar_a_partida(partida)
    iniciar_partida_service(partida)
    pony.commit()

    respuesta = estado_jugadores(partida)
    assert respuesta["personal_message"]["action"] == "estado_jugadores"
    assert len(respuesta["personal_message"]["data"]["lista_jugadores"]) == 3
    assert list(respuesta["personal_message"]["data"]["lista_jugadores"][0].keys()) == [
        "id_jugador",
        "apodo",
        "color",
        "posicion",
        "orden",
        "estado_turno",
        "en_turno",
    ]
