# API Request Examples

Complete examples for testing all API endpoints.

## Authentication

### 1. OAuth Flow

#### Step 1: Get OAuth URL
```bash
curl http://localhost:5000/api/auth/login
```

**Response:**
```json
{
  "success": true,
  "data": {
    "auth_url": "https://github.com/login/oauth/authorize?client_id=...",
    "state": "random_state_token"
  },
  "message": "OAuth URL generated"
}
```

#### Step 2: User Authorizes on GitHub
→ GitHub redirects to: `http://localhost:5000/api/auth/callback?code=...&state=...`

#### Step 3: Exchange Code for Token
This happens automatically when GitHub redirects to the callback URL.

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "github_token": "gho_...",
    "user": {
      "id": 12345,
      "login": "username",
      "name": "User Name",
      ...
    }
  },
  "message": "Authentication successful"
}
```

### 2. Validate Personal Access Token

```bash
curl -X POST http://localhost:5000/api/auth/validate \
  -H "Content-Type: application/json" \
  -d '{"token": "ghp_your_token_here"}'
```

## Users

### Get Authenticated User

```bash
curl http://localhost:5000/api/user \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get User by Username

```bash
curl http://localhost:5000/api/users/octocat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 583231,
    "login": "octocat",
    "name": "The Octocat",
    "email": "octocat@github.com",
    "bio": "GitHub mascot",
    "avatar_url": "https://avatars.githubusercontent.com/u/583231",
    "html_url": "https://github.com/octocat",
    "location": "San Francisco",
    "company": "@github",
    "public_repos": 8,
    "followers": 5000,
    "following": 9,
    "created_at": "2011-01-25T18:44:36",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

## Repositories

### List User Repositories

```bash
# List authenticated user's repos
curl http://localhost:5000/api/repos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# List specific user's repos
curl "http://localhost:5000/api/repos?username=octocat&sort=updated&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Repository Details

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1296269,
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "description": "My first repository",
    "private": false,
    "html_url": "https://github.com/octocat/Hello-World",
    "clone_url": "https://github.com/octocat/Hello-World.git",
    "language": "JavaScript",
    "stars": 1500,
    "watchers": 1500,
    "forks": 500,
    "open_issues": 20,
    "default_branch": "main"
  }
}
```

### Create Repository

```bash
curl -X POST http://localhost:5000/api/repos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-new-repo",
    "description": "A test repository",
    "private": false,
    "auto_init": true
  }'
```

## Branches

### List Branches

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World/branches \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "branches": [
      {
        "name": "main",
        "protected": true,
        "commit": {
          "sha": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
          "url": "https://github.com/octocat/Hello-World/commit/7fd1a60"
        }
      },
      {
        "name": "develop",
        "protected": false,
        "commit": {
          "sha": "abc123...",
          "url": "..."
        }
      }
    ],
    "count": 2
  }
}
```

### Get Branch Details

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World/branches/main \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Tags

### List Tags

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World/tags \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tags": [
      {
        "name": "v1.0.0",
        "commit": {
          "sha": "abc123...",
          "url": "..."
        },
        "zipball_url": "https://github.com/.../zipball/v1.0.0",
        "tarball_url": "https://github.com/.../tarball/v1.0.0"
      }
    ],
    "count": 1
  }
}
```

## Contributors

### List Contributors

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World/contributors \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Pull Requests

### List Pull Requests

```bash
# List open PRs
curl http://localhost:5000/api/repos/octocat/Hello-World/pulls \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# List all PRs
curl "http://localhost:5000/api/repos/octocat/Hello-World/pulls?state=all&per_page=20" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Pull Request Details

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World/pulls/42 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "number": 42,
    "title": "Add new feature",
    "body": "This PR adds...",
    "state": "open",
    "user": "contributor",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-02T15:30:00",
    "merged": false,
    "mergeable": true,
    "html_url": "https://github.com/octocat/Hello-World/pull/42",
    "head": "feature-branch",
    "base": "main",
    "commits": 5,
    "additions": 100,
    "deletions": 20,
    "changed_files": 3
  }
}
```

### Create Pull Request

```bash
curl -X POST http://localhost:5000/api/repos/octocat/Hello-World/pulls \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Add new feature",
    "body": "This PR implements feature X",
    "head": "feature-branch",
    "base": "main"
  }'
```

## Issues

### List Issues

```bash
# List open issues
curl http://localhost:5000/api/repos/octocat/Hello-World/issues \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# List closed issues
curl "http://localhost:5000/api/repos/octocat/Hello-World/issues?state=closed" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Issue Details

```bash
curl http://localhost:5000/api/repos/octocat/Hello-World/issues/10 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "number": 10,
    "title": "Bug in feature X",
    "body": "When I do X, Y happens...",
    "state": "open",
    "user": "reporter",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-02T11:00:00",
    "html_url": "https://github.com/octocat/Hello-World/issues/10",
    "comments": 5,
    "labels": ["bug", "high-priority"]
  }
}
```

### Create Issue

```bash
curl -X POST http://localhost:5000/api/repos/octocat/Hello-World/issues \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Found a bug",
    "body": "Detailed description of the bug...",
    "labels": ["bug"]
  }'
```

## Commits

### List Commits

```bash
# List commits from main branch
curl http://localhost:5000/api/repos/octocat/Hello-World/commits \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# List commits from specific branch
curl "http://localhost:5000/api/repos/octocat/Hello-World/commits?branch=develop&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "commits": [
      {
        "sha": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
        "message": "Fix bug in authentication",
        "author": "John Doe",
        "date": "2024-01-15T10:30:00",
        "html_url": "https://github.com/.../commit/7fd1a60"
      }
    ],
    "count": 1
  }
}
```

## Search

### Search Repositories

```bash
# Basic search
curl "http://localhost:5000/api/search/repositories?q=flask" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Advanced search with filters
curl "http://localhost:5000/api/search/repositories?q=flask+language:python&sort=stars&order=desc&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "repositories": [
      {
        "id": 596892,
        "name": "flask",
        "full_name": "pallets/flask",
        "description": "The Python micro framework for building web applications",
        "html_url": "https://github.com/pallets/flask",
        "language": "Python",
        "stars": 65000,
        "forks": 16000,
        "updated_at": "2024-01-15T10:00:00"
      }
    ],
    "count": 1,
    "total_count": 50000
  }
}
```

## Health Check

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "github-api-backend"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Missing required fields: title, head",
  "status_code": 400,
  "errors": {
    "missing_fields": ["title", "head"]
  }
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Invalid or expired token",
  "status_code": 401
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Repository not found",
  "status_code": 404
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "An unexpected error occurred",
  "status_code": 500
}
```

## Testing with Postman

1. Import the endpoints into Postman
2. Set up environment variables:
   - `base_url`: `http://localhost:5000`
   - `jwt_token`: Your JWT token from OAuth flow
3. Use `{{base_url}}/api/repos` format for requests
4. Add `Authorization: Bearer {{jwt_token}}` to headers

## Testing with HTTPie

HTTPie provides a more readable command-line HTTP client:

```bash
# Install HTTPie
pip install httpie

# Example requests
http GET localhost:5000/api/user Authorization:"Bearer YOUR_TOKEN"
http GET localhost:5000/api/repos username==octocat per_page==10
http POST localhost:5000/api/repos/owner/repo/issues title="Bug" body="Description"
```
