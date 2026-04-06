"""OAuth authentication routes."""
from flask import Blueprint, request
import secrets
from typing import Dict, Any

from ..controllers.auth_controller import AuthController
from ..utils.response import success_response, error_response
from ..utils.exceptions import APIException

bp = Blueprint("auth", __name__)
controller = AuthController()


@bp.route("/auth/login", methods=["GET"])
def github_login() -> Dict[str, Any]:
    """Initiate GitHub OAuth flow."""
    try:
        # Generate random state for CSRF protection
        state = secrets.token_urlsafe(32)

        result = controller.get_github_oauth_url(state)
        return success_response(result, "OAuth URL generated")

    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/auth/callback", methods=["GET"])
def github_callback() -> Dict[str, Any]:
    """Handle GitHub OAuth callback."""
    try:
        code = request.args.get("code")
        # state = request.args.get("state")  # Validate state in production

        if not code:
            return error_response("Missing authorization code", 400)

        result = controller.exchange_code_for_token(code)
        return success_response(result, "Authentication successful")

    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/auth/validate", methods=["POST"])
def validate_token() -> Dict[str, Any]:
    """Validate GitHub Personal Access Token."""
    try:
        data = request.get_json() or {}
        token = data.get("token")

        if not token:
            return error_response("Token is required", 400)

        result = controller.validate_token(token)
        return success_response(result, "Token is valid")

    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)
