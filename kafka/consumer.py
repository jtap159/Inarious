from kafka.consumer import KafkaConsumer
from kafka.admin import KafkaAdminClient


def run_consumer():
    print("connecting.....")
    consumer = KafkaConsumer(bootstrap_servers="localhost:9092", client_id="myapp")
    print("consumer is connected")
    print("sending a log to Users Topic")
    consumer.subscribe("Users")
    topic_partitions = consumer.assignment()
    result = consumer.beginning_offsets(topic_partitions)
    print(f"result {result}")
    consumer.close()


def check_topic_lists():
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", client_id="myapp"
    )
    print(admin_client.list_topics())


if __name__ == "__main__":
    run_consumer()
