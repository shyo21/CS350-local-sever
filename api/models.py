# api/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class WaitTime(Base):
    __tablename__ = "wait_times"

    id = Column(Integer, primary_key=True, index=True)
    cafeteria_id = Column(Integer, nullable=False)
    wait_count = Column(Integer, nullable=False)
    estimated_wait_time = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
