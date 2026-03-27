from sqlalchemy.orm import Session
from ..models.user import User

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create(db: Session, username: str, email: str, password_hash: str, full_name: str, role: str):
    db_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user