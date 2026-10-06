# pyright: reportUnknownVariableType=false

from dishka import (
    Provider,
    Scope,
    provide,
)

from application.use_cases.cases.list import ListCasesUc
from application.use_cases.cases.open import OpenCaseUc
from application.use_cases.get_leaderboard import GetLeaderboardUc
from application.use_cases.inventory.get import GetInventoryUc
from application.use_cases.inventory.gift import GiftItemUc
from application.use_cases.players.claim_daily_bonus import ClaimDailyBonusUc
from application.use_cases.players.create import CreatePlayerUc
from application.use_cases.players.get import GetPlayerUc


class UseCasesProvider(Provider):
    create_player = provide(CreatePlayerUc, scope=Scope.REQUEST)
    get_player = provide(GetPlayerUc, scope=Scope.REQUEST)
    claim_daily_bonus = provide(ClaimDailyBonusUc, scope=Scope.REQUEST)
    list_cases = provide(ListCasesUc, scope=Scope.REQUEST)
    open_case = provide(OpenCaseUc, scope=Scope.REQUEST)
    get_inventory = provide(GetInventoryUc, scope=Scope.REQUEST)
    gift_item = provide(GiftItemUc, scope=Scope.REQUEST)
    get_leaderboard = provide(GetLeaderboardUc, scope=Scope.REQUEST)
