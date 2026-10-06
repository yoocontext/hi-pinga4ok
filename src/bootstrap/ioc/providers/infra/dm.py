# pyright: reportUnknownVariableType=false

from dishka import (
    Provider,
    Scope,
    provide,
)

from application.interfaces.dm.case import ICaseDm
from application.interfaces.dm.inventory_item import IInventoryItemDm
from application.interfaces.dm.player import IPlayerDm
from infra.dm.case import AlchemyCaseDm
from infra.dm.inventory_item import AlchemyInventoryItemDm
from infra.dm.player import AlchemyPlayerDm


class DmProvider(Provider):
    player_dm = provide(
        AlchemyPlayerDm,
        provides=IPlayerDm,
        scope=Scope.REQUEST,
    )

    case_dm = provide(
        AlchemyCaseDm,
        provides=ICaseDm,
        scope=Scope.REQUEST,
    )

    inventory_item_dm = provide(
        AlchemyInventoryItemDm,
        provides=IInventoryItemDm,
        scope=Scope.REQUEST,
    )
