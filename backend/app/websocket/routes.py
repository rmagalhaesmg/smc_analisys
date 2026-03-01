"""
WebSocket Routes - Endpoints para comunicação em tempo real
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket.manager import manager
from app.auth.jwt import decode_token
from app.signals.manager import signal_manager
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


async def authenticate_websocket(token: Optional[str]) -> bool:
    """
    Autentica o token JWT do WebSocket
    
    Returns:
        True se autenticado ou token não requerido, False se rejeitar
    """
    if not token:
        # Allow connections without token for demo
        return True
    
    try:
        payload = decode_token(token)
        return payload is not None
    except Exception as e:
        logger.warning(f"WebSocket auth failed: {e}")
        return True  # Allow for demo


@router.websocket("/ws/realtime")
async def websocket_realtime(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    WebSocket endpoint principal para tempo real
    
    Rooms disponíveis:
    - signals: Broadcast de novos sinais
    - metrics: Broadcast de métricas
    - alerts: Broadcast de alertas
    - replay: Dados do replay
    """
    # Autentica
    if not await authenticate_websocket(token):
        await websocket.close(code=1008)
        return
    
    # Aceita conexão
    await manager.connect(websocket, room="signals")
    
    try:
        # Envia estado atual
        await websocket.send_json({
            "type": "system",
            "data": {
                "message": "Connected to SMC Real-Time",
                "open_signals": len(signal_manager.get_open_signals()),
                "closed_signals": len(signal_manager.closed_signals)
            }
        })
        
        # Mantém conexão ativa
        while True:
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Processa comandos do cliente
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif message.get("type") == "get_metrics":
                    metrics = signal_manager.get_metrics()
                    await websocket.send_json(metrics.to_dict())
                elif message.get("type") == "subscribe":
                    room = message.get("room")
                    if room:
                        manager.disconnect(websocket)
                        await manager.connect(websocket, room=room)
                        
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@router.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    WebSocket endpoint específico para sinais
    """
    if not await authenticate_websocket(token):
        await websocket.close(code=1008)
        return
    
    await manager.connect(websocket, room="signals")
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "ack"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    WebSocket endpoint específico para métricas em tempo real
    """
    if not await authenticate_websocket(token):
        await websocket.close(code=1008)
        return
    
    await manager.connect(websocket, room="metrics")
    
    try:
        # Envia métricas iniciais
        metrics = signal_manager.get_metrics()
        await websocket.send_json(metrics.to_dict())
        
        while True:
            data = await websocket.receive_text()
            
            # Permite request de métricas
            if data == "refresh":
                metrics = signal_manager.get_metrics()
                await websocket.send_json(metrics.to_dict())
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/replay")
async def websocket_replay(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    WebSocket endpoint para replay/backtest
    """
    if not await authenticate_websocket(token):
        await websocket.close(code=1008)
        return
    
    await manager.connect(websocket, room="replay")
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "ack", "room": "replay"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
