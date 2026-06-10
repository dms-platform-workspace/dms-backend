# packages/core/database/src/database/exceptions.py


class DataSourceException(Exception):
    """Base exception for data source operations.
    All exceptions related to database connectivity or query execution should inherit from this class.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        super().__init__(message)
        self.original_exception = original_exception


class QueryExecutionException(DataSourceException):
    """Exception raised for errors during query execution.
    Wraps database-specific exceptions and provides a consistent interface.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        super().__init__(
            message=message,
            original_exception=original_exception,
        )


class TransactionException(DataSourceException):
    """Exception raised for errors during transaction management.
    Includes issues with commit or rollback operations.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        super().__init__(
            message=message,
            original_exception=original_exception,
        )
