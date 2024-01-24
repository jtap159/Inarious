from confluent_kafka import Consumer


class AsyncConsumer(Consumer):
    """
    An asynchronous Kafka consumer.
    """

    def __init__(
        self,
        bootstrap_servers,
        group_id,
        auto_offset_reset='latest',
    ):
        super().__init__(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": auto_offset_reset,
            }
        )

    async def consume(self):
        """
        Asynchronously consumes messages from Kafka.
        """
        self.subscribe(['Users'])
        try:
            while True:
                message = self.poll(timeout=1.0)
                if not message:
                    continue

                if message.error():
                    print(f"{message.error()}")

                else:
                    yield message.value()

        finally:
            self.close()
