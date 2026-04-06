# GitHub API Backend

RESTful API backend for GitHub integration built with Flask and PyGithub.

## Features

- **GitHub API Integration**: Full support for repositories, pull requests, issues, commits, branches, tags, users, and search
- **Dual Authentication**: Support for both Personal Access Token (PAT) and OAuth 2.0
- **JWT Token Management**: Secure token-based authentication
- **RESTful API**: Clean, consistent API design with proper error handling
- **CORS Support**: Cross-origin resource sharing enabled
- **Environment-based Configuration**: Separate dev/production configs
- **Comprehensive Error Handling**: Custom exceptions and global error handlers
- **Response Formatting**: Consistent success/error response structure

## Tech Stack

- **Framework**: Flask 3.0
- **GitHub Integration**: PyGithub 2.1.1
- **Authentication**: PyJWT 2.8.0
- **CORS**: Flask-CORS 4.0.0
- **Environment**: python-dotenv 1.0.0
- **Production Server**: Gunicorn 21.2.0

## Project Structure

```
github-api-backend/
├── src/
│   ├── app.py                      # Application entry point
│   ├── config.py                   # Configuration management
│   ├── routes/                     # API routes
│   │   ├── __init__.py
│   │   ├── github_routes.py        # GitHub API endpoints
│   │   └── auth_routes.py          # OAuth endpoints
│   ├── controllers/                # Business logic
│   │   ├── __init__.py
│   │   ├── github_controller.py    # GitHub API logic
│   │   └── auth_controller.py      # OAuth logic
│   ├── middleware/                 # Middleware functions
│   │   ├── __init__.py
│   │   └── auth_middleware.py      # Authentication middleware
│   └── utils/                      # Utility modules
│       ├── __init__.py
│       ├── exceptions.py           # Custom exceptions
│       ├── response.py             # Response formatters
│       ├── validators.py           # Request validators
│       └── jwt_helper.py           # JWT utilities
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd github-api-backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and configure:
# - GITHUB_TOKEN (required for PAT auth)
# - GITHUB_CLIENT_ID & GITHUB_CLIENT_SECRET (optional, for OAuth)
# - JWT_SECRET_KEY (change in production!)
```

### 5. Run the application

**Development:**
```bash
flask run
# or
python -m src.app
```

**Production:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "src.app:create_app()"
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/login` | Get GitHub OAuth URL |
| GET | `/api/auth/callback` | OAuth callback handler |
| POST | `/api/auth/validate` | Validate PAT token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user` | Get authenticated user |
| GET | `/api/users/:username` | Get user by username |

### Repositories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos` | List user repositories |
| GET | `/api/repos/:owner/:repo` | Get repository details |
| POST | `/api/repos` | Create repository |
| GET | `/api/repos/:owner/:repo/branches` | List branches |
| GET | `/api/repos/:owner/:repo/branches/:name` | Get branch details |
| GET | `/api/repos/:owner/:repo/tags` | List tags |
| GET | `/api/repos/:owner/:repo/contributors` | List contributors |

### Pull Requests

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:owner/:repo/pulls` | List pull requests |
| GET | `/api/repos/:owner/:repo/pulls/:number` | Get PR details |
| POST | `/api/repos/:owner/:repo/pulls` | Create pull request |

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:owner/:repo/issues` | List issues |
| GET | `/api/repos/:owner/:repo/issues/:number` | Get issue details |
| POST | `/api/repos/:owner/:repo/issues` | Create issue |

### Commits

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:owner/:repo/commits` | List commits |

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/repositories` | Search repositories |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | API info |

## Authentication Methods

### 1. Personal Access Token (PAT)

Set `GITHUB_TOKEN` in `.env`:

```bash
GITHUB_TOKEN=ghp_your_token_here
```

All endpoints automatically use this token when `@require_github_token` middleware is applied.

### 2. OAuth 2.0 Flow

1. Configure OAuth app in GitHub Settings → Developer settings → OAuth Apps
2. Set in `.env`:
   ```bash
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   GITHUB_REDIRECT_URI=http://localhost:5000/api/auth/callback
   ```

3. OAuth flow:
   ```
   GET /api/auth/login
   → Redirects to GitHub
   → User authorizes
   → GitHub redirects to /api/auth/callback?code=...
   → Receives JWT token
   ```

4. Use JWT in subsequent requests:
   ```
   Authorization: Bearer <jwt_token>
   ```

## Request Examples

### Get User Info
```bash
curl http://localhost:5000/api/user \
  -H "Content-Type: application/json"
```

### List Repositories
```bash
curl "http://localhost:5000/api/repos?username=octocat&per_page=10" \
  -H "Content-Type: application/json"
```

### Create Issue
```bash
curl -X POST http://localhost:5000/api/repos/owner/repo/issues \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bug report",
    "body": "Something is broken",
    "labels": ["bug"]
  }'
```

### Search Repositories
```bash
curl "http://localhost:5000/api/search/repositories?q=flask&sort=stars&per_page=5" \
  -H "Content-Type: application/json"
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "status_code": 400,
  "errors": { ... }  // Optional additional details
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FLASK_APP` | No | `src.app` | Flask app module |
| `FLASK_ENV` | No | `development` | Environment (development/production) |
| `FLASK_DEBUG` | No | `False` | Debug mode |
| `GITHUB_TOKEN` | Yes* | - | GitHub Personal Access Token |
| `GITHUB_CLIENT_ID` | No | - | OAuth client ID |
| `GITHUB_CLIENT_SECRET` | No | - | OAuth client secret |
| `GITHUB_REDIRECT_URI` | No | `http://localhost:5000/api/auth/callback` | OAuth redirect URI |
| `JWT_SECRET_KEY` | No | `your-secret-key-change-in-production` | JWT signing key |
| `JWT_EXPIRATION_HOURS` | No | `24` | JWT expiration time |
| `HOST` | No | `0.0.0.0` | Server host |
| `PORT` | No | `5000` | Server port |
| `CORS_ORIGINS` | No | `http://localhost:3000` | Allowed CORS origins (comma-separated) |

\* Required unless using OAuth flow

## Error Handling

The API uses custom exception classes for different error types:

- `BadRequestError` (400): Invalid request
- `UnauthorizedError` (401): Authentication failed
- `ForbiddenError` (403): Insufficient permissions
- `NotFoundError` (404): Resource not found
- `GitHubAPIError` (varies): GitHub API errors

All errors return consistent JSON responses with appropriate HTTP status codes.

## Development

### Running Tests
```bash
# Add tests in future
pytest
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document all functions with docstrings
- Use structured logging

## Production Deployment

1. Set `FLASK_ENV=production` in `.env`
2. Change `JWT_SECRET_KEY` to a secure random value
3. Use HTTPS for OAuth redirect URI
4. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "src.app:create_app()"
   ```
5. Consider using a reverse proxy (Nginx) and process manager (systemd/supervisor)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on GitHub.
