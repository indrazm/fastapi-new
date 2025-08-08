import asyncio
import json

import redis.asyncio as redis
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.redis = None

    async def setup_redis(self):
        """Setup Redis and start listening"""
        self.redis = redis.from_url("redis://localhost:6377")
        asyncio.create_task(self._listen_redis())

    async def _listen_redis(self):
        """Listen for messages from Redis"""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("ws_messages")

        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                client_id = data["client_id"]
                msg = data["message"]

                # Send to specific client if connected
                if client_id in self.active_connections:
                    try:
                        await self.active_connections[client_id].send_text(msg)
                    except WebSocketDisconnect:
                        self.disconnect(client_id)

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: int):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_to_client(self, message: str, client_id: int):
        """Send message directly (for internal use)"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
                return True
            except WebSocketDisconnect:
                self.disconnect(client_id)
        return False


manager = ConnectionManager()
