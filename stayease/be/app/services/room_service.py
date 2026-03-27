from sqlalchemy.orm import Session
from ..repositories import room_repo
from ..schemas.room import RoomCreate, RoomUpdate

def add_room(db: Session, data: RoomCreate):
    return room_repo.create(db, data.model_dump())

def update_room(db: Session, room_id: int, data: RoomUpdate):
    room = room_repo.get_by_id(db, room_id)
    if not room: return None
    return room_repo.update(db, room, data.model_dump(exclude_unset=True))