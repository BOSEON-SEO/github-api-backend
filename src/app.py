"""Flask application entry point."""
from flask import Flask, jsonify
from flask_cors import CORS
from typing import Dict, Any

from .config import get_config
from .routes import github_routes


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

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check() -> Dict[str, Any]:
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "github-api-backend"
        })

    # Root endpoint
    @app.route("/", methods=["GET"])
    def root() -> Dict[str, Any]:
        """Root endpoint."""
        return jsonify({
            "message": "GitHub API Backend",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "api": "/api"
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
