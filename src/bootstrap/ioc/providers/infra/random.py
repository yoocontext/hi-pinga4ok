# pyright: reportUnknownVariableType=false

from dishka import (
    Provider,
    Scope,
    provide,
)

from application.interfaces.random import IRandom
from infra.random import SystemRandomValue


class RandomProvider(Provider):
    @provide(scope=Scope.APP)
    def random(self) -> IRandom:
        return SystemRandomValue()
