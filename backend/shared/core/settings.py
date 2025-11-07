from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AUTH_URL: str

    KAFKA_BOOTSTRAP_SERVERS: str

    class Config:
        env_file = ".env"


settings = Settings()