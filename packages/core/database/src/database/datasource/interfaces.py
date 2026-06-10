# packages/core/database/src/database/interfaces.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class DataSource(ABC, Generic[T]):
    @abstractmethod
    async def add(self, record: T) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
