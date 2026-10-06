from dataclasses import (
    dataclass,
    replace,
)
from datetime import (
    datetime,
    timedelta,
)
from typing import Self
from uuid import UUID

from application.exceptions import (
    InvalidStateError,
    NotFoundError,
)


@dataclass(eq=False, kw_only=True)
class PlayerNotFoundError(NotFoundError):
    player_id: UUID

    @property
    def message(self) -> str:
        return "Player not found"


@dataclass(eq=False, kw_only=True)
class NotEnoughCoinsError(InvalidStateError):
    player_id: UUID
    balance: int
    amount: int

    @property
    def message(self) -> str:
        return "Not enough coins"


@dataclass(eq=False, kw_only=True)
class DailyBonusNotReadyError(InvalidStateError):
    player_id: UUID
    available_at: datetime

    @property
    def message(self) -> str:
        return "Daily bonus is not ready yet"


@dataclass(frozen=True, kw_only=True)
class Player:
    id: UUID
    nickname: str

    balance: int
    last_bonus_at: datetime | None = None

    def spend(
        self,
        *,
        amount: int,
    ) -> Self:
        if amount > self.balance:
            raise NotEnoughCoinsError(
                player_id=self.id,
                balance=self.balance,
                amount=amount,
            )

        return replace(self, balance=self.balance - amount)

    def claim_daily_bonus(
        self,
        *,
        amount: int,
        cooldown: timedelta,
        at: datetime,
    ) -> Self:
        if self.last_bonus_at is not None:
            available_at = self.last_bonus_at + cooldown

            if at < available_at:
                raise DailyBonusNotReadyError(
                    player_id=self.id,
                    available_at=available_at,
                )

        return replace(
            self,
            balance=self.balance + amount,
            last_bonus_at=at,
        )
