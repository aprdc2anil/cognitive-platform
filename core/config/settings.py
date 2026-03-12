from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "cognitive-platform"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "cognitive"
    POSTGRES_USER: str = "cognitive"
    POSTGRES_PASSWORD: str = "cognitive"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    PROMETHEUS_ENABLED: bool = True


settings = Settings()
