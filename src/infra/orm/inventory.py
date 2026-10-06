from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from infra.orm.base import BaseOrm
from infra.orm.mixins import UuidPkMixin

if TYPE_CHECKING:
    from infra.orm.cases import ItemOrm


class InventoryItemOrm(
    UuidPkMixin,
    BaseOrm,
):
    __tablename__ = "inventory_items"

    item: Mapped["ItemOrm"] = relationship(
        back_populates="inventory_items",
        lazy="raise",
    )

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("players.id"),
        index=True,
    )

    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))

    obtained_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
