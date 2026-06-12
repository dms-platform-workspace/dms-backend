# apps/public_api/routers/api_docs_routers.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

# Router dedicated to API documentation
docs_router = APIRouter()


@docs_router.get("/scalar", include_in_schema=False)
async def get_scalar_docs(request: Request) -> HTMLResponse:
    """
    Interactive API documentation using Scalar.
    Dynamically fetches the openapi_url from the current application instance.
    """
    return get_scalar_api_reference(
        openapi_url=request.app.openapi_url,
        title="DMS API Documentation",
    )
