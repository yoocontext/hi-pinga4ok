# pyright: reportUnknownVariableType=false

from dishka import (
    Provider,
    Scope,
    provide,
)

from application.use_cases.players.config import PlayersConfig
from bootstrap.settings import (
    PgSettings,
    Settings,
)


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def pg_settings(
        self,
        *,
        settings: Settings,
    ) -> PgSettings:
        return settings.pg

    @provide(scope=Scope.APP)
    def players_config(
        self,
        *,
        settings: Settings,
    ) -> PlayersConfig:
        return PlayersConfig(
            start_balance=settings.players.start_balance,
            daily_bonus=settings.players.daily_bonus,
            daily_bonus_cooldown=settings.players.daily_bonus_cooldown,
        )
