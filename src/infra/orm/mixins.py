from datetime import (
    UTC,
    datetime,
)
from uuid import (
    UUID,
    uuid7,
)

from sqlalchemy import (
    DateTime,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.types import Uuid


class IntPkMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UuidPkMixin:
    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
