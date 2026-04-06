"""Authentication middleware."""
from functools import wraps
from flask import jsonify, request
from typing import Callable, Any
import logging

from ..config import get_config

logger = logging.getLogger(__name__)


def require_github_token(f: Callable) -> Callable:
    """Middleware to ensure GitHub token is configured."""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        config = get_config()

        if not config.GITHUB_TOKEN:
            logger.warning("GitHub token not configured")
            return jsonify({
                "error": "GitHub token not configured",
                "message": "Please set GITHUB_TOKEN in environment variables"
            }), 401

        return f(*args, **kwargs)

    return decorated_function


def require_api_key(f: Callable) -> Callable:
    """Middleware to validate API key from request header."""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            logger.warning("API key missing from request")
            return jsonify({
                "error": "Unauthorized",
                "message": "API key required"
            }), 401

        # Add your API key validation logic here
        # For now, just check if it exists

        return f(*args, **kwargs)

    return decorated_function
