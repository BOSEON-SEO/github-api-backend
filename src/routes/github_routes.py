"""GitHub API routes."""
from flask import Blueprint, request
from typing import Dict, Any

from ..controllers.github_controller import GitHubController
from ..middleware.auth_middleware import require_github_token
from ..utils.response import success_response, error_response
from ..utils.exceptions import APIException

bp = Blueprint("github", __name__)
controller = GitHubController()


@bp.route("/repos", methods=["GET"])
@require_github_token
def list_repositories() -> Dict[str, Any]:
    """List user repositories."""
    username = request.args.get("username")
    sort = request.args.get("sort", "updated")
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_repositories(username, sort, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>", methods=["GET"])
@require_github_token
def get_repository(owner: str, repo: str) -> Dict[str, Any]:
    """Get repository details."""
    try:
        result = controller.get_repository(owner, repo)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos", methods=["POST"])
@require_github_token
def create_repository() -> Dict[str, Any]:
    """Create a new repository."""
    try:
        data = request.get_json() or {}
        result = controller.create_repository(data)
        return success_response(result, "Repository created successfully", 201)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/pulls", methods=["GET"])
@require_github_token
def list_pull_requests(owner: str, repo: str) -> Dict[str, Any]:
    """List pull requests for a repository."""
    state = request.args.get("state", "open")
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_pull_requests(owner, repo, state, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/pulls/<int:number>", methods=["GET"])
@require_github_token
def get_pull_request(owner: str, repo: str, number: int) -> Dict[str, Any]:
    """Get pull request details."""
    try:
        result = controller.get_pull_request(owner, repo, number)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/pulls", methods=["POST"])
@require_github_token
def create_pull_request(owner: str, repo: str) -> Dict[str, Any]:
    """Create a new pull request."""
    try:
        data = request.get_json() or {}
        result = controller.create_pull_request(owner, repo, data)
        return success_response(result, "Pull request created successfully", 201)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/issues", methods=["GET"])
@require_github_token
def list_issues(owner: str, repo: str) -> Dict[str, Any]:
    """List issues for a repository."""
    state = request.args.get("state", "open")
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_issues(owner, repo, state, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/issues/<int:number>", methods=["GET"])
@require_github_token
def get_issue(owner: str, repo: str, number: int) -> Dict[str, Any]:
    """Get issue details."""
    try:
        result = controller.get_issue(owner, repo, number)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/issues", methods=["POST"])
@require_github_token
def create_issue(owner: str, repo: str) -> Dict[str, Any]:
    """Create a new issue."""
    try:
        data = request.get_json() or {}
        result = controller.create_issue(owner, repo, data)
        return success_response(result, "Issue created successfully", 201)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/commits", methods=["GET"])
@require_github_token
def list_commits(owner: str, repo: str) -> Dict[str, Any]:
    """List commits for a repository."""
    branch = request.args.get("branch", "main")
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_commits(owner, repo, branch, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/users/<username>", methods=["GET"])
@require_github_token
def get_user(username: str) -> Dict[str, Any]:
    """Get user information."""
    try:
        result = controller.get_user(username)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/user", methods=["GET"])
@require_github_token
def get_authenticated_user() -> Dict[str, Any]:
    """Get authenticated user information."""
    try:
        result = controller.get_user()
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/branches", methods=["GET"])
@require_github_token
def list_branches(owner: str, repo: str) -> Dict[str, Any]:
    """List branches for a repository."""
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_branches(owner, repo, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/branches/<branch_name>", methods=["GET"])
@require_github_token
def get_branch(owner: str, repo: str, branch_name: str) -> Dict[str, Any]:
    """Get branch details."""
    try:
        result = controller.get_branch(owner, repo, branch_name)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/tags", methods=["GET"])
@require_github_token
def list_tags(owner: str, repo: str) -> Dict[str, Any]:
    """List tags for a repository."""
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_tags(owner, repo, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/contributors", methods=["GET"])
@require_github_token
def list_contributors(owner: str, repo: str) -> Dict[str, Any]:
    """List contributors for a repository."""
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_contributors(owner, repo, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/search/repositories", methods=["GET"])
@require_github_token
def search_repositories() -> Dict[str, Any]:
    """Search repositories."""
    query = request.args.get("q", "")
    sort = request.args.get("sort", "stars")
    order = request.args.get("order", "desc")
    per_page = int(request.args.get("per_page", "30"))

    if not query:
        return error_response("Query parameter 'q' is required", 400)

    try:
        result = controller.search_repositories(query, sort, order, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


# ---------------------------------------------------------------------------
# Milestone routes
# ---------------------------------------------------------------------------

@bp.route("/repos/<owner>/<repo>/milestones", methods=["GET"])
@require_github_token
def list_milestones(owner: str, repo: str) -> Dict[str, Any]:
    """List milestones for a repository.

    Query params:
      - state     : "open" | "closed" | "all"  (default: "open")
      - sort      : "due_on" | "completeness"   (default: "due_on")
      - direction : "asc" | "desc"              (default: "asc")
      - per_page  : int                          (default: 30)
    """
    state = request.args.get("state", "open")
    sort = request.args.get("sort", "due_on")
    direction = request.args.get("direction", "asc")
    per_page = int(request.args.get("per_page", "30"))

    try:
        result = controller.list_milestones(owner, repo, state, sort, direction, per_page)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/milestones/<int:milestone_number>", methods=["GET"])
@require_github_token
def get_milestone(owner: str, repo: str, milestone_number: int) -> Dict[str, Any]:
    """Get a single milestone by its number."""
    try:
        result = controller.get_milestone(owner, repo, milestone_number)
        return success_response(result)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/milestones", methods=["POST"])
@require_github_token
def create_milestone(owner: str, repo: str) -> Dict[str, Any]:
    """Create a milestone.

    Required body field:
      - title       : str
    Optional body fields:
      - state       : "open" | "closed"  (default: "open")
      - description : str
      - due_on      : ISO-8601 datetime string  e.g. "2026-12-31T00:00:00Z"
    """
    try:
        data = request.get_json() or {}
        result = controller.create_milestone(owner, repo, data)
        return success_response(result, "Milestone created successfully", 201)
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/milestones/<int:milestone_number>", methods=["PATCH"])
@require_github_token
def update_milestone(owner: str, repo: str, milestone_number: int) -> Dict[str, Any]:
    """Update an existing milestone (partial update).

    Updatable body fields:
      - title       : str
      - state       : "open" | "closed"
      - description : str
      - due_on      : ISO-8601 datetime string or null to clear
    """
    try:
        data = request.get_json() or {}
        result = controller.update_milestone(owner, repo, milestone_number, data)
        return success_response(result, "Milestone updated successfully")
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)


@bp.route("/repos/<owner>/<repo>/milestones/<int:milestone_number>", methods=["DELETE"])
@require_github_token
def delete_milestone(owner: str, repo: str, milestone_number: int) -> Dict[str, Any]:
    """Delete a milestone."""
    try:
        result = controller.delete_milestone(owner, repo, milestone_number)
        return success_response(result, "Milestone deleted successfully")
    except APIException as e:
        return error_response(e.message, e.status_code, e.payload)
