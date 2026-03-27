from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    floor: int = 1
    price_per_night: Decimal
    capacity: int = 1
    description: Optional[str] = None
    status: str = "available"

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    floor: Optional[int] = None
    price_per_night: Optional[Decimal] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None

class RoomOut(RoomBase):
    id: int

    class Config:
        from_attributes = True