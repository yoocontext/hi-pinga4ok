from typing import Protocol


class IRandom(Protocol):
    def value(self) -> float:
        """Return a random number in [0, 1)."""
        ...
