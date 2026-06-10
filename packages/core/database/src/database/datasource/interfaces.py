# packages/core/database/src/database/interfaces.py

from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class DataSource(ABC):
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
