"""Request validators."""
from typing import Dict, Any, List
from ..utils.exceptions import BadRequestError


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate that required fields are present in data."""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        raise BadRequestError(
            f"Missing required fields: {', '.join(missing_fields)}",
            payload={"missing_fields": missing_fields}
        )


def validate_pagination_params(page: int, per_page: int) -> None:
    """Validate pagination parameters."""
    if page < 1:
        raise BadRequestError("Page number must be >= 1")

    if per_page < 1 or per_page > 100:
        raise BadRequestError("Per page must be between 1 and 100")
