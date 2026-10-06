import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from bootstrap.settings import Settings
from infra.orm import BaseOrm

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations(
    connection: Connection,
) -> None:
    context.configure(
        connection=connection,
        target_metadata=BaseOrm.metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    engine = create_async_engine(
        Settings().pg.sqlalchemy_url,
        poolclass=pool.NullPool,
    )

    async with engine.connect() as connection:
        await connection.run_sync(run_migrations)

    await engine.dispose()


asyncio.run(run_async_migrations())
