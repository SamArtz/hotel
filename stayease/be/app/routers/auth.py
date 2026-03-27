from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate, UserOut, LoginRequest
from ..schemas.token import Token
from ..services.auth_service import AuthService
from ..repositories import user_repo

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_by_username(db, username=data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed_pw = AuthService.hash_password(data.password)
    return user_repo.create(db, data.username, data.email, hashed_pw, data.full_name, data.role)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = user_repo.get_by_username(db, data.username)
    if not user or not AuthService.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    access_token = AuthService.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}