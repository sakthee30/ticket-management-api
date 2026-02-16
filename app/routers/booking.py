from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse
from app.models.showtime import ShowTime
from app.schemas.showtime import ShowTimeCreate, ShowTimeResponse

#user access
from app.utils.jwt import user_required
from app.models.user import User

router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(user_required)):

    # 1. Get showtime
    show = (db.query(ShowTime).filter(ShowTime.id == booking.show_id).first())

    if show is None:
        raise HTTPException(status_code=404, detail="ShowTime not found")

    # 2. Check seat availability (
    if show.available_seat < booking.number_of_seats:
        raise HTTPException(status_code=400,detail=f"Only {show.available_seat} seats available")

    # 3. Calculate price
    ticket_price = 150
    total_price = booking.number_of_seats * ticket_price

    # 4. Reduce seats
    show.available_seat -= booking.number_of_seats

    # 5. Create booking
    new_booking = Booking(
        show_id=booking.show_id,
        user_id = current_user.id,
        number_of_seats=booking.number_of_seats,
        total_price=total_price
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

#get all booking 
from typing import List 
@router.get("/",response_model=List[BookingResponse]) 
def get_booking(db: Session = Depends(get_db)): 
	return db.query(Booking).all() 

#get booking by id 
@router.get("/{booking_id}", response_model=BookingResponse) 
def get_booking(booking_id:int, db:Session = Depends(get_db)): 
	booking = db.query(Booking).filter(Booking.id == booking_id).first() 
	if not booking: 
		raise HTTPException(status_code=404, detail="Showtime not found") 
	return booking 

#delete booking 
@router.delete("/{booking_id}") 
def delete_booking(booking_id: int, db: Session = Depends(get_db)): 
	booking = db.query(Booking).filter(Booking.id == booking_id).first() 
	if not booking: 
		raise HTTPException(status_code=404, detail="Booking not found") 
	
	db.delete(booking) 
	db.commit() 
	return {"detail": "Booking deleted successfully"}