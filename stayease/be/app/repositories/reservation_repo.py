from sqlalchemy.orm import Session
from ..models.reservation import Reservation
from datetime import date

def create(db: Session, room_id: int, guest_id: int, staff_id: int, 
           check_in_date: date, check_out_date: date, 
           nightly_rate: float, notes: str):
    
    # Calcular total: (días) * tarifa
    days = (check_out_date - check_in_date).days
    total_amount = float(nightly_rate) * max(days, 1)
    
    db_res = Reservation(
        room_id=room_id,
        guest_id=guest_id,
        staff_id=staff_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        nightly_rate=nightly_rate,
        total_amount=total_amount,
        notes=notes
    )
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

def get_all(db: Session):
    return db.query(Reservation).all()

def get_by_staff(db: Session, staff_id: int):
    return db.query(Reservation).filter(Reservation.staff_id == staff_id).all()

def get_by_id(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def update_status(db: Session, reservation: Reservation, new_status: str):
    reservation.status = new_status
    db.commit()
    db.refresh(reservation)
    return reservation