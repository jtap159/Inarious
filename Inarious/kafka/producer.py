from confluent_kafka import Producer
import socket
from Inarious.config import settings


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def send_event(topic: str, key: str, value: str):
    server_url = f"{settings.KAFKA_HOSTNAME}:{settings.KAFKA_PORT}"
    conf = {
        "bootstrap.servers": server_url,
        "client.id": socket.gethostname(),
    }
    producer = Producer(conf)
    producer.produce(topic, key=key, value=value, callback=acked)

    # wait up to 1 second for events. callbacks will be invoked during
    # this method call if the message is acknowledged
    producer.poll(1)
    # producer.flush()

