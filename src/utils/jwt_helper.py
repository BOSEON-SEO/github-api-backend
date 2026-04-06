"""JWT token helper functions."""
from datetime import datetime, timedelta
from typing import Dict, Any
import jwt
import logging

from ..config import get_config
from ..utils.exceptions import UnauthorizedError

logger = logging.getLogger(__name__)


def create_access_token(user_data: Dict[str, Any]) -> str:
    """Create JWT access token."""
    config = get_config()

    expiration = datetime.utcnow() + timedelta(hours=config.JWT_EXPIRATION_HOURS)

    payload = {
        "user_id": user_data.get("id"),
        "username": user_data.get("login"),
        "exp": expiration,
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT access token."""
    config = get_config()

    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        raise UnauthorizedError("Token has expired")

    except jwt.InvalidTokenError as e:
        logger.warning("Invalid token: %s", e)
        raise UnauthorizedError("Invalid token")
