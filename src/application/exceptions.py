from dataclasses import dataclass


@dataclass(eq=False, kw_only=True)
class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error"

    def __post_init__(self) -> None:
        Exception.__init__(self, self.message)


class NotFoundError(ApplicationError):
    @property
    def message(self) -> str:
        return "Not found"


class InvalidInputError(ApplicationError):
    @property
    def message(self) -> str:
        return "Invalid input"


class InvalidStateError(ApplicationError):
    @property
    def message(self) -> str:
        return "Invalid state"


class AccessDeniedError(ApplicationError):
    @property
    def message(self) -> str:
        return "Access denied"
