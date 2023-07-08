import faust
from Inarious.config import settings


class UserMethod(faust.Record):
    client_host: str
    client_port: str
    endpoint: str
    http_method: str


app = faust.App(
    "inarious-app", broker=f"kafka://{settings.KAFKA_URL}"
)
users_kafka_topic = app.topic("Users", key_type=str, value_type=UserMethod)


@app.agent(users_kafka_topic)
async def process(user_methods):
    async for user_method in user_methods:
        print(f"{str(user_method)}")


if __name__ == "__main__":
    app.main()
