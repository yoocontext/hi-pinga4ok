# pyright: reportUnknownVariableType=false

from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from application.interfaces.transaction_manager import ITransactionManager
from bootstrap.settings import PgSettings
from infra.transaction_manager import AlchemyTransactionManager


class AlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    async def engine(self, settings: PgSettings) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(settings.sqlalchemy_url)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @provide(scope=Scope.REQUEST)
    def transaction_manager(
        self,
        session: AsyncSession,
    ) -> ITransactionManager:
        return AlchemyTransactionManager(session=session)
