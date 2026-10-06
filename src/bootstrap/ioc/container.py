from dishka import AsyncContainer, make_async_container

from bootstrap.ioc.providers.bootstrap.settings import SettingsProvider
from bootstrap.ioc.providers.infra.alchemy import AlchemyProvider
from bootstrap.ioc.providers.infra.clock import ClockProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        ClockProvider(),
        AlchemyProvider(),
    )
