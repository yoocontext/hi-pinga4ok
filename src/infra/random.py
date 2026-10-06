from random import SystemRandom


class SystemRandomValue:
    def __init__(self) -> None:
        self._random = SystemRandom()

    def value(self) -> float:
        return self._random.random()
