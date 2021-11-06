import pony.orm as pony
import random

db = pony.Database()

# implementación de clases
class Partida(db.Entity):
    id_partida = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    iniciada = pony.Required(bool, default=False)
    creador = pony.Required("Jugador", reverse="creador_de")
    jugadores = pony.Set("Jugador", reverse="partida")
    jugador_en_turno = pony.Optional(int, default=1)
    cartas = pony.Set("Carta", reverse="partida")
    sobre = pony.Set("Carta", reverse="sobre")

    @pony.db_session()
    def cantidad_jugadores(self):
        return len(self.jugadores)


class Jugador(db.Entity):
    id_jugador = pony.PrimaryKey(int, auto=True)
    apodo = pony.Required(str)
    orden_turno = pony.Optional(int)
    creador_de = pony.Optional("Partida", reverse="creador")
    partida = pony.Optional("Partida", reverse="jugadores")
    posicion = pony.Optional(int)
    ultima_tirada = pony.Optional(int)
    cartas = pony.Set("Carta", reverse="jugador")

    @pony.db_session()
    def asociar_a_partida(self, partida):
        partida.jugadores.add(self)
    
    @pony.db_session()
    def cambiar_posicion(self, nueva_pos):
        self.posicion = nueva_pos



class Carta(db.Entity):
    id_carta = pony.PrimaryKey(int, auto=True)
    partida = pony.Optional("Partida", reverse="cartas")
    nombre = pony.Required(str)
    tipo = pony.Required(str)
    jugador = pony.Optional("Jugador", reverse="cartas")
    sobre = pony.Optional("Partida", reverse="sobre")


# línea que sirve para debug
pony.set_sql_debug(True)

# creación de tablas para los modelos
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

# implementación de funciones
@pony.db_session()
def crear_jugador(apodo):
    jugador = Jugador(apodo=apodo)
    return jugador


@pony.db_session()
def crear_partida(nombre, id_jugador):
    jugador = Jugador[id_jugador]
    partida = Partida(nombre=nombre, creador=jugador.id_jugador)
    jugador.asociar_a_partida(partida)
    return partida


