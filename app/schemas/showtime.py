from pydantic import BaseModel
from typing import Optional
from datetime import date,time

class ShowTimeCreate(BaseModel):
    movie_id : int
    theatre_id : int
    screen_no : int
    show_date : date
    show_time : time
    available_seat : int

class ShowTimeResponse(ShowTimeCreate):
    id: int


    class Config:
        orm_mode = True