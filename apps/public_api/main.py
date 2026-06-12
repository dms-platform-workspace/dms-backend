# apps/public_api/main.py

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from rich.panel import Panel
from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncIterator[None]:
    print(Panel("Application is starting", title="LIFE CYCLE", border_style="green"))
    try:
        yield
    finally:
        print(
            Panel(
                "Application is shutting down", title="LIFE CYCLE", border_style="red"
            )
        )


def create_app() -> FastAPI:
    app = FastAPI(title="DMS", lifespan=lifespan_handler)
    return app


if __name__ == "__main__":
    app = create_app()


@app.get("/scalar", include_in_schema=False)
async def get_scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="DMS",
    )
