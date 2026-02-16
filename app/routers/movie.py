from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse

#only admin access
from app.utils.jwt import admin_required
from app.models.user import User

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

#create movies
@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

#get all movie list
from typing import List
@router.get("/", response_model=List[MovieResponse])
def list_movie(db: Session = Depends(get_db)):
    return db.query(Movie).all()

#get movie by id
@router.get("/{movie_id}")
def get_movie(movie_id: int, db:Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

#delete movie
@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"detail": "Movie deleted successfully"}


