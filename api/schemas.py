from pydantic import BaseModel, Field
from datetime import datetime

class WaitTimeCreate(BaseModel):
    building_id: int = Field(..., example=1)
    store_id: int = Field(..., example=101)
    ewt_num: int = Field(..., example=15)
    ewt_cur: float = Field(..., example=25.5)
    timestamp: datetime = Field(..., example="2024-04-27T15:00:00.000Z")

    class Config:
        orm_mode = True

class WaitTimeResponse(BaseModel):
    id: int
    building_id: int
    store_id: int
    ewt_num: int
    ewt_cur: float
    timestamp: datetime

    class Config:
        orm_mode = True
