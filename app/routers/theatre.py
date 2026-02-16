from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.theatre import Theatre
from app.schemas.theatre import TheatreCreate, TheatreResponse

#only admin access
from app.utils.jwt import admin_required
from app.models.user import User

router = APIRouter(
    prefix="/theatres",
    tags=["Theatres"]
)

#create theatres
@router.post("/", response_model=TheatreResponse, status_code=status.HTTP_201_CREATED)
def create_theatre(theatre: TheatreCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    new_theatre = Theatre(**theatre.dict())
    db.add(new_theatre)
    db.commit()
    db.refresh(new_theatre)
    return new_theatre

#get all theatre list
from typing import List
@router.get("/", response_model=List[TheatreResponse])
def list_theatre(db: Session = Depends(get_db)):
    return db.query(Theatre).all()

#get theatre by id
@router.get("/{theatre_id}")
def get_theatre(theatre_id: int, db:Session = Depends(get_db)):
    theatre = db.query(Theatre).filter(Theatre.id == theatre_id).first()
    if not theatre:
        raise HTTPException(status_code=404, detail="Movie not found")
    return theatre

#delete theatre
@router.delete("/{theatre_id}")
def delete_theatre(theatre_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    theatre = db.query(Theatre).filter(Theatre.id == theatre_id).first()
    if not theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    db.delete(theatre)
    db.commit()
    return {"detail": "Theatre deleted successfully"}
