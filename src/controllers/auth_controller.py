"""OAuth authentication controller."""
from typing import Dict, Any
import requests
import logging

from ..config import get_config
from ..utils.exceptions import UnauthorizedError, BadRequestError
from ..utils.jwt_helper import create_access_token

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for OAuth authentication."""

    def __init__(self):
        """Initialize auth controller."""
        self.config = get_config()

    def get_github_oauth_url(self, state: str) -> Dict[str, Any]:
        """Generate GitHub OAuth authorization URL."""
        if not self.config.GITHUB_CLIENT_ID:
            raise BadRequestError("GitHub OAuth not configured")

        base_url = "https://github.com/login/oauth/authorize"
        params = {
            "client_id": self.config.GITHUB_CLIENT_ID,
            "redirect_uri": self.config.GITHUB_REDIRECT_URI,
            "scope": "repo,user,read:org",
            "state": state
        }

        auth_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

        return {
            "auth_url": auth_url,
            "state": state
        }

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange OAuth code for access token."""
        if not self.config.GITHUB_CLIENT_ID or not self.config.GITHUB_CLIENT_SECRET:
            raise BadRequestError("GitHub OAuth not configured")

        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        headers = {"Accept": "application/json"}
        data = {
            "client_id": self.config.GITHUB_CLIENT_ID,
            "client_secret": self.config.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": self.config.GITHUB_REDIRECT_URI
        }

        try:
            response = requests.post(token_url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            token_data = response.json()

            if "error" in token_data:
                logger.error("GitHub OAuth error: %s", token_data.get("error_description"))
                raise UnauthorizedError(token_data.get("error_description", "OAuth failed"))

            access_token = token_data.get("access_token")

            if not access_token:
                raise UnauthorizedError("Failed to obtain access token")

            # Get user info
            user_info = self._get_user_info(access_token)

            # Create JWT token
            jwt_token = create_access_token(user_info)

            return {
                "access_token": jwt_token,
                "github_token": access_token,
                "user": user_info
            }

        except requests.RequestException as e:
            logger.error("Failed to exchange code for token: %s", e)
            raise UnauthorizedError("Failed to authenticate with GitHub")

    def _get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from GitHub."""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            user_data = response.json()

            return {
                "id": user_data.get("id"),
                "login": user_data.get("login"),
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "avatar_url": user_data.get("avatar_url"),
                "bio": user_data.get("bio"),
                "public_repos": user_data.get("public_repos"),
                "followers": user_data.get("followers"),
                "following": user_data.get("following")
            }

        except requests.RequestException as e:
            logger.error("Failed to get user info: %s", e)
            raise UnauthorizedError("Failed to get user information")

    def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate Personal Access Token with GitHub."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=10
            )

            if response.status_code == 401:
                raise UnauthorizedError("Invalid or expired token")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error("Token validation failed: %s", e)
            raise UnauthorizedError("Token validation failed")
