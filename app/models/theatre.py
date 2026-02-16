from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Theatre(Base):
    __tablename__ = "theatres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    total_screens = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)  