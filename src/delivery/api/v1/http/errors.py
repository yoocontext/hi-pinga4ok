import re
from dataclasses import fields
from typing import Any

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from application.exceptions import (
    AccessDeniedError,
    ApplicationError,
    InvalidInputError,
    InvalidStateError,
    NotFoundError,
)

STATUSES: dict[type[ApplicationError], int] = {
    NotFoundError: 404,
    InvalidInputError: 422,
    InvalidStateError: 409,
    AccessDeniedError: 403,
}


async def application_error_handler(
    request: Request,
    error: Exception,
) -> JSONResponse:
    assert isinstance(error, ApplicationError)

    return _error_response(
        status=_status(error=error),
        code=_code(error=error),
        message=error.message,
        details=_details(error=error),
    )


async def request_validation_handler(
    request: Request,
    error: Exception,
) -> JSONResponse:
    assert isinstance(error, RequestValidationError)

    return _error_response(
        status=422,
        code="invalid_request",
        message="Invalid request",
        details={"errors": error.errors()},
    )


async def unexpected_error_handler(
    request: Request,
    error: Exception,
) -> JSONResponse:
    # starlette re-raises the error after this response, so the server logs it
    return _error_response(
        status=500,
        code="internal_error",
        message="Internal error",
        details={},
    )


def _status(*, error: ApplicationError) -> int:
    for error_type in type(error).__mro__:
        if error_type in STATUSES:
            return STATUSES[error_type]

    return 400


def _code(*, error: ApplicationError) -> str:
    name = type(error).__name__.removesuffix("Error")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _details(*, error: ApplicationError) -> dict[str, Any]:
    return {item.name: getattr(error, item.name) for item in fields(error)}


def _error_response(
    *,
    status: int,
    code: str,
    message: str,
    details: dict[str, Any],
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content=jsonable_encoder(
            {"error": {"code": code, "message": message, "details": details}}
        ),
    )
