import asyncio
import datetime
import time

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

from inarious.config import settings


class ConsumerConfig(BaseModel):
    bootstrap_servers: str = Field(default=settings.KAFKA_URL)
    group_id: str = Field(default=str(uuid4()))


class ProducerConfig(ConsumerConfig):
    ...


class CronJobConfig(BaseModel):
    interval: int
    start: Optional[datetime.datetime] = Field(
        default=datetime.datetime.now()
    )
    end: Optional[datetime.datetime] = Field(default=None)


async def aio_kafka_producer(producer_config: ProducerConfig):
    return AIOKafkaProducer(
        bootstrap_servers=producer_config.bootstrap_servers
    )


async def aio_kafka_consumer(topics, consumer_config: ConsumerConfig):
    return AIOKafkaConsumer(
        *topics,
        bootstrap_servers=consumer_config.bootstrap_servers,
        group_id=consumer_config.group_id,
    )


async def consume_messages(consumer):
    try:
        while True:
            async for msg in consumer:
                await asyncio.sleep(0.1)
                if msg is None:
                    continue
                yield msg
    except Exception as err:
        print(f"Exception {err}")
        await consumer.stop()
    finally:
        await consumer.stop()


class App:

    def __init__(
        self,
        bootstrap_servers: str = settings.KAFKA_URL,
        group_id: Optional[str] = None,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.producer = None
        self.agents = dict()
        self.timers = list()
        self.tasks = list()
        self.topics = list()
        self.cronjobs = list()

    def topic(self, topic: str):
        self.topics.append(topic)

    def agent(self, topics: list[str]):
        def decorator(func):
            for topic in topics:
                if topic in self.agents:
                    if isinstance(self.agents[topic], list):
                        self.agents[topic].append(func)
                    else:
                        self.agents[topic] = [self.agents[topic]]
                        self.agents[topic].append(func)
                else:
                    self.agents[topic] = [func]
        return decorator

    def timer(self, interval):
        def decorator(func):
            self.timers.append(self.run_timer(interval, func))
            return func
        return decorator

    def task(self):
        def decorator(func):
            self.tasks.append(self.run_task(func))
            return func
        return decorator

    def cronjob(self, interval, start=None, end=None):
        def decorator(func):
            cronjob_config = {
                "interval": interval, "start": start, "end": end
            }
            cronjob_config = {k: v for k, v in cronjob_config.items() if v}
            self.cronjobs.append(
                self.run_cronjob(CronJobConfig(**cronjob_config), func)
            )
            return func
        return decorator

    async def run_task(self, func):
        await asyncio.sleep(0.1, await func())

    async def run_timer(self, interval, func):
        while True:
            await asyncio.sleep(interval, await func())

    async def run_cronjob(self, config, func):
        if (now := datetime.datetime.now()) < config.start:
            await asyncio.sleep(config.start - now)
        while now < config.end:
            await asyncio.sleep(config.interval, await func())
            now = datetime.datetime.now()

    async def run_agents(self):
        while True:
            async for msg in consume_messages(self.consumer):
                for func in self.agents[msg.topic]:
                    await func(msg.value)
            await asyncio.sleep(0.1)

    async def run_jobs(self):
        await asyncio.sleep(0.1)
        await asyncio.gather(
            *self.tasks,
            *self.timers,
            self.run_agents(),
            *self.cronjobs,
        )

    async def send(self, topic, record_value):
        await self.producer.start()
        while True:
            try:
                res = await self.producer.send_and_wait(topic, record_value)
                print(res)
                await asyncio.sleep(1)
            except Exception:
                await self.producer.stop()
                raise

    async def main(self):
        try:
            self.consumer = await aio_kafka_consumer(
                self.topics, ConsumerConfig()
            )
            self.producer = await aio_kafka_producer(
                ProducerConfig()
            )
            await self.consumer.start()
            await self.run_jobs()
        except Exception as err:
            print(f"Exception: {err}")
            await self.consumer.stop()
        finally:
            await self.consumer.stop()
