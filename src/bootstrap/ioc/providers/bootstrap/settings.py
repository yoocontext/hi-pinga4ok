# pyright: reportUnknownVariableType=false

from dishka import Provider, Scope, provide

from bootstrap.settings import PgSettings, Settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def pg_settings(self, settings: Settings) -> PgSettings:
        return settings.pg
