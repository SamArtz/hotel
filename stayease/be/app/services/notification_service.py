import asyncio
from sqlalchemy.orm import Session
from fastapi import WebSocket
from ..repositories import notification_repo

# Diccionario para rastrear conexiones activas: {user_id: websocket_obj}
_connections: dict[int, WebSocket] = {}

def register_ws(user_id: int, websocket: WebSocket):
    _connections[user_id] = websocket

def unregister_ws(user_id: int):
    if user_id in _connections:
        del _connections[user_id]

async def push(user_id: int, payload: dict):
    """Envía un mensaje privado a un usuario específico"""
    ws = _connections.get(user_id)
    if ws:
        try:
            await ws.send_json(payload)
        except Exception:
            unregister_ws(user_id)

async def broadcast(payload: dict):
    """Envía un mensaje a TODOS los empleados conectados (ej. cambio de estado de cuarto)"""
    for user_id, ws in list(_connections.items()):
        try:
            await ws.send_json(payload)
        except Exception:
            unregister_ws(user_id)

def send_notification(db: Session, user_id: int, title: str, message: str, ntype: str, related_reservation_id: int = None):
    """Guarda en DB y hace push por WebSocket si el usuario está online"""
    # 1. Guardar en Base de Datos (Persistencia)
    note = notification_repo.create(db, user_id, title, message, ntype, related_reservation_id)
    
    # 2. Intento de envío inmediato (Best-effort)
    payload = {
        "id": note.id,
        "title": title,
        "message": message,
        "type": ntype,
        "reservation_id": related_reservation_id
    }
    # Usar ensure_future para no bloquear el hilo principal
    asyncio.ensure_future(push(user_id, payload))
    return note