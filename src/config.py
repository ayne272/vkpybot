from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    bot_token: str
    db_host: str = Field("localhost", alias="POSTGRES_HOST")
    db_port: int = Field(5432, alias="POSTGRES_PORT")
    db_user: str = Field(..., alias="POSTGRES_USER")
    db_pass: str = Field(..., alias="POSTGRES_PASSWORD")
    db_name: str = Field(..., alias="POSTGRES_DB")

    @property
    def db_url(self) -> str:
        """Динамически создает DSN (URL) для подключения к БД."""
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
ADMIN_IDS = [1031738398]