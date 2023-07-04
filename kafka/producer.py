from confluent_kafka import Producer
from random import choice
import socket


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def run_producer():
    print("connecting.....")
    topic = "Users"
    conf = {
        "bootstrap.servers": "localhost:19092",
        "client.id": socket.gethostname(),
    }
    producer = Producer(conf)
    print("producer is connected")
    users = ["jeremy", "blake", "ryan", "kelly", "barbra", "amanda"]
    events = ["clicked", "emailed", "swiped", "downloaded"]
    for _ in range(10):
        user = choice(users)
        event = choice(events)
        producer.produce(topic, key=user, value=event, callback=acked)

    # wait up to 1 second for events. callbacks will be invoked during
    # this method call if the message is acknowledged
    producer.poll(1)
    producer.flush()


if __name__ == "__main__":
    run_producer()
