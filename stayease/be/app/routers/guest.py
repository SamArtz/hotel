from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.reservation import ReservationCreate, ReservationOut, ReservationStatusUpdate
from ..services import reservation_service
from .deps import get_current_user

# Esto es lo que te faltaba
router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationOut, status_code=201)
def make_reservation(data: ReservationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    res = reservation_service.create_reservation(db, current_user.id, data)
    if not res:
        raise HTTPException(status_code=422, detail="Room unavailable or guest not found")
    return res

@router.get("/mine", response_model=list[ReservationOut])
def get_my_reservations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return reservation_service.get_my_reservations(db, current_user.id)

@router.patch("/{reservation_id}/status", response_model=ReservationOut)
def update_status(reservation_id: int, data: ReservationStatusUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    res = reservation_service.update_reservation_status(db, reservation_id, current_user.id, data.status)
    if not res:
        raise HTTPException(status_code=422, detail="Invalid status transition")
    return res