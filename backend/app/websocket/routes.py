from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket.manager import manager
from app.auth.jwt import decode_token
from typing import Optional

router = APIRouter()


@router.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    """WebSocket endpoint for real-time updates"""
    
    # Validate token if provided
    if token:
        try:
            payload = decode_token(token)
            if not payload:
                await websocket.close(code=1008)
                return
        except Exception:
            # Allow connection without auth for demo purposes
            pass
    
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive, wait for messages
            data = await websocket.receive_text()
            # Echo back for ping/pong
            await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@router.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket, token: Optional[str] = Query(None)):
    """WebSocket endpoint specifically for signals"""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
