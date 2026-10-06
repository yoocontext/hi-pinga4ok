from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from application.exceptions import ApplicationError
from bootstrap.ioc.container import create_container
from delivery.api.v1.http.errors import (
    application_error_handler,
    request_validation_handler,
    unexpected_error_handler,
)
from delivery.api.v1.http.router import router


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None]:
    yield

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    setup_dishka(
        container=create_container(),
        app=app,
    )

    app.include_router(router)

    app.add_exception_handler(ApplicationError, application_error_handler)

    app.add_exception_handler(
        RequestValidationError,
        request_validation_handler,
    )

    app.add_exception_handler(Exception, unexpected_error_handler)

    return app
