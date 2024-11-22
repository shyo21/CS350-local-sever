from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/add_wait_time", response_model=schemas.WaitTimeCreate)
def add_wait_time(wait_time: schemas.WaitTimeCreate, db: Session = Depends(database.get_db)):
    db_wait_time = models.WaitTime(
        cafeteria_id=wait_time.cafeteria_id,
        wait_count=wait_time.wait_count,
        estimated_wait_time=wait_time.estimated_wait_time,
        timestamp=wait_time.timestamp
    )
    db.add(db_wait_time)
    db.commit()
    db.refresh(db_wait_time)
    return wait_time
