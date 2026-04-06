# GitHub API Backend

RESTful API backend for GitHub integration built with Flask.

## Features

- GitHub API integration (repositories, pull requests, issues, commits)
- RESTful API endpoints
- CORS support
- Authentication middleware
- Environment-based configuration

## Tech Stack

- **Framework**: Flask 3.0
- **GitHub Integration**: PyGithub 2.1
- **CORS**: Flask-CORS
- **Environment**: python-dotenv

## Project Structure

```
github-api-backend/
├── src/
│   ├── app.py                 # Application entry point
│   ├── config.py              # Configuration management
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   └── github_routes.py
│   ├── controllers/           # Business logic
│   │   ├── __init__.py
│   │   └── github_controller.py
│   └── middleware/            # Middleware functions
│       ├── __init__.py
│       └── auth_middleware.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd github-api-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GitHub token
   ```

5. **Run the application**
   ```bash
   flask run
   ```

## API Endpoints

### Repositories
- `GET /api/repos` - List user repositories
- `GET /api/repos/:owner/:repo` - Get repository details
- `POST /api/repos` - Create repository

### Pull Requests
- `GET /api/repos/:owner/:repo/pulls` - List pull requests
- `GET /api/repos/:owner/:repo/pulls/:number` - Get pull request details
- `POST /api/repos/:owner/:repo/pulls` - Create pull request

### Issues
- `GET /api/repos/:owner/:repo/issues` - List issues
- `GET /api/repos/:owner/:repo/issues/:number` - Get issue details
- `POST /api/repos/:owner/:repo/issues` - Create issue

### Commits
- `GET /api/repos/:owner/:repo/commits` - List commits

## Environment Variables

See `.env.example` for required environment variables.

## License

MIT License - see LICENSE file for details
