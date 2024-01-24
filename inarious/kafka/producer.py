from confluent_kafka import Producer
from inarious.config import settings
from typing import Any, Dict
import json


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def send_raw_event(topic: str, key: str, value: str):
    """
    Send a raw event message value to the Kafka topic.

    Args:
        topics (str): The Kafka Topic name.
        key (str): The Kafka Topic message key.
        value (str): The Kafka topic message value as a raw byte str.
            Example (b'some message').
    """
    producer = Producer(settings.KAFKA_PRODUCER_CONF)
    producer.produce(
        topic, key=key, value=value, callback=acked,
    )

    # wait up to 1 second for events. callbacks will be invoked during
    # this method call if the message is acknowledged
    producer.poll(1)
    producer.flush()


def send_json_event(topic: str, key: str, value: Dict[str, Any]):
    """
    Send a json event message value to the Kafka topic.

    Args:
        topics (str): The Kafka Topic name.
        key (str): The Kafka Topic message key.
        value (str): The Kafka topic message value as a dictionary
            that will be converted to json.
    """
    producer = Producer(settings.KAFKA_PRODUCER_CONF)
    producer.produce(
        topic, key=key, value=json.dumps(value), callback=acked,
    )

    # wait up to 1 second for events. callbacks will be invoked during
    # this method call if the message is acknowledged
    producer.poll(1)
    producer.flush()
