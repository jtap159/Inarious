import faust
from Inarious.config import settings
from Inarious.protobuf.backendApiActivity_pb2 import BackendApiActivity
from faust.serializers import codecs
from typing import Any
from google.protobuf import json_format
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.protobuf import text_format
from google.protobuf.text_format import MessageToString
from google.protobuf.text_format import MessageToBytes


# see https://stackoverflow.com/questions/64686686/using-python-compiled-protobuf-pb2-as-key-and-value-serializer
class ProtobufSerializer(codecs.Codec):
    def __init__(self, pb_type: Any):
        self.pb_type = pb_type
        super(self.__class__, self).__init__()

    def _dumps(self, pb: Any) -> bytes:
        return pb.SerializeToString()

    def _loads(self, s: bytes) -> Any:
        pb = self.pb_type()
        pb.ParseFromString(s)
        return pb


app = faust.App(
    "inarious-app", broker=f"kafka://{settings.KAFKA_URL}"
)

activity_schema = faust.Schema(
    key_type=str,
    value_serializer=ProtobufSerializer(pb_type=BackendApiActivity)
)

users_kafka_topic = app.topic("Users", schema=activity_schema)


@app.agent(users_kafka_topic)
async def process(user_activities):
    async for user_activity in user_activities:
        print(f"{MessageToJson(user_activity)}")


if __name__ == "__main__":
    app.main()
