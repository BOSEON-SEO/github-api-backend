"""Response formatters."""
from typing import Any, Dict, Optional
from flask import jsonify


def success_response(
    data: Any,
    message: Optional[str] = None,
    status_code: int = 200
) -> tuple:
    """Format success response."""
    response = {
        "success": True,
        "data": data
    }

    if message:
        response["message"] = message

    return jsonify(response), status_code


def error_response(
    message: str,
    status_code: int = 500,
    errors: Optional[Dict[str, Any]] = None
) -> tuple:
    """Format error response."""
    response = {
        "success": False,
        "error": message,
        "status_code": status_code
    }

    if errors:
        response["errors"] = errors

    return jsonify(response), status_code


def paginated_response(
    items: list,
    page: int,
    per_page: int,
    total: Optional[int] = None
) -> tuple:
    """Format paginated response."""
    response = {
        "success": True,
        "data": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "count": len(items)
        }
    }

    if total is not None:
        response["pagination"]["total"] = total

    return jsonify(response), 200
