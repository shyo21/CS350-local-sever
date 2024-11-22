import models
import schemas
import database
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/add_wait_time", response_model=schemas.WaitTimeCreate)
def add_wait_time(wait_time: schemas.WaitTimeCreate, db: Session = Depends(database.get_db)):
    db_wait_time = models.WaitTime(
        building_id=wait_time.building_id,
        store_id=wait_time.store_id,
        ewt_num=wait_time.ewt_num,
        ewt_cur=wait_time.ewt_cur,
        timestamp=wait_time.timestamp
    )
    db.add(db_wait_time)
    db.commit()
    db.refresh(db_wait_time)
    return wait_time
