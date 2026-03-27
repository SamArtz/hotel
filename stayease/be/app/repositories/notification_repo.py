from sqlalchemy.orm import Session
from ..models.notification import Notification

def create(db: Session, user_id: int, title: str, message: str, ntype: str, 
           related_reservation_id: int = None):
    db_note = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=ntype,
        related_reservation_id=related_reservation_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_for_user(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()