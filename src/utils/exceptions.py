"""Custom exceptions for the application."""
from typing import Optional, Dict, Any


class APIException(Exception):
    """Base API exception."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None
    ):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        rv = dict(self.payload)
        rv["error"] = self.message
        rv["status_code"] = self.status_code
        return rv


class BadRequestError(APIException):
    """400 Bad Request."""

    def __init__(self, message: str = "Bad request", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, payload)


class UnauthorizedError(APIException):
    """401 Unauthorized."""

    def __init__(self, message: str = "Unauthorized", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 401, payload)


class ForbiddenError(APIException):
    """403 Forbidden."""

    def __init__(self, message: str = "Forbidden", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 403, payload)


class NotFoundError(APIException):
    """404 Not Found."""

    def __init__(self, message: str = "Resource not found", payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, payload)


class GitHubAPIError(APIException):
    """GitHub API error."""

    def __init__(self, message: str, status_code: int = 500, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code, payload)
