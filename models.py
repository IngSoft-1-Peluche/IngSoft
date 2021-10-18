import pony.orm as pony

db = pony.Database()

class Partida(db.Entity):
    id_partida = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    iniciada = pony.Required(bool, default=False)
    creador = pony.Required("Jugador", reverse='creador_de')
    jugadores = pony.Set("Jugador", reverse='partida')
    jugador_en_turno = pony.Optional(int)

class Jugador(db.Entity):
    id_jugador = pony.PrimaryKey(int, auto=True)
    apodo = pony.Required(str)
    orden_turno = pony.Optional(int)
    creador_de = pony.Set("Partida", reverse='creador')
    partida = pony.Set("Partida", reverse='jugadores')


db.bind('sqlite', 'database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
