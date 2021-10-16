from fastapi.testclient import TestClient
import pony.orm as pony
from fastapi import status

from main import app
from main import Partida , Jugadores

client = TestClient(app)

def test_get_home_page():
    response = client.get("/home")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message":"Project home Grupo Peluche"}

def test_database():
    with pony.db_session:
        j1 = Jugadores(apodo='juan')
        p1 = Partida(nombre='Partida de juan', iniciada=True, creador=j1)
        j1.partida = p1 
        j2 = Jugadores(apodo='maria')
        j2.partida = p1

        pony.commit()#Es necesario realizar los commit para que se guarden las entidades en la base y se les asigne un id
        assert p1.nombre == 'Partida de juan'
        assert p1.iniciada == True
        assert p1 in j1.creador_de
        assert j1 in p1.jugadores
        assert p1.jugador_en_turno == None
        assert j1.orden_turno == None
        assert j1 in p1.jugadores and j2 in p1.jugadores
        assert j1.id_jugador != j2.id_jugador
        assert j2.creador_de == []
