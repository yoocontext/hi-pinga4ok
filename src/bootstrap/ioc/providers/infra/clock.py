# pyright: reportUnknownVariableType=false

from dishka import Provider, Scope, provide

from application.interfaces.clock import IClock
from infra.clock import SystemClock


class ClockProvider(Provider):
    @provide(scope=Scope.APP)
    def clock(self) -> IClock:
        return SystemClock()
