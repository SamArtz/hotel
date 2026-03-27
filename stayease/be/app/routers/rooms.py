from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.room import RoomCreate, RoomOut, RoomUpdate
from ..services import room_service
from .deps import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=list[RoomOut])
def list_rooms(db: Session = Depends(get_db)):
    return room_service.room_repo.get_all(db)

@router.post("/", response_model=RoomOut, status_code=201)
def add_room(data: RoomCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return room_service.add_room(db, data)

@router.patch("/{room_id}", response_model=RoomOut)
def update_room(room_id: int, data: RoomUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    room = room_service.update_room(db, room_id, data)
    if not room:
        raise HTTPException(status_code=404, detail="Cuarto no encontrado")
    return room