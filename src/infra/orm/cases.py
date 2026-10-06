from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from infra.orm.base import BaseOrm
from infra.orm.mixins import UuidPkMixin

if TYPE_CHECKING:
    from infra.orm.inventory import InventoryItemOrm


class ItemOrm(
    UuidPkMixin,
    BaseOrm,
):
    __tablename__ = "items"

    drops: Mapped[list["CaseDropOrm"]] = relationship(
        back_populates="item",
        lazy="raise",
    )

    inventory_items: Mapped[list["InventoryItemOrm"]] = relationship(
        back_populates="item",
        lazy="raise",
    )

    name: Mapped[str] = mapped_column(String(64))
    rarity: Mapped[str] = mapped_column(String(16))


class CaseOrm(
    UuidPkMixin,
    BaseOrm,
):
    __tablename__ = "cases"
    __table_args__ = (CheckConstraint("price > 0", name="price_positive"),)

    drops: Mapped[list["CaseDropOrm"]] = relationship(
        back_populates="case",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
    )

    name: Mapped[str] = mapped_column(String(64))
    price: Mapped[int] = mapped_column(Integer)


class CaseDropOrm(
    UuidPkMixin,
    BaseOrm,
):
    __tablename__ = "case_drops"
    __table_args__ = (CheckConstraint("weight > 0", name="weight_positive"),)

    case: Mapped[CaseOrm] = relationship(
        back_populates="drops",
        lazy="raise",
    )

    item: Mapped[ItemOrm] = relationship(
        back_populates="drops",
        lazy="raise",
    )

    case_id: Mapped[UUID] = mapped_column(
        ForeignKey("cases.id", ondelete="CASCADE"),
        index=True,
    )

    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))

    weight: Mapped[int] = mapped_column(Integer)
