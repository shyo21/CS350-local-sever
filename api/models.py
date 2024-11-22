# api/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from api.database import Base

class WaitTime(Base):
    __tablename__ = "wait_times"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, nullable=False, index=True)
    store_id = Column(Integer, nullable=False, index=True)
    ewt_num = Column(Integer, nullable=False)
    ewt_cur = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
