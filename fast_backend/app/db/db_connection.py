from collections.abc import Generator
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSettings(BaseSettings):
    DATABASE_SERVER: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = DatabaseSettings()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD,
    host=settings.DATABASE_SERVER,
    port=settings.DATABASE_PORT,
    database=settings.DATABASE_NAME,
)

engine = create_engine(database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session