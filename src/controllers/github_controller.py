"""GitHub API controller."""
from typing import Dict, Any, List, Optional
from github import Github, GithubException
import logging

from ..config import get_config
from ..utils.exceptions import GitHubAPIError, NotFoundError, BadRequestError

logger = logging.getLogger(__name__)


class GitHubController:
    """Controller for GitHub API operations."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client."""
        config = get_config()
        github_token = token or config.GITHUB_TOKEN

        if not github_token:
            raise BadRequestError("GitHub token is required")

        self.client = Github(github_token)
        self.user = self.client.get_user()

    def list_repositories(
        self,
        username: Optional[str] = None,
        sort: str = "updated",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List repositories for a user."""
        try:
            if username:
                user = self.client.get_user(username)
            else:
                user = self.user

            repos = user.get_repos(sort=sort)

            result = []
            for repo in repos[:per_page]:
                result.append({
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "private": repo.private,
                    "html_url": repo.html_url,
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "language": repo.language,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                })

            return {"repositories": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository details."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")

            return {
                "id": repository.id,
                "name": repository.name,
                "full_name": repository.full_name,
                "description": repository.description,
                "private": repository.private,
                "html_url": repository.html_url,
                "clone_url": repository.clone_url,
                "created_at": repository.created_at.isoformat(),
                "updated_at": repository.updated_at.isoformat(),
                "language": repository.language,
                "stars": repository.stargazers_count,
                "watchers": repository.watchers_count,
                "forks": repository.forks_count,
                "open_issues": repository.open_issues_count,
                "default_branch": repository.default_branch,
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def create_repository(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new repository."""
        try:
            repo = self.user.create_repo(
                name=data["name"],
                description=data.get("description", ""),
                private=data.get("private", False),
                auto_init=data.get("auto_init", True),
            )

            return {
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def list_pull_requests(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List pull requests for a repository."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            pulls = repository.get_pulls(state=state)

            result = []
            for pr in pulls[:per_page]:
                result.append({
                    "id": pr.id,
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "user": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                    "updated_at": pr.updated_at.isoformat(),
                    "html_url": pr.html_url,
                    "head": pr.head.ref,
                    "base": pr.base.ref,
                })

            return {"pull_requests": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def get_pull_request(self, owner: str, repo: str, number: int) -> Dict[str, Any]:
        """Get pull request details."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            pr = repository.get_pull(number)

            return {
                "id": pr.id,
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "user": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "merged": pr.merged,
                "mergeable": pr.mergeable,
                "html_url": pr.html_url,
                "head": pr.head.ref,
                "base": pr.base.ref,
                "commits": pr.commits,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def create_pull_request(
        self,
        owner: str,
        repo: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new pull request."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            pr = repository.create_pull(
                title=data["title"],
                body=data.get("body", ""),
                head=data["head"],
                base=data.get("base", "main"),
            )

            return {
                "id": pr.id,
                "number": pr.number,
                "title": pr.title,
                "html_url": pr.html_url,
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def list_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List issues for a repository."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            issues = repository.get_issues(state=state)

            result = []
            for issue in issues[:per_page]:
                if not issue.pull_request:  # Exclude PRs
                    result.append({
                        "id": issue.id,
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "user": issue.user.login,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "html_url": issue.html_url,
                        "comments": issue.comments,
                    })

            return {"issues": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def get_issue(self, owner: str, repo: str, number: int) -> Dict[str, Any]:
        """Get issue details."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            issue = repository.get_issue(number)

            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "user": issue.user.login,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "html_url": issue.html_url,
                "comments": issue.comments,
                "labels": [label.name for label in issue.labels],
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def create_issue(
        self,
        owner: str,
        repo: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new issue."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            issue = repository.create_issue(
                title=data["title"],
                body=data.get("body", ""),
                labels=data.get("labels", []),
            )

            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "html_url": issue.html_url,
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def list_commits(
        self,
        owner: str,
        repo: str,
        branch: str = "main",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List commits for a repository."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            commits = repository.get_commits(sha=branch)

            result = []
            for commit in commits[:per_page]:
                result.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                    "html_url": commit.html_url,
                })

            return {"commits": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def get_user(self, username: Optional[str] = None) -> Dict[str, Any]:
        """Get user information."""
        try:
            if username:
                user = self.client.get_user(username)
            else:
                user = self.user

            return {
                "id": user.id,
                "login": user.login,
                "name": user.name,
                "email": user.email,
                "bio": user.bio,
                "avatar_url": user.avatar_url,
                "html_url": user.html_url,
                "location": user.location,
                "company": user.company,
                "blog": user.blog,
                "twitter_username": user.twitter_username,
                "public_repos": user.public_repos,
                "public_gists": user.public_gists,
                "followers": user.followers,
                "following": user.following,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def list_branches(
        self,
        owner: str,
        repo: str,
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List branches for a repository."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            branches = repository.get_branches()

            result = []
            for branch in branches[:per_page]:
                result.append({
                    "name": branch.name,
                    "protected": branch.protected,
                    "commit": {
                        "sha": branch.commit.sha,
                        "url": branch.commit.html_url
                    }
                })

            return {"branches": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def get_branch(self, owner: str, repo: str, branch_name: str) -> Dict[str, Any]:
        """Get branch details."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            branch = repository.get_branch(branch_name)

            return {
                "name": branch.name,
                "protected": branch.protected,
                "commit": {
                    "sha": branch.commit.sha,
                    "message": branch.commit.commit.message,
                    "author": branch.commit.commit.author.name,
                    "date": branch.commit.commit.author.date.isoformat(),
                    "url": branch.commit.html_url
                }
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def list_tags(
        self,
        owner: str,
        repo: str,
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List tags for a repository."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            tags = repository.get_tags()

            result = []
            for tag in tags[:per_page]:
                result.append({
                    "name": tag.name,
                    "commit": {
                        "sha": tag.commit.sha,
                        "url": tag.commit.html_url
                    },
                    "zipball_url": tag.zipball_url,
                    "tarball_url": tag.tarball_url
                })

            return {"tags": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def list_contributors(
        self,
        owner: str,
        repo: str,
        per_page: int = 30
    ) -> Dict[str, Any]:
        """List contributors for a repository."""
        try:
            repository = self.client.get_repo(f"{owner}/{repo}")
            contributors = repository.get_contributors()

            result = []
            for contributor in contributors[:per_page]:
                result.append({
                    "login": contributor.login,
                    "id": contributor.id,
                    "avatar_url": contributor.avatar_url,
                    "html_url": contributor.html_url,
                    "contributions": contributor.contributions
                })

            return {"contributors": result, "count": len(result)}

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """Search repositories."""
        try:
            repos = self.client.search_repositories(
                query=query,
                sort=sort,
                order=order
            )

            result = []
            for repo in repos[:per_page]:
                result.append({
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "html_url": repo.html_url,
                    "language": repo.language,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "updated_at": repo.updated_at.isoformat()
                })

            return {
                "repositories": result,
                "count": len(result),
                "total_count": repos.totalCount
            }

        except GithubException as e:
            logger.error("GitHub API error: %s", e)
            raise GitHubAPIError(str(e), e.status)
