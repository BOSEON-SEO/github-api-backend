"""Simple API integration tests."""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


class TestAPI:
    """Test API endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        print("✓ Health check passed")

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = requests.get(f"{BASE_URL}/", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "version" in data["data"]
        print("✓ Root endpoint passed")

    def test_list_repos(self):
        """Test list repositories endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_list_repos (no token)")
            return

        response = requests.get(
            f"{BASE_URL}/api/repos",
            params={"per_page": 5},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "repositories" in data["data"]
        print("✓ List repos passed")

    def test_get_user(self):
        """Test get user endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_get_user (no token)")
            return

        response = requests.get(
            f"{BASE_URL}/api/user",
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "login" in data["data"]
        print("✓ Get user passed")

    def test_search_repos(self):
        """Test search repositories endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_search_repos (no token)")
            return

        response = requests.get(
            f"{BASE_URL}/api/search/repositories",
            params={"q": "flask", "per_page": 3},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "repositories" in data["data"]
        print("✓ Search repos passed")

    def test_error_handling(self):
        """Test error handling."""
        response = requests.get(f"{BASE_URL}/api/nonexistent", timeout=5)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        print("✓ Error handling passed")


def run_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running GitHub API Backend Tests")
    print("="*50 + "\n")

    test = TestAPI()
    tests = [
        test.test_health_check,
        test.test_root_endpoint,
        test.test_list_repos,
        test.test_get_user,
        test.test_search_repos,
        test.test_error_handling,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} failed: {e}")
            failed += 1

    print("\n" + "="*50)
    print(f"Tests: {passed} passed, {failed} failed")
    print("="*50 + "\n")


if __name__ == "__main__":
    run_tests()
