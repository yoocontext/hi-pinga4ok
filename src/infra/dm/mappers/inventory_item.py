from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption

from application.entities.inventory_item import InventoryItem
from infra.dm.mappers.item import item_from_orm
from infra.orm.inventory import InventoryItemOrm


def inventory_item_loading() -> LoaderOption:
    """Load what `inventory_item_from_orm` reads: the catalog item.

    every inventory row has exactly one item, so a JOIN does not repeat rows.
    """

    return joinedload(InventoryItemOrm.item, innerjoin=True)


def inventory_item_from_orm(
    *,
    orm: InventoryItemOrm,
) -> InventoryItem:
    return InventoryItem(
        id=orm.id,
        owner_id=orm.owner_id,
        item=item_from_orm(orm=orm.item),
        obtained_at=orm.obtained_at,
    )


def inventory_item_to_orm(
    *,
    entity: InventoryItem,
) -> InventoryItemOrm:
    return InventoryItemOrm(
        id=entity.id,
        owner_id=entity.owner_id,
        item_id=entity.item.id,
        obtained_at=entity.obtained_at,
    )
