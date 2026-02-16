from app.database import Base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

class ShowTime(Base):
    __tablename__="showtime"

    id = Column(Integer, primary_key= True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    theatre_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)
    screen_no = Column(Integer, nullable=False)
    show_date = Column(Date, nullable=False)
    show_time = Column(Time, nullable=False)
    available_seat = Column(Integer, nullable=False, default=0)

    movie = relationship("Movie", back_populates="showtimes")