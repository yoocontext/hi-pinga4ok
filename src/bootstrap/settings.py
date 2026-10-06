from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PgSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    db: str = "project_name"
    user: str = "project_name"
    password: str = "project_name"

    @property
    def sqlalchemy_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    pg: PgSettings = Field(default_factory=PgSettings)
