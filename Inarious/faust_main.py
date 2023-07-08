import faust


class UserMethod(faust.Record):
    method: str


app = faust.App(
    "inarious-app", broker="kafka://localhost:19092", value_serializer="raw"
)
users_kafka_topic = app.topic("Users", key_type=str, value_type=str)


@app.agent(users_kafka_topic)
async def process(user_method_stream):
    async for key, method in user_method_stream.items():
        print(f"key: {key} method: {method}")


if __name__ == "__main__":
    app.main()
