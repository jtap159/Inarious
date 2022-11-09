from fastapi import FastAPI
import uvicorn
from database import create_db_and_tables, engine, User
from sqlmodel import Session, select

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"Hello": "jeremy"}


@app.post("/users/")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/")
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000, reload=True)
