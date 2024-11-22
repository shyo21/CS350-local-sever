# api/schemas.py
from pydantic import BaseModel
from datetime import datetime

class WaitTimeCreate(BaseModel):
    cafeteria_id: int
    wait_count: int
    estimated_wait_time: float
    timestamp: datetime
