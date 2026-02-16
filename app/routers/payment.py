from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.payment import Payment
from app.models.booking import Booking
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.models.user import User
from app.utils.jwt import get_current_user  


router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)

@router.post("/create/{booking_id}")
def create_payment(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    payment = Payment(
        user_id=current_user.id,
        booking_id=booking.id,
        amount=booking.total_price,
        status="pending",
        payment_gateway="mock"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "payment_id": payment.id,
        "amount": payment.amount,
        "status": payment.status
    }

@router.post("/{payment_id}/success")
def payment_success(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment or payment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    payment.status = "success"
    payment.transaction_id = str(uuid.uuid4())

    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    booking.status = "CONFIRMED"

    db.commit()

    return {
        "message": "Payment successful",
        "booking_status": booking.status
    }

@router.post("/{payment_id}/fail")
def payment_failed(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment or payment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    payment.status = "failed"

    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    booking.status = "CANCELLED"

    db.commit()

    return {
        "message": "Payment failed",
        "booking_status": booking.status
    }
