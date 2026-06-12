# apps/public_api/core/lifespan.py

from contextlib import asynccontextmanager
from typing import AsyncIterator

from rich.panel import Panel

from .core_fastapi import CoreFastAPI


@asynccontextmanager
async def lifespan_handler(app: CoreFastAPI) -> AsyncIterator[None]:
    print(Panel("Application is starting", title="LIFE CYCLE", border_style="green"))

    # Ensure resources (like DB Engine) are initialized via the app instance
    app.container.init_resources()

    try:
        yield
    finally:
        # Retrieve the engine and safely dispose the database connection pool
        db_engine = app.container.db_engine()
        await db_engine.dispose()

        print(
            Panel(
                "Application is shutting down", title="LIFE CYCLE", border_style="red"
            )
        )
