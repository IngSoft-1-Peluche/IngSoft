import pony.orm as pony

from .base import db

# implementación de clases
class Jugador(db.Entity):
    id_jugador = pony.PrimaryKey(int, auto=True)
    apodo = pony.Required(str)
    orden_turno = pony.Optional(int)
    creador_de = pony.Optional("Partida", reverse="creador")
    partida = pony.Optional("Partida", reverse="jugadores")

    def asociar_a_partida(self, partida):
        asociar_a_partida(partida, self)

# implementación de funciones
@pony.db_session()
def crear_jugador(apodo):
    jugador = Jugador(apodo=apodo)
    return jugador

@pony.db_session()
def asociar_a_partida(partida, jugador):
    partida.jugadores.add(jugador)
