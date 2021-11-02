import pony.orm as pony

from .base import db

# implementación de clases
class Partida(db.Entity):
    id_partida = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    iniciada = pony.Required(bool, default=False)
    creador = pony.Required("Jugador", reverse="creador_de")
    jugadores = pony.Set("Jugador", reverse="partida")
    jugador_en_turno = pony.Optional(int, default=1)

@pony.db_session()
def crear_partida(nombre, jugador):
    partida = Partida(nombre=nombre, creador=jugador.id_jugador)
    jugador.asociar_a_partida(partida)
    return partida
