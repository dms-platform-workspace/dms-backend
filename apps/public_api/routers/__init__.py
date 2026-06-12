# apps/public_api/routers/__init__.py

from .api_docs_routers import docs_router
from .api_v1_routers import api_v1_router

__all__ = [
    "docs_router",
    "api_v1_router",
]
