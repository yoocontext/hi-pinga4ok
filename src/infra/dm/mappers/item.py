from application.entities.item import (
    Item,
    Rarity,
)
from infra.orm.cases import ItemOrm


def item_from_orm(
    *,
    orm: ItemOrm,
) -> Item:
    return Item(
        id=orm.id,
        name=orm.name,
        rarity=Rarity(orm.rarity),
    )
