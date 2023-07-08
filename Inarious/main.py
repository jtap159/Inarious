from fastapi import FastAPI
import uvicorn
from Inarious.database.arangodb.database import initialize_db_collection
from Inarious.routers import users

initialize_db_collection()

app = FastAPI()

app.include_router(
    users.router,
    prefix="/users",
    tags=['users']
)


@app.get("/")
def home():
    return {"message": "welcome to Inarious"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
