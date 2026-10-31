from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )

    postgres_user: str = "user"
    postgres_password: str = "pass"
    postgres_host: str = "localhost"
    postgres_db: str = "db_example"
    postgres_port: int = "5435"

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

@lru_cache
def get_settings():
    return Config()

settings = get_settings()
