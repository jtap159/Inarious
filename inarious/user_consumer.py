# import faust
import asyncio

from inarious.config import settings
from inarious.kafka.consumer import AsyncConsumer


async def main():
    consumer = AsyncConsumer(settings.KAFKA_URL, 'my_group')

    async for message in consumer.consume():
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
