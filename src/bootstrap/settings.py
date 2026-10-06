from datetime import timedelta

from pydantic import (
    BaseModel,
    Field,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class PgSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    db: str = "case_opener"
    user: str = "case_opener"
    password: str = "case_opener"
    echo: bool = False

    @property
    def sqlalchemy_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )


class PlayersSettings(BaseModel):
    start_balance: int = 500
    daily_bonus: int = 100
    daily_bonus_cooldown: timedelta = timedelta(hours=24)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    pg: PgSettings = Field(default_factory=PgSettings)
    players: PlayersSettings = Field(default_factory=PlayersSettings)
