from kafka.admin import KafkaAdminClient, NewTopic


def run():
    try:
        print("connecting.....")
        admin_client = KafkaAdminClient(
            bootstrap_servers="localhost:9092", client_id="myapp"
        )
        print("connected")
        print("creating Users Topic")
        topic_list = []

        topic_list.append(
            NewTopic(name="Users", num_partitions=1, replication_factor=1)
        )
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("created Users Topic")
    except Exception as err:
        print(err)


def check_topic_lists():
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", client_id="myapp"
    )
    print(admin_client.list_topics())


if __name__ == "__main__":
    check_topic_lists()
