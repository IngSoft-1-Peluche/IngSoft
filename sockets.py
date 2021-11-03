from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[(int, WebSocket)] = []

    async def connect(self, id_partida: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append((id_partida, websocket))

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection[1] == websocket:
                self.active_connections.remove(connection)

    async def send_personal_message(self, action, data, websocket: WebSocket):
        await websocket.send_json({"action":action, "data":data})

    async def broadcast(self, action, data, id_partida):
        for connection in self.active_connections:
            if connection[0] == id_partida:
                await connection[1].send_json({"action": action, "data": data})