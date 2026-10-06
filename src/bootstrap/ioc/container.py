from dishka import (
    AsyncContainer,
    make_async_container,
)

from bootstrap.ioc.providers.application.use_cases import UseCasesProvider
from bootstrap.ioc.providers.bootstrap.settings import SettingsProvider
from bootstrap.ioc.providers.infra.alchemy import AlchemyProvider
from bootstrap.ioc.providers.infra.clock import ClockProvider
from bootstrap.ioc.providers.infra.dm import DmProvider
from bootstrap.ioc.providers.infra.queries import QueriesProvider
from bootstrap.ioc.providers.infra.random import RandomProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        ClockProvider(),
        RandomProvider(),
        AlchemyProvider(),
        DmProvider(),
        QueriesProvider(),
        UseCasesProvider(),
    )
