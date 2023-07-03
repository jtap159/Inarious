from confluent_kafka import Producer
import socket


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def run_producer():
    print("connecting.....")
    topic = "Users"
    conf = {
        "bootstrap.servers": "localhost:19092",
        "client.id": socket.gethostname(),
    }
    producer = Producer(conf)
    print("producer is connected")
    print("sending Users Topic")
    producer.produce(topic, key="name", value=b"Jeremy Tapia", callback=acked)

    # wait up to 1 second for events. callbacks will be invoked during
    # this method call if the message is acknowledged
    producer.poll(1)
    producer.flush()


if __name__ == "__main__":
    run_producer()
