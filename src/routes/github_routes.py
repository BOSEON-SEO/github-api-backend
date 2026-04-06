"""GitHub API routes."""
from flask import Blueprint, request, jsonify
from typing import Dict, Any

from ..controllers.github_controller import GitHubController
from ..middleware.auth_middleware import require_github_token

bp = Blueprint("github", __name__)
controller = GitHubController()


@bp.route("/repos", methods=["GET"])
@require_github_token
def list_repositories() -> Dict[str, Any]:
    """List user repositories."""
    username = request.args.get("username")
    sort = request.args.get("sort", "updated")
    per_page = int(request.args.get("per_page", "30"))

    result = controller.list_repositories(username, sort, per_page)
    return jsonify(result)


@bp.route("/repos/<owner>/<repo>", methods=["GET"])
@require_github_token
def get_repository(owner: str, repo: str) -> Dict[str, Any]:
    """Get repository details."""
    result = controller.get_repository(owner, repo)
    return jsonify(result)


@bp.route("/repos", methods=["POST"])
@require_github_token
def create_repository() -> Dict[str, Any]:
    """Create a new repository."""
    data = request.get_json()
    result = controller.create_repository(data)
    return jsonify(result), 201


@bp.route("/repos/<owner>/<repo>/pulls", methods=["GET"])
@require_github_token
def list_pull_requests(owner: str, repo: str) -> Dict[str, Any]:
    """List pull requests for a repository."""
    state = request.args.get("state", "open")
    per_page = int(request.args.get("per_page", "30"))

    result = controller.list_pull_requests(owner, repo, state, per_page)
    return jsonify(result)


@bp.route("/repos/<owner>/<repo>/pulls/<int:number>", methods=["GET"])
@require_github_token
def get_pull_request(owner: str, repo: str, number: int) -> Dict[str, Any]:
    """Get pull request details."""
    result = controller.get_pull_request(owner, repo, number)
    return jsonify(result)


@bp.route("/repos/<owner>/<repo>/pulls", methods=["POST"])
@require_github_token
def create_pull_request(owner: str, repo: str) -> Dict[str, Any]:
    """Create a new pull request."""
    data = request.get_json()
    result = controller.create_pull_request(owner, repo, data)
    return jsonify(result), 201


@bp.route("/repos/<owner>/<repo>/issues", methods=["GET"])
@require_github_token
def list_issues(owner: str, repo: str) -> Dict[str, Any]:
    """List issues for a repository."""
    state = request.args.get("state", "open")
    per_page = int(request.args.get("per_page", "30"))

    result = controller.list_issues(owner, repo, state, per_page)
    return jsonify(result)


@bp.route("/repos/<owner>/<repo>/issues/<int:number>", methods=["GET"])
@require_github_token
def get_issue(owner: str, repo: str, number: int) -> Dict[str, Any]:
    """Get issue details."""
    result = controller.get_issue(owner, repo, number)
    return jsonify(result)


@bp.route("/repos/<owner>/<repo>/issues", methods=["POST"])
@require_github_token
def create_issue(owner: str, repo: str) -> Dict[str, Any]:
    """Create a new issue."""
    data = request.get_json()
    result = controller.create_issue(owner, repo, data)
    return jsonify(result), 201


@bp.route("/repos/<owner>/<repo>/commits", methods=["GET"])
@require_github_token
def list_commits(owner: str, repo: str) -> Dict[str, Any]:
    """List commits for a repository."""
    branch = request.args.get("branch", "main")
    per_page = int(request.args.get("per_page", "30"))

    result = controller.list_commits(owner, repo, branch, per_page)
    return jsonify(result)
