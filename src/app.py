"""Flask application entry point."""
from flask import Flask
from flask_cors import CORS
from typing import Dict, Any
import logging

from .config import get_config
from .routes import github_routes, auth_routes
from .utils.exceptions import APIException
from .utils.response import success_response, error_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Enable CORS
    CORS(app, origins=config.CORS_ORIGINS)

    # Register blueprints
    app.register_blueprint(github_routes.bp, url_prefix="/api")
    app.register_blueprint(auth_routes.bp, url_prefix="/api")

    # Register error handlers
    @app.errorhandler(APIException)
    def handle_api_exception(error: APIException) -> tuple:
        """Handle custom API exceptions."""
        logger.error("API Exception: %s", error.message)
        return error_response(error.message, error.status_code, error.payload)

    @app.errorhandler(404)
    def handle_not_found(error: Any) -> tuple:
        """Handle 404 errors."""
        return error_response("Resource not found", 404)

    @app.errorhandler(500)
    def handle_internal_error(error: Any) -> tuple:
        """Handle 500 errors."""
        logger.error("Internal server error: %s", error)
        return error_response("Internal server error", 500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple:
        """Handle unexpected errors."""
        logger.exception("Unexpected error: %s", error)
        return error_response("An unexpected error occurred", 500)

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check() -> tuple:
        """Health check endpoint."""
        return success_response({
            "status": "healthy",
            "service": "github-api-backend"
        })

    # Root endpoint
    @app.route("/", methods=["GET"])
    def root() -> tuple:
        """Root endpoint."""
        return success_response({
            "message": "GitHub API Backend",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "auth": "/api/auth",
                "github": "/api"
            }
        })

    return app


if __name__ == "__main__":
    app = create_app()
    config = get_config()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
