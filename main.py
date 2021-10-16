from fastapi import FastAPI, status
import pony.orm as pony

db = pony.Database()

class Partida(db.Entity):
    id_partida = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    iniciada = pony.Required(bool) 
    creador = pony.Required("Jugadores", reverse='creador_de')
    jugadores = pony.Set("Jugadores", reverse='partida')
    jugador_en_turno = pony.Optional(int)

class Jugadores(db.Entity):
    id_jugador = pony.PrimaryKey(int, auto=True)
    apodo = pony.Required(str)
    orden_turno = pony.Optional(int)
    creador_de = pony.Set("Partida", reverse='creador')
    partida = pony.Set("Partida", reverse='jugadores')


db.bind('sqlite', 'database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

app = FastAPI()

@app.get("/home")
async def home():
    return {"message" : "Project home Grupo Peluche"}
