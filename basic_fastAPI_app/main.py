from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session

from models import User as modelUser
from schemas import User as schemaUser

from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(modelUser).all()


@app.post("/users/")
def post_user(user: schemaUser, db: Session = Depends(get_db)):
    db_user = modelUser(**dict(user))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)

