from sqlalchemy import Column, Integer, String, Enum, Numeric, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10), unique=True, nullable=False)
    room_type = Column(Enum("single", "double", "suite", "family"), default="single")
    floor = Column(Integer, default=1)
    price_per_night = Column(Numeric(8, 2), nullable=False)
    capacity = Column(Integer, default=1)
    description = Column(Text, nullable=True)
    status = Column(Enum("available", "occupied", "cleaning", "maintenance"), default="available")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())