from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, kw_only=True)
class PlayersConfig:
    start_balance: int
    daily_bonus: int
    daily_bonus_cooldown: timedelta
