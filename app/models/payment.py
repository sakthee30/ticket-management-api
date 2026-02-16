from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)

    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  

    payment_gateway = Column(String, default="stripe")
    transaction_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

  
    user = relationship("User", backref="payments")
    booking = relationship("Booking", backref="payment")
