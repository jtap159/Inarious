from fastapi import FastAPI
import uvicorn

from inarious.database.arangodb.database import initialize_db_collection
from inarious.routers import users
from inarious.routers import pg_to_mdb_pipeline

initialize_db_collection()

app = FastAPI()

app.include_router(
    users.router,
    prefix="/users",
    tags=['users']
)
app.include_router(
    pg_to_mdb_pipeline.router,
    prefix="/pg_to_mdb_pipeline",
    tags=["pg_to_mdb_pipeline"]
)


@app.get("/")
def home():
    return {"message": "welcome to Inarious"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
