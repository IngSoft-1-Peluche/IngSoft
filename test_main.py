from fastapi.testclient import TestClient
import pony.orm as pony
from fastapi import status

from main import app
from models import db

client = TestClient(app)

def test_get_home_page():
    response = client.get("/home")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message":"Project home Grupo Peluche"}

@pony.db_session
def test_database():
    j1 = db.Jugador(apodo='juan')
    j2 = db.Jugador(apodo='maria')
    pony.flush()
    p1 = db.Partida(nombre='Partida de juan', iniciada=False, creador=j1)
    j1.partida = p1 
    j2.partida = p1

    pony.commit()#Es necesario realizar los commit para que se guarden las entidades en la base y se les asigne un id
    assert p1.nombre == 'Partida de juan'
    assert p1.iniciada == False
    assert p1 == j1.creador_de
    assert j1 in p1.jugadores
    assert p1.jugador_en_turno == None
    assert j1.orden_turno == None
    assert j1 in p1.jugadores and j2 in p1.jugadores
    assert j1.id_jugador != j2.id_jugador
    assert j2.creador_de == None

@pony.db_session
def test_listar_partidas_endpoint():
    response = client.get("/partidas")
    partidas_json = response.json()
    partidas = [db.Partida[p['id_partida']] for p in partidas_json]
    
    assert response.status_code == status.HTTP_200_OK
    assert all(p['cantidad_jugadores'] < 6 for p in partidas_json)
    assert all(not p.iniciada for p in partidas)

def test_post_crear_partida():
    response = client.post("/partidas/")
    response = client.post(
        "/partidas/",
        json={"nombre_partida": "foobar", "apodo": "Foo Bar"},
    )
    assert response.status_code == status.HTTP_201_CREATED