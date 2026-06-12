# apps/public_api/main.py

import logging

from fastapi.exceptions import RequestValidationError

from .configs import settings
from .core import (
    AppContainer,
    CoreFastAPI,
    global_exception_handler,
    lifespan_handler,
    validation_exception_handler,
)
from .routers import api_v1_router, docs_router

# Configure a basic logger (in production, use a structured logger or APM like Sentry)
logger = logging.getLogger(__name__)

# Initialize the global DI container
container = AppContainer()

# Inject Pydantic settings into the container configuration
container.config.from_pydantic(settings)


def create_app() -> CoreFastAPI:
    """
    Application factory to create and configure the FastAPI instance.
    """
    fastapi_app = CoreFastAPI(title=settings.app_name, lifespan=lifespan_handler)

    # Attach the container to the custom FastAPI application instance.
    # Type checkers (MyPy/Pylance) are now happy because CoreFastAPI explicitly declares this attribute.
    fastapi_app.container = container

    # Add exception handlers
    fastapi_app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,  # ty:ignore[invalid-argument-type]
    )
    fastapi_app.add_exception_handler(Exception, global_exception_handler)

    # Include application routers
    fastapi_app.include_router(api_v1_router)
    fastapi_app.include_router(docs_router)

    return fastapi_app


# Instantiate the app object at the module level so ASGI servers (like Uvicorn) can access it easily
app = create_app()
