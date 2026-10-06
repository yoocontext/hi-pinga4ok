# pyright: reportUnknownVariableType=false

from dishka import (
    Provider,
    Scope,
    provide,
)

from application.interfaces.queries.cases import ICasesQueries
from application.interfaces.queries.inventory import IInventoryQueries
from application.interfaces.queries.leaderboard import ILeaderboardQueries
from application.interfaces.queries.players import IPlayersQueries
from infra.queries.cases import AlchemyCasesQueries
from infra.queries.inventory import AlchemyInventoryQueries
from infra.queries.leaderboard import AlchemyLeaderboardQueries
from infra.queries.players import AlchemyPlayersQueries


class QueriesProvider(Provider):
    players_queries = provide(
        AlchemyPlayersQueries,
        provides=IPlayersQueries,
        scope=Scope.REQUEST,
    )

    cases_queries = provide(
        AlchemyCasesQueries,
        provides=ICasesQueries,
        scope=Scope.REQUEST,
    )

    inventory_queries = provide(
        AlchemyInventoryQueries,
        provides=IInventoryQueries,
        scope=Scope.REQUEST,
    )

    leaderboard_queries = provide(
        AlchemyLeaderboardQueries,
        provides=ILeaderboardQueries,
        scope=Scope.REQUEST,
    )
