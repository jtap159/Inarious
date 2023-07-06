import faust


class UserMethod(faust.Record):
    method: str


app = faust.App('inarious-app', broker='kafka://localhost:19092')
users_kafka_topic = app.topic("Users")


@app.agent(users_kafka_topic)
async def process(user_method_stream):
    print(user_method_stream)
    async for method in user_method_stream:
        print(f"method: {method}")


if __name__ == "__main__":
    app.main()
