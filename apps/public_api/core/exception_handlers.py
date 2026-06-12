# apps/public_api/core/exceptions.py

import logging

from api_kit.http import ErrorResponseDto
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Configure a basic logger (in production, use a structured logger or APM like Sentry)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Validation Error Handler (The Frontline Guard)
# -----------------------------------------------------------------------------
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
