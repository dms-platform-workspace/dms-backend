# packages/core/foundation/src/foundation/base/error.py

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ErrorSeverity(str, Enum):
    """
    Defines the severity level of the error to guide higher-level
    decision-making (e.g., logging strategies or HTTP status mapping).
    """

    RETRYABLE = "RETRYABLE"
    RECOVERABLE = "RECOVERABLE"
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"


@dataclass(frozen=True)
class BaseDomainError:
    """
    Base class for all domain errors, implemented as an immutable Value Object.
    Intentionally avoids inheriting from Exception to physically prevent
    errors from being raised in the pure domain and application layers.
    """

    message: str
    severity: ErrorSeverity
    code: str
    # Additional metadata and context to be exposed to the client (e.g., list of invalid fields).
    meta: dict[str, Any] | None = field(default=None)
    # The original underlying exception, strictly used for internal tracing and logging.
    # Excluded from representations to prevent leaking infrastructure details to the client.
    cause: Exception | None = field(default=None, repr=False)
