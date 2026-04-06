"""Authentication middleware."""
from functools import wraps
from flask import request, g
from typing import Callable, Any
import logging

from ..config import get_config
from ..utils.exceptions import UnauthorizedError
from ..utils.jwt_helper import decode_access_token
from ..utils.response import error_response

logger = logging.getLogger(__name__)


def require_github_token(f: Callable) -> Callable:
    """Middleware to ensure GitHub token is configured."""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        config = get_config()

        if not config.GITHUB_TOKEN:
            logger.warning("GitHub token not configured")
            return error_response(
                "GitHub token not configured. Please set GITHUB_TOKEN in environment variables",
                401
            )

        return f(*args, **kwargs)

    return decorated_function


def require_auth(f: Callable) -> Callable:
    """Middleware to require JWT authentication."""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.warning("Missing Authorization header")
            return error_response("Missing Authorization header", 401)

        try:
            # Extract token from "Bearer <token>"
            parts = auth_header.split()

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return error_response("Invalid Authorization header format", 401)

            token = parts[1]

            # Decode and validate token
            payload = decode_access_token(token)

            # Store user info in Flask's g object
            g.user_id = payload.get("user_id")
            g.username = payload.get("username")

        except UnauthorizedError as e:
            return error_response(e.message, e.status_code)

        return f(*args, **kwargs)

    return decorated_function


def optional_auth(f: Callable) -> Callable:
    """Middleware for optional authentication."""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                parts = auth_header.split()

                if len(parts) == 2 and parts[0].lower() == "bearer":
                    token = parts[1]
                    payload = decode_access_token(token)

                    g.user_id = payload.get("user_id")
                    g.username = payload.get("username")
                    g.authenticated = True
                else:
                    g.authenticated = False

            except UnauthorizedError:
                g.authenticated = False
        else:
            g.authenticated = False

        return f(*args, **kwargs)

    return decorated_function
