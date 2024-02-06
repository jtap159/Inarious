import datetime

from fastapi import APIRouter, HTTPException, Request
from pyArango.theExceptions import UniqueConstrainViolation
from uuid import uuid4

from inarious.database.arangodb.database import conn
from inarious.schemas.arangodb.schemas import PgToMongoPipelineRequest
from inarious.kafka.producer import send_json_event

router = APIRouter()


@router.get("/")
async def get_pipelines(request: Request):
    db = conn["inarious"]
    pg_to_mongo_collection = db["PgToMongoPipeline"]
    pipeline_calls = []
    for pipeline_call in pg_to_mongo_collection.fetchAll():
        pipeline_calls.append(pipeline_call.getStore())
    return pipeline_calls


@router.post("/")
async def post_pipelines(pg_to_mongo_pipeline: PgToMongoPipelineRequest, request: Request):
    event = {
        "client_host": request.client.host,
        "client_port": str(request.client.port),
        "endpoint": str(request.url),
        "http_method": request.method
    }
    send_json_event(
        "PgToMongoPipeline",
        request.base_url.hostname,
        event,
    )
    db = conn["inarious"]
    pg_to_mongo_collection = db["PgToMongoPipeline"]
    try:
        doc = pg_to_mongo_collection.createDocument()
        doc["call_time"] = datetime.datetime.now()
        doc._key = str(uuid4())
        doc.save()
    except UniqueConstrainViolation as err:
        return HTTPException(
            status_code=400,
            detail="Item already exists.",
        )
    return pg_to_mongo_pipeline.dict()
    # return pg_to_mongo_collection.dict()
