from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt
from ..config import settings
from ..services import notification_service

router = APIRouter(tags=["WebSockets"])

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    user_id = None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        await websocket.close(code=1008)
        return

    await websocket.accept()
    notification_service.register_ws(user_id, websocket)
    
    try:
        while True:
            # Mantener conexión viva esperando mensajes (aunque no hagamos nada con ellos)
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_service.unregister_ws(user_id)