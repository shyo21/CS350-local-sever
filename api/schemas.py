# api/schemas.py
from pydantic import BaseModel
from datetime import datetime

class WaitTimeCreate(BaseModel):
    building_id: int
    store_id: int
    ewt_num: int
    ewt_cur: float
    timestamp: datetime
