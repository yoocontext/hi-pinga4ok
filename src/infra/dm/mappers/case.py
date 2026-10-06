from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from application.entities.case import (
    Case,
    CaseDrop,
)
from infra.dm.mappers.item import item_from_orm
from infra.orm.cases import (
    CaseDropOrm,
    CaseOrm,
)


def case_loading() -> LoaderOption:
    """Load what `case_from_orm` reads: drops and their items.

    drops is a collection: a JOIN would repeat the case row once per drop,
    so selectinload fetches them in a second `WHERE case_id IN (...)` query.
    item is one row per drop: a plain JOIN adds columns without repeating
    rows, so joinedload is cheaper there.
    """

    return selectinload(CaseOrm.drops).joinedload(
        CaseDropOrm.item,
        innerjoin=True,
    )


def case_from_orm(
    *,
    orm: CaseOrm,
) -> Case:
    return Case(
        id=orm.id,
        name=orm.name,
        price=orm.price,
        drops=tuple(
            CaseDrop(
                item=item_from_orm(orm=drop.item),
                weight=drop.weight,
            )
            for drop in orm.drops
        ),
    )
