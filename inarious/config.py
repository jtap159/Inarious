from pydantic import BaseSettings

import pathlib
import os
import socket


class Settings(BaseSettings):
    ARANGO_USERNAME: str
    ARANGO_ROOT_PASSWORD: str
    ARANGO_URL: str
    ARANGO_DATABASE: str
    KAFKA_HOSTNAME: str
    KAFKA_PORT: str
    MLB_CONTEST_FILES = (
        pathlib.Path(os.getenv("HOME")) /
        "freenas" /
        "MLB" /
        "mlb_historical_files" /
        "DK_contest_standings"
    )
    MINERVA_URL = os.getenv("MINERVA_URL")
    APOLLO_API = os.getenv("APOLLO_API")
    ARTEMIS_API = os.getenv("ARTEMIS_API")
    MSF_MLB_API = os.getenv("MSF_MLB_API")
    MSF_MLB_API_KEY = os.getenv("MSF_MLB_API_KEY")

    @property
    def KAFKA_URL(self):
        return f"{self.KAFKA_HOSTNAME}:{self.KAFKA_PORT}"

    @property
    def KAFKA_PRODUCER_CONF(self):
        return {
            "bootstrap.servers": self.KAFKA_URL,
            "client.id": socket.gethostname(),
        }


settings = Settings()
