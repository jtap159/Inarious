from fastapi import APIRouter, HTTPException, Request
from pyArango.theExceptions import UniqueConstrainViolation
from Inarious.database.arangodb.database import conn
from Inarious.schemas.arangodb.schemas import User as schema_User
from Inarious.kafka.producer import send_event

router = APIRouter()


@router.get("/")
async def get_users(request: Request):
    send_event("Users", request.base_url.hostname, request.method)
    db = conn["inarious"]
    users_collection = db["Users"]
    users = []
    for user in users_collection.fetchAll():
        users.append(user.getStore())
    return users


@router.post("/")
async def post_user(user: schema_User, request: Request):
    send_event("Users", request.base_url.hostname, request.method)
    db = conn["inarious"]
    users_collection = db["Users"]
    try:
        doc = users_collection.createDocument()
        doc["first_name"] = user.first_name
        doc["last_name"] = user.last_name
        doc["middle_name"] = user.middle_name
        doc["gender"] = user.gender
        doc._key = user.first_name + user.last_name
        doc.save()
    except UniqueConstrainViolation as err:
        return HTTPException(status_code=400, detail="Item already exists.")
    return user.dict()
