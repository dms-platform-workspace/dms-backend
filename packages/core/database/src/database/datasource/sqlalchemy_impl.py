# packages/core/database/src/database/datasource/sqlalchemy_impl.py

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import (
    DataSourceException,
    QueryExecutionException,
    TransactionException,
)
from .interfaces import DataSource


class SQLAlchemyDataSourceImpl(DataSource[object]):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, record: object) -> None:
        try:
            self._session.add(record)
        except SQLAlchemyError as e:
            raise QueryExecutionException(
                message="Failed to add record due to database error",
                original_exception=e,
            )
        except Exception as e:
            raise DataSourceException(
                message="Unexpected error while adding record",
                original_exception=e,
            )

    async def flush(self) -> None:
        try:
            await self._session.flush()
        except SQLAlchemyError as e:
            raise QueryExecutionException(
                message="Failed to flush session",
                original_exception=e,
            )
        except Exception as e:
            raise DataSourceException(
                message="Unexpected error while flushing session",
                original_exception=e,
            )

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            raise TransactionException(
                message="Failed to commit transaction",
                original_exception=e,
            )
        except Exception as e:
            raise DataSourceException(
                message="Unexpected error during commit",
                original_exception=e,
            )

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as e:
            raise TransactionException(
                message="Failed to rollback transaction",
                original_exception=e,
            )
        except Exception as e:
            raise DataSourceException(
                message="Unexpected error during rollback",
                original_exception=e,
            )

    async def close(self) -> None:
        try:
            await self._session.close()
        except SQLAlchemyError as e:
            raise DataSourceException(
                message="Failed to close database session safely",
                original_exception=e,
            )
        except Exception as e:
            raise DataSourceException(
                message="Unexpected error while closing session",
                original_exception=e,
            )
