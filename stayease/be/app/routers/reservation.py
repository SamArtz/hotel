from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.guest import GuestCreate, GuestOut
from ..services import guest_service
from .deps import get_current_user

# Esto inicializa el router, sin esto @router.post no funciona
router = APIRouter(prefix="/guests", tags=["Guests"])

@router.get("/", response_model=list[GuestOut])
def get_guests(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return guest_service.guest_repo.get_all(db)

@router.post("/", response_model=GuestOut, status_code=201)
def add_guest(data: GuestCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    guest = guest_service.add_guest(db, data)
    if not guest:
        raise HTTPException(status_code=409, detail="A guest with that email already exists")
    return guest