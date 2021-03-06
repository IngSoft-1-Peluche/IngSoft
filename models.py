import pony.orm as pony
from fastapi import HTTPException

from board.board import RECINTOS, TRAMPAS

ESTADOS_TURNO_JUGADOR = {
    "N": "No tiene turno",
    "D": "Tirar Dado",
    "M": "Mover",
    "SA": "Sospechar/Acusar",
    "EC": "Esperar carta",
    "F": "Fin de turno",
    "MS": "Mostrar sospecha",
}

db = pony.Database()

# implementación de clases
class Partida(db.Entity):
    id_partida = pony.PrimaryKey(int, auto=True)
    nombre = pony.Required(str)
    iniciada = pony.Required(bool, default=False)
    creador = pony.Required("Jugador", reverse="creador_de")
    jugadores = pony.Set("Jugador", reverse="partida")
    jugador_en_turno = pony.Optional(int, default=1)
    jugador_que_sospecha = pony.Optional("Jugador", reverse="sospecha")
    cartas = pony.Set("Carta", reverse="partida")
    sobre = pony.Set("Carta", reverse="sobre")
    se_jugo_bruja = pony.Required(bool, default=False)

    @pony.db_session()
    def cantidad_jugadores(self):
        return len(self.jugadores)

    @pony.db_session()
    def monstruo_en_sobre(self):
        for carta in self.sobre:
            if carta.tipo == "M":
                return carta

    @pony.db_session()
    def victima_en_sobre(self):
        for carta in self.sobre:
            if carta.tipo == "V":
                return carta

    @pony.db_session()
    def recinto_en_sobre(self):
        for carta in self.sobre:
            if carta.tipo == "R":
                return carta

    @pony.db_session()
    def siguiente_jugador(self, pasar_turno=False):
        t = True
        i = 0
        if all([j.en_trampa for j in self.jugadores]):
            if pasar_turno:
                for j in self.jugadores:
                    j.en_trampa = False
            while t:
                siguiente = (self.jugador_en_turno + i) % len(self.jugadores) + 1
                jugador_siguiente = next(
                    filter(lambda j: j.orden_turno == siguiente, self.jugadores)
                )
                t = jugador_siguiente.acuso
                i += 1
            return jugador_siguiente
        while t:
            siguiente = (self.jugador_en_turno + i) % len(self.jugadores) + 1
            jugador_siguiente = next(
                filter(lambda j: j.orden_turno == siguiente, self.jugadores)
            )
            t = jugador_siguiente.acuso or jugador_siguiente.en_trampa
            if pasar_turno:
                jugador_siguiente.en_trampa = False
            i += 1
        return jugador_siguiente

    @pony.db_session()
    def pasar_turno(self):
        self.jugador_en_turno = self.siguiente_jugador(pasar_turno=True).orden_turno

    @pony.db_session()
    def esta_terminada(self):
        return any([j.ganador for j in self.jugadores]) or all(
            [j.acuso for j in self.jugadores]
        )


class Jugador(db.Entity):
    id_jugador = pony.PrimaryKey(int, auto=True)
    apodo = pony.Required(str)
    orden_turno = pony.Optional(int)
    creador_de = pony.Optional("Partida", reverse="creador")
    partida = pony.Optional("Partida", reverse="jugadores")
    posicion = pony.Optional(int, default=2)
    ultima_tirada = pony.Optional(int)
    cartas = pony.Set("Carta", reverse="jugador")
    sospecha = pony.Optional("Partida", reverse="jugador_que_sospecha")
    color = pony.Optional(str)
    estado_turno = pony.Optional(str, default="N")
    acuso = pony.Required(bool, default=False)
    ganador = pony.Required(bool, default=False)
    en_trampa = pony.Required(bool, default=False)

    @pony.db_session()
    def asociar_a_partida(self, partida):
        partida.jugadores.add(self)

    @pony.db_session()
    def eliminar_de_partida(self, partida):
        partida.jugadores.remove(self)

    @pony.db_session()
    def cambiar_posicion(self, nueva_pos):
        self.posicion = nueva_pos
        if nueva_pos in TRAMPAS:
            self.en_trampa = True

    @pony.db_session()
    def estado_turno_front(self):
        if self.partida.esta_terminada():
            return "T"
        elif self.estado_turno == "SA" and self.posicion in RECINTOS.keys():
            return self.estado_turno
        elif self.estado_turno == "SA" and self.posicion not in RECINTOS.keys():
            return "A"
        else:
            return self.estado_turno


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
def get_partida(id_partida):
    try:
        return Partida[id_partida]
    except:
        raise HTTPException(status_code=500, detail="No existe la partida solicitada")


@pony.db_session()
def get_jugador(id_jugador):
    try:
        return Jugador[id_jugador]
    except:
        raise HTTPException(status_code=500, detail="No existe el jugador solicitado")


@pony.db_session()
def get_carta(id_carta):
    try:
        return Carta[id_carta]
    except:
        raise HTTPException(status_code=500, detail="No existe la carta solicitada")


@pony.db_session()
def crear_jugador(apodo):
    jugador = Jugador(apodo=apodo)
    pony.commit()
    return jugador


@pony.db_session()
def crear_partida(nombre, id_jugador):
    jugador = get_jugador(id_jugador)
    partida = Partida(nombre=nombre, creador=jugador.id_jugador)
    pony.commit()
    jugador.asociar_a_partida(partida)
    return partida
