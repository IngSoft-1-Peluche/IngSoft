from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[(int, int, WebSocket)] = []

    async def connect(self, id_jugador: int, id_partida: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append((id_jugador, id_partida, websocket))

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection[2] == websocket:
                self.active_connections.remove(connection)

    async def send_message_to(self, action, data, id_jugador):
        if data != "":
            for connection in self.active_connections:
                if connection[0] == id_jugador:
                    await connection[2].send_json({"action": action, "data": data})

    async def send_personal_message(self, action, data, websocket: WebSocket):
        if data != "":
            await websocket.send_json({"action": action, "data": data})

    async def broadcast(self, action, data, id_partida):
        if data != "":
            for connection in self.active_connections:
                if connection[1] == id_partida:
                    await connection[2].send_json({"action": action, "data": data})
