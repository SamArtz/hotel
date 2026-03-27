from sqlalchemy.orm import Session
from ..repositories import room_repo, guest_repo, reservation_repo
from ..schemas.reservation import ReservationCreate
from . import notification_service
import asyncio 

def create_reservation(db: Session, staff_id: int, data: ReservationCreate):
    # 1. Validar cuarto
    room = room_repo.get_by_id(db, data.room_id)
    if not room or room.status != "available":
        return None
    
    # 2. Validar huésped
    guest = guest_repo.get_by_id(db, data.guest_id)
    if not guest:
        return None
    
    # 3. Crear reserva
    res = reservation_repo.create(
        db, room.id, guest.id, staff_id,
        data.check_in_date, data.check_out_date,
        room.price_per_night, data.notes
    )
    
    # 4. Actualizar cuarto a ocupado
    room_repo.update_status(db, room, "occupied")
    
    # 5. Notificar al staff
    notification_service.send_notification(
        db, staff_id, "Reserva Creada", 
        f"Reserva #{res.id} confirmada para {guest.full_name}", 
        "reservation_created", res.id
    )
    
    return res

def update_reservation_status(db: Session, reservation_id: int, user_id: int, new_status: str):
    res = reservation_repo.get_by_id(db, reservation_id)
    if not res: return None

    # Lógica de transiciones válidas
    old_status = res.status
    if old_status == "confirmed" and new_status in ["checked_in", "cancelled"]:
        pass
    elif old_status == "checked_in" and new_status == "checked_out":
        pass
    else:
        return None # Transición inválida

    # Aplicar cambios
    reservation_repo.update_status(db, res, new_status)
    room = room_repo.get_by_id(db, res.room_id)

    if new_status == "checked_in":
        room_repo.update_status(db, room, "occupied")
    
    elif new_status == "checked_out":
        room_repo.update_status(db, room, "cleaning")
        # BROADCAST: Avisar a todos que el cuarto ahora está en limpieza
        asyncio.ensure_future(notification_service.broadcast({
            "type": "room_status_update",
            "room_id": room.id,
            "room_number": room.room_number,
            "new_status": "cleaning"
        }))
    
    elif new_status == "cancelled":
        room_repo.update_status(db, room, "available")

    return res

def get_my_reservations(db: Session, staff_id: int):
    return reservation_repo.get_by_staff(db, staff_id)

def get_all_reservations(db: Session):
    return reservation_repo.get_all(db)