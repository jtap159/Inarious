import sys
from confluent_kafka import Consumer
from confluent_kafka import KafkaException, KafkaError


def msg_process(kafka_event_msg):
    print(
        f"recieved topic: {kafka_event_msg.topic()},  \
          partition: {kafka_event_msg.partition()} \
          key: {kafka_event_msg.key()} \
          value: {kafka_event_msg.value()}"
    )


def run_consumer_loop(topics: list[str]):
    print("connecting.....")
    conf = {
        "bootstrap.servers": "localhost:19092",
        "group.id": "group1",  # group.id is required for consumers
        # what offset the consumer should read from in the event
        # there are no committed offsets for a partition
        "auto.offset.reset": "smallest",
        # need to commit the offset recieved from the event to know where we left off
        "enable.auto.commit": True,
    }
    consumer = Consumer(conf)
    print("consumer is connected")
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)

    except Exception as e:
        raise e
    finally:
        # Close down consumer to comit final offsets.
        consumer.close()


if __name__ == "__main__":
    run_consumer_loop(["Users"])
