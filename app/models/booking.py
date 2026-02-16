from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)  
    
     # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("showtime.id"), nullable=False)

    # Booking details
    number_of_seats = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    status = Column(String, default="PENDING")

    # Relationships
    user = relationship("User", backref="bookings")
    show = relationship("ShowTime", backref="bookings")

    # id = Column(Integer, primary_key=True, index=True)
    # show_id = Column(Integer, ForeignKey("showtime.id"), nullable=False)
    # user_name = Column(String, nullable=False)
    # email = Column(String, unique=True, index=True, nullable=False)
    # number_of_seats = Column(Integer, nullable=False)
    # total_price = Column(Float, nullable=False)

