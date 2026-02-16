from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.user import User
from app.utils.jwt import admin_required
from app.models.payment import Payment
from app.models.showtime import ShowTime
from app.models.movie import Movie
from app.models.theatre import Theatre

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/bookings")
def view_all_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    bookings = db.query(Booking).all()

    response = []

    for b in bookings:
        payment = (
            db.query(Payment)
            .filter(Payment.booking_id == b.id)
            .first()
        )

        response.append({
            "booking_id": b.id,
            "booking_status": b.status,

            "user": {
                "id": b.user.id,
                "name": b.user.name,
                "email": b.user.email
            },

            "movie": b.show.movie.title,
            "show_time": str(b.show.show_time),
            "seats": b.number_of_seats,
            "total_price": b.total_price,

            "payment": {
                "status": payment.status if payment else "not_initiated",
                "amount": payment.amount if payment else None,
                "transaction_id": payment.transaction_id if payment else None
            }
        })

    return response
