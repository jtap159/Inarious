from pydantic import BaseSettings
import socket


class Settings(BaseSettings):
    ARANGO_USERNAME: str
    ARANGO_ROOT_PASSWORD: str
    ARANGO_URL: str
    ARANGO_DATABASE: str
    KAFKA_HOSTNAME: str
    KAFKA_PORT: str

    @property
    def KAFKA_URL(self):
        return f"{self.KAFKA_HOSTNAME}:{self.KAFKA_PORT}"

    @property
    def KAFKA_PRODUCER_CONF(self):
        conf = {
            "bootstrap.servers": self.KAFKA_URL,
            "client.id": socket.gethostname(),
        }
        return conf


settings = Settings()
