import os
if os.path.exists("database.sqlite"):
    os.remove("database.sqlite")

from fastapi.testclient import TestClient
import pony.orm as pony
from fastapi import status

from main import app
from models import db

from .test_board import *
from .test_cards import *
from .test_acusar import *
from .test_in_game import *
from .test_lobby import *

client = TestClient(app)


def test_get_home_page():
    response = client.get("/home")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Project home Grupo Peluche"}


@pony.db_session
def test_database():
    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    pony.flush()
    p1 = db.Partida(nombre="Partida de juan", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    pony.commit()

    assert p1.nombre == "Partida de juan"
    assert p1.iniciada == False
    assert p1 == j1.creador_de
    assert j1 in p1.jugadores
    assert p1.jugador_en_turno == 1
    assert j1.orden_turno == None
    assert j1 in p1.jugadores and j2 in p1.jugadores
    assert j1.id_jugador != j2.id_jugador
    assert j2.creador_de == None


@pony.db_session
def test_listar_partidas_endpoint():
    response = client.get("/partidas")
    partidas_json = response.json()
    partidas = [db.Partida[p["id_partida"]] for p in partidas_json]

    assert response.status_code == status.HTTP_200_OK
    assert all(p["cantidad_jugadores"] < 6 for p in partidas_json)
    assert all(not p.iniciada for p in partidas)


@pony.db_session
def test_post_crear_partida():
    response = client.post("/partidas/")
    response = client.post(
        "/partidas/",
        json={"nombre_partida": "nombre de mi partida", "apodo": "apodo de mi jugador"},
    )
    assert type(response.json()["id_jugador"]) == int
    assert type(response.json()["id_partida"]) == int
    assert response.json()["jugador_creador"] == True
    assert response.json()["apodo"] == "apodo de mi jugador"
    assert response.json()["nombre_partida"] == "nombre de mi partida"
    assert response.status_code == status.HTTP_201_CREATED
    jugador_creado = pony.select(
        c for c in db.Jugador if c.apodo == "apodo de mi jugador"
    )
    assert jugador_creado.first() != None
    assert jugador_creado.first().apodo == "apodo de mi jugador"


@pony.db_session
def test_detalle_partida_endpoint():
    partida = db.Partida.select().first()
    response = client.get("/partidas/%s" % partida.id_partida)
    partida_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert partida_json["id_partida"] == partida.id_partida
    assert "nombre" in partida_json.keys()
    assert "id_jugador" in partida_json["jugadores"][0].keys()
    assert "apodo" in partida_json["jugadores"][0].keys()
    assert "orden" in partida_json["jugadores"][0].keys()
    assert "en_turno" in partida_json["jugadores"][0].keys()


@pony.db_session
def test_unirse_a_partida():
    _response = client.post("/partidas/")
    _response = client.post(
        "/partidas/",
        json={"nombre_partida": "nombre de mi partida", "apodo": "apodo de mi jugador"},
    )
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "ultimo"})
    
    assert response.json()["id_partida"] == _response.json()["id_partida"]
    assert response.json()["nombre_partida"] == _response.json()["nombre_partida"]
    assert type(response.json()["id_jugador"]) == int
    assert response.json()["apodo"] == "ultimo"
    assert response.json()["jugador_creador"] == False

@pony.db_session
def test_unirse_a_partida_llena():
    _response = client.post("/partidas/")
    _response = client.post(
        "/partidas/",
        json={"nombre_partida": "partida llena", "apodo": "apodo de mi jugador"},
    )
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "segundo"})
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "tercero"})
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "cuarto"})
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "quinto"})
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "sexto"})
    response = client.put("/partidas/", json={"id_partida": _response.json()["id_partida"], "apodo": "afuera"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pony.db_session
def test_asignar_orden():
    from services.start_game import asignar_orden_aleatorio

    j1 = db.Jugador(apodo="juan")
    j2 = db.Jugador(apodo="maria")
    j3 = db.Jugador(apodo="pedro")
    pony.flush()
    p1 = db.Partida(nombre="Partida de juan", iniciada=False, creador=j1)
    j1.partida = p1
    j2.partida = p1
    j3.partida = p1
    asignar_orden_aleatorio(p1)
    pony.commit()

    n = len(p1.jugadores)
    ordenes = [j.orden_turno for j in p1.jugadores]
    assert set(range(1, n + 1)) == set(ordenes)

