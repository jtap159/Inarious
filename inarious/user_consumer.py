# import faust
import asyncio
import datetime

from inarious.config import settings
from inarious.kafka.consumer import App

app1 = App()
app1.topic("Users")
app1.topic("Clients")


@app1.agent(["Users", "Clients"])
async def run_main(message):
    print(message)


@app1.agent(["Clients"])
async def run_clients(message):
    print(message)


@app1.cronjob(
    10,
    start=datetime.datetime.now(),
    end=datetime.datetime(2024, 2, 4, 0, 0, 0, 0,)
)
async def run_job1():
    print("hello from cronjob 1")


@app1.cronjob(
    2,
    start=datetime.datetime.now(),
    end=datetime.datetime(2024, 2, 4, 0, 0, 0, 0,)
)
async def run_job2():
    print("hello from cronjob 2")


@app1.task()
async def task1():
    print("hello from task 1")


@app1.task()
async def task2():
    print("hello from task 2")


@app1.timer(5)
async def foo():
    print("fuck you")


@app1.timer(10)
async def foo2():
    print("fuck you too")


async def main():
    await app1.main()
    print("hello")


if __name__ == "__main__":
    asyncio.run(main())
