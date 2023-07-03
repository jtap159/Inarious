from kafka.producer import KafkaProducer
from kafka.admin import KafkaAdminClient


def run_producer():
    print("connecting.....")
    producer = KafkaProducer(bootstrap_servers="localhost:9092", client_id="myapp")
    print("producer is connected")
    print("sending a log to Users Topic")
    result = producer.send("Users", b"jeremy tapia", partition=0)
    print(f"sent {result}")
    producer.close()


def check_topic_lists():
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", client_id="myapp"
    )
    print(admin_client.list_topics())


if __name__ == "__main__":
    run_producer()
