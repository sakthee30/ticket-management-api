from pydantic import BaseModel
from typing import Optional
from datetime import date

class TheatreCreate(BaseModel):
    name: str
    location: str
    total_screens: int
    rating: Optional[float] = None

class TheatreResponse(BaseModel):
    id: int
    name: str
    location: str
    total_screens: int
    rating: Optional[float]

    class Config:
        orm_mode = True