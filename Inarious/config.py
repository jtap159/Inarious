from pydantic import BaseSettings


class Settings(BaseSettings):
    ARANGO_USERNAME: str
    ARANGO_ROOT_PASSWORD: str
    ARANGO_URL: str
    ARANGO_DATABASE: str
    KAFKA_HOSTNAME: str
    KAFKA_PORT: str


settings = Settings()
