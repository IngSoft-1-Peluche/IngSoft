import pony.orm as pony

from models import db
from services.start_game import iniciar_partida_service
from services.in_game import acusar


@pony.db_session
def test_acusar():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida para acusar", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    iniciar_partida_service(p1)
    pony.commit()
    for carta in p1.sobre:
        if carta.tipo == "M":
            carta_monstruo = carta.nombre
        elif carta.tipo == "V":
            carta_victima = carta.nombre
        elif carta.tipo == "R":
            carta_recinto = carta.nombre
    
    for recinto in ["Alcoba", "Biblioteca"]:
        if carta_recinto != recinto:
            recinto_incorrecto = recinto
    
    for j in p1.jugadores:
        if j.orden_turno == p1.jugador_en_turno:
            jugador_turno = j
        else:
            jugador_no_turno = j
    respuesta_no_turno = acusar(jugador_no_turno, p1, carta_monstruo, carta_victima, carta_recinto)
    respuesta_correcta = acusar(jugador_turno, p1, carta_monstruo, carta_victima, carta_recinto)
    respuesta_incorrecta = acusar(jugador_turno, p1, carta_monstruo, carta_victima, recinto_incorrecto)
            

    assert respuesta_no_turno["personal_message"]["action"] == "error_imp"
    assert respuesta_no_turno["personal_message"]["data"]["message"] == "No es tu turno"
    assert respuesta_correcta["personal_message"]["action"] == "acuse"
    assert respuesta_correcta["personal_message"]["data"]["message"] == "ganaste"
    assert respuesta_correcta["to_broadcast"]["action"] == "acuso"
    assert respuesta_correcta["to_broadcast"]["data"]["ganador"] == jugador_turno.apodo
    assert respuesta_correcta["to_broadcast"]["data"]["monstruo_en_sobre"] == carta_monstruo
    assert respuesta_correcta["to_broadcast"]["data"]["victima_en_sobre"] == carta_victima
    assert respuesta_correcta["to_broadcast"]["data"]["recinto_en_sobre"] == carta_recinto
    assert respuesta_incorrecta["personal_message"]["action"] == "acuse"
    assert respuesta_incorrecta["personal_message"]["data"]["message"] == "perdiste"
    assert respuesta_incorrecta["personal_message"]["data"]["monstruo_en_sobre"] == carta_monstruo
    assert respuesta_incorrecta["personal_message"]["data"]["victima_en_sobre"] == carta_victima
    assert respuesta_incorrecta["personal_message"]["data"]["recinto_en_sobre"] == carta_recinto
    assert respuesta_incorrecta["to_broadcast"]["action"] == "acuso"
    assert respuesta_incorrecta["to_broadcast"]["data"]["perdedor"] == jugador_turno.apodo
    assert respuesta_incorrecta["to_broadcast"]["data"]["monstruo_acusado"] == carta_monstruo
    assert respuesta_incorrecta["to_broadcast"]["data"]["victima_acusado"] == carta_victima
    assert respuesta_incorrecta["to_broadcast"]["data"]["recinto_acusado"] == recinto_incorrecto
