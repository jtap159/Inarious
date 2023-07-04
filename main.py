from fastapi import FastAPI, Depends, HTTPException
from pyArango.database import Database
import uvicorn
from Inarious.schemas import User as schemaUser
from Inarious.database import conn, initialize_db_collection


initialize_db_collection()
app = FastAPI()


@app.get("/users/")
def get_users():
    db = conn["inarious"]
    users_collection = db["Users"]
    users = []
    for user in users_collection.fetchAll():
        users.append(user.getStore())
    return users


@app.post("/users/")
def post_user(user: schemaUser):
    db = conn["inarious"]
    users_collection = db["Users"]
    doc = users_collection.createDocument()
    doc["first_name"] = user.first_name
    doc["last_name"] = user.last_name
    doc["middle_name"] = user.middle_name
    doc["gender"] = user.gender
    doc._key = user.first_name + user.last_name
    doc.save()
    return user.dict()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
