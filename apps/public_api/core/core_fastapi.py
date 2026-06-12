# apps/public_api/core/core_fastapi.py

from fastapi import FastAPI

from .dependency_injector import AppContainer


class CoreFastAPI(FastAPI):
    """
    Custom FastAPI application class for the project to ensure 100% Type-Safety.

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
