"""
WebSocket Connection Manager - Gerenciamento de Conexões em Tempo Real
"""
from typing import List, Dict, Any, Optional
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Gerenciador de Conexões WebSocket
    
    Funcionalidades:
    - Gerenciamento de conexões ativas
    - Broadcast para todos os clientes
    - Suporte a rooms/channels
    - Mensagens personalizadas
    - Reconexão automática
    """
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
        # Rooms para broadcasts específicos
        self.rooms: Dict[str, List[WebSocket]] = {
            "signals": [],
            "metrics": [],
            "alerts": [],
            "replay": []
        }
        
        # Contador de mensagens
        self.message_count = 0
    
    async def connect(self, websocket: WebSocket, room: Optional[str] = None):
        """Aceita nova conexão WebSocket"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Adiciona à room se especificado
        if room and room in self.rooms:
            self.rooms[room].append(websocket)
        
        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")
        
        # Envia mensagem de boas-vindas
        await self.send_personal_message({
            "type": "welcome",
            "message": "Connected to SMC WebSocket",
            "rooms": list(self.rooms.keys())
        }, websocket)
    
    def disconnect(self, websocket: WebSocket, room: Optional[str] = None):
        """Remove conexão WebSocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Remove da room específica
        if room and room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)
        
        # Remove de todas as rooms
        for room_name, connections in self.rooms.items():
            if websocket in connections:
                connections.remove(websocket)
        
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Envia mensagem para um cliente específico"""
        try:
            await websocket.send_json(message)
            self.message_count += 1
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict, room: Optional[str] = None):
        """
        Envia mensagem para todos os clientes conectados
        
        Args:
            message: Dicionário com a mensagem
            room: Room específica (opcional) - se None, envia para todos
        """
        self.message_count += 1
        
        # Determina quais conexões usar
        targets = self.rooms.get(room, []) if room else self.active_connections
        
        if not targets:
            return
        
        disconnected = []
        sent_count = 0
        
        for connection in targets:
            try:
                await connection.send_json(message)
                sent_count += 1
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.append(connection)
        
        # Remove clientes desconectados
        for connection in disconnected:
            self.disconnect(connection)
        
        logger.debug(f"Broadcast sent to {sent_count}/{len(targets)} clients")
    
    async def broadcast_signal(self, signal_data: dict):
        """Envia evento de sinal - formato padronizado"""
        await self.broadcast({
            "type": "signal",
            "data": signal_data
        }, room="signals")
    
    async def broadcast_metrics(self, metrics_data: dict):
        """Envia métricas - formato padronizado"""
        await self.broadcast({
            "type": "metrics",
            "data": metrics_data
        }, room="metrics")
    
    async def broadcast_alert(self, alert_data: dict):
        """Envia alerta - formato padronizado"""
        await self.broadcast({
            "type": "alert",
            "data": alert_data
        }, room="alerts")
    
    async def broadcast_replay(self, replay_data: dict):
        """Envia dados de replay - formato padronizado"""
        await self.broadcast({
            "type": "replay",
            "data": replay_data
        }, room="replay")
    
    def get_connection_count(self) -> int:
        """Retorna número de conexões ativas"""
        return len(self.active_connections)
    
    def get_room_count(self, room: str) -> int:
        """Retorna número de clientes em uma room específica"""
        return len(self.rooms.get(room, []))


# Singleton instance
manager = ConnectionManager()
