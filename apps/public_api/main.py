# apps/public_api/main.py

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from api_kit.http import ErrorResponseDto
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from rich.panel import Panel
from scalar_fastapi import get_scalar_api_reference

from .containers import AppContainer
from .settings import settings

# Configure a basic logger (in production, use a structured logger or APM like Sentry)
logger = logging.getLogger(__name__)

# Initialize the global DI container
container = AppContainer()


# Inject Pydantic settings into the container configuration
container.config.from_pydantic(settings)


class DMSFastAPI(FastAPI):
    """
    Custom FastAPI application class for the DMS project to ensure 100% Type-Safety.

    DI Usage Rules in our Architecture:
    -----------------------------------
    1. When to use `Depends(Provide[...])`:
       - ONLY inside API Route handlers (Endpoints).
       - This is the standard, clean way to inject dependencies directly into
         the request execution scope without knowing about the framework's state.

    2. When to use `app.container` (or `request.app.container`):
       - In Middlewares.
       - In Exception Handlers.
       - In Lifespan events.
       - Use this ONLY when FastAPI's `Depends` system is physically unavailable
         because you are outside the context of a routed endpoint.
    """

    container: AppContainer


@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncIterator[None]:
    print(Panel("Application is starting", title="LIFE CYCLE", border_style="green"))

    # Ensure resources (like DB Engine) are initialized
    container.init_resources()

    try:
        yield
    finally:
        # Retrieve the engine and safely dispose the database connection pool
        db_engine = container.db_engine()
        await db_engine.dispose()

        print(
            Panel(
                "Application is shutting down", title="LIFE CYCLE", border_style="red"
            )
        )


def create_app() -> DMSFastAPI:
    app = DMSFastAPI(title=settings.app_name, lifespan=lifespan_handler)

    # Attach the container to the custom FastAPI application instance.
    # Type checkers (MyPy/Pylance) are now happy because DMSFastAPI explicitly declares this attribute.
    app.container = container

    return app


if __name__ == "__main__":
    app = create_app()


# -----------------------------------------------------------------------------
# Validation Error Handler (The Frontline Guard)
# -----------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Catches Pydantic validation errors before they ever reach the router or UseCase.
    Translates them into our unified api_kit error structure.
    """
    # Extract specific invalid fields to enrich the meta data for the frontend
    errors = exc.errors()
    invalid_fields = [
        {"loc": err["loc"], "msg": err["msg"], "type": err["type"]} for err in errors
    ]

    error_response = ErrorResponseDto(
        code="VALIDATION_ERROR",
        message="Invalid request payload or parameters.",
        severity="WARNING",
        meta={"invalid_fields": invalid_fields},
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_response.model_dump(),
    )


# -----------------------------------------------------------------------------
# Global Exception Handler (The Safety Net)
# -----------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    The ultimate safety net. Catches any unhandled exceptions (e.g., raw database
    errors leaked from the Repository, or unexpected Python bugs in UseCases).
    Ensures the client always receives a standardized JSON instead of a raw 500 error.
    """
    # Log the full traceback so developers can debug the leaked exception
    logger.error(f"Unhandled Server Error at {request.url.path}: {exc}", exc_info=True)

    error_response = ErrorResponseDto(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected internal server error occurred. Please try again later.",
        severity="CRITICAL",
        meta=None,  # SECURITY: Never expose internal exception details to the client!
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


# -----------------------------------------------------------------------------
# Documentation Route
# -----------------------------------------------------------------------------
@app.get("/scalar", include_in_schema=False)
async def get_scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="DMS",
    )
