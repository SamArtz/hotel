from pydantic import BaseModel, EmailStr
from typing import Optional

class GuestBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    document_id: Optional[str] = None

class GuestCreate(GuestBase):
    pass

class GuestOut(GuestBase):
    id: int

    class Config:
        from_attributes = True