# packages/api_kit/src/api_kit/http/responses.py

from typing import Any, TypeVar

from fastapi import status
from fastapi.responses import JSONResponse
from foundation import BaseDomainError
from pydantic import BaseModel, ConfigDict, Field
from returns.result import Failure, Result, Success


class ErrorResponseDto(BaseModel):
    """
    Standardized error response schema for the entire application.
    Ensures that clients always receive a consistent JSON structure
    regardless of which feature generated the error.
    """

    success: bool = Field(
        default=False, description="Indicates if the request was successful"
    )
    code: str = Field(
        ..., description="Machine-readable error code (e.g., 'USER_NOT_FOUND')"
    )
    message: str = Field(..., description="Human-readable error message")
    severity: str = Field(..., description="Severity level of the error")
    meta: dict[str, Any] | None = Field(
        default=None, description="Additional error metadata"
    )

    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T")


def unwrap_or_respond(
    result: Result[T, BaseDomainError],
    error_map: dict[type[BaseDomainError], int],
    default_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
) -> T | JSONResponse:  # ty:ignore[invalid-return-type]
    """
    Evaluates the Result monad returned from the Service/UseCase layer.

    - On Success: Returns the raw data, allowing the APIRouter to process it with its response_model.
    - On Failure: Maps the domain error to an HTTP status code using the provided `error_map`
      and returns a standardized JSONResponse.
    """
    match result:
        case Success(data):
            return data
        case Failure(error):
            # Find the corresponding HTTP status code, fallback to default_status (500) if not explicitly mapped
            status_code = error_map.get(type(error), default_status)

            # Construct the standardized presentation DTO
            error_response = ErrorResponseDto(
                code=error.code,
                message=error.message,
                severity=error.severity.value,
                meta=error.meta,
            )

            # Return a raw JSONResponse to bypass the router's success response_model
            return JSONResponse(
                status_code=status_code,
                content=error_response.model_dump,
            )
