from pydantic import BaseModel
from typing import Optional
from datetime import date,time

class BookingCreate(BaseModel):
    show_id :int
    number_of_seats : int 

class BookingResponse(BookingCreate):
    id: int
    show_id: int
    user_id: int
    number_of_seats: int
    total_price : float


    class Config:
        orm_mode = True