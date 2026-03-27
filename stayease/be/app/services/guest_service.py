from sqlalchemy.orm import Session
from ..repositories import guest_repo
from ..schemas.guest import GuestCreate

def add_guest(db: Session, data: GuestCreate):
    existing = guest_repo.get_by_email(db, data.email)
    if existing: return None
    return guest_repo.create(db, data.model_dump())