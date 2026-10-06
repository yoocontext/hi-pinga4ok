from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from infra.orm.base import BaseOrm
from infra.orm.mixins import UuidPkMixin


class PlayerOrm(
    UuidPkMixin,
    BaseOrm,
):
    __tablename__ = "players"

    __table_args__ = (
        # last line of defence if the code forgets to check the balance
        CheckConstraint("balance >= 0", name="balance_not_negative"),
    )

    nickname: Mapped[str] = mapped_column(String(32), unique=True)
    balance: Mapped[int] = mapped_column(Integer)

    last_bonus_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )
