from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.showtime import ShowTime
from app.schemas.showtime import ShowTimeCreate, ShowTimeResponse

#only admin access
from app.utils.jwt import admin_required
from app.models.user import User

router = APIRouter(
    prefix="/showtime",
    tags=["ShowTime"]
)

#create showtime
@router.post("/", response_model=ShowTimeResponse, status_code=status.HTTP_201_CREATED)
def create_show_time(showtime: ShowTimeCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    new_show_time = ShowTime(**showtime.dict())
    db.add(new_show_time)
    db.commit()
    db.refresh(new_show_time)
    return new_show_time

#get all showtime
from typing import List
@router.get("/",response_model=List[ShowTimeResponse])
def get_show_time(db: Session = Depends(get_db)):
    return db.query(ShowTime).all()

#get showtime by id
@router.get("/{showtime_id}", response_model=ShowTimeResponse)
def get_showtime(showtime_id:int, db:Session = Depends(get_db)):
    showtime = db.query(ShowTime).filter(ShowTime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime

#delete showtime
@router.delete("/{showtime_id}")
def delete_showtime(showtime_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    showtime = db.query(ShowTime).filter(ShowTime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    db.delete(showtime)
    db.commit()
    return {"detail": "Showtime deleted successfully"}
