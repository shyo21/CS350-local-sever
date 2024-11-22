# api/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class WaitTime(Base):
    __tablename__ = "wait_times"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, nullable=False)
    store_id = Column(Integer, nullable=False)
    ewt_num = Column(Integer, nullable=False)
    ewt_cur = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
