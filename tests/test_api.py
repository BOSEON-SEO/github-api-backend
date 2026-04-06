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


    def test_list_milestones(self):
        """Test list milestones endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_list_milestones (no token)")
            return

        response = requests.get(
            f"{BASE_URL}/api/repos/BOSEAN-SEO/github-api-backend/milestones",
            params={"state": "all", "per_page": 5},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "milestones" in data["data"]
        assert "count" in data["data"]
        print("✓ List milestones passed")

    def test_create_milestone(self):
        """Test create milestone endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_create_milestone (no token)")
            return

        response = requests.post(
            f"{BASE_URL}/api/repos/BOSEAN-SEO/github-api-backend/milestones",
            json={
                "title": "v1.1.0 — Test Milestone",
                "description": "Auto-generated milestone for integration test",
                "state": "open",
                "due_on": "2026-12-31T00:00:00Z",
            },
            timeout=10
        )
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        ms = data["data"]
        assert ms["title"] == "v1.1.0 — Test Milestone"
        assert ms["state"] == "open"
        assert ms["number"] is not None
        self._created_milestone_number = ms["number"]
        print(f"✓ Create milestone passed (number={ms['number']})")

    def test_get_milestone(self):
        """Test get single milestone endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_get_milestone (no token)")
            return
        if not hasattr(self, "_created_milestone_number"):
            print("⊘ Skipping test_get_milestone (no milestone created)")
            return

        number = self._created_milestone_number
        response = requests.get(
            f"{BASE_URL}/api/repos/BOSEAN-SEO/github-api-backend/milestones/{number}",
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["number"] == number
        print(f"✓ Get milestone passed (number={number})")

    def test_update_milestone(self):
        """Test update milestone endpoint (PATCH)."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_update_milestone (no token)")
            return
        if not hasattr(self, "_created_milestone_number"):
            print("⊘ Skipping test_update_milestone (no milestone created)")
            return

        number = self._created_milestone_number
        response = requests.patch(
            f"{BASE_URL}/api/repos/BOSEAN-SEO/github-api-backend/milestones/{number}",
            json={"description": "Updated description for integration test"},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["description"] == "Updated description for integration test"
        print(f"✓ Update milestone passed (number={number})")

    def test_delete_milestone(self):
        """Test delete milestone endpoint."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_delete_milestone (no token)")
            return
        if not hasattr(self, "_created_milestone_number"):
            print("⊘ Skipping test_delete_milestone (no milestone created)")
            return

        number = self._created_milestone_number
        response = requests.delete(
            f"{BASE_URL}/api/repos/BOSEAN-SEO/github-api-backend/milestones/{number}",
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["deleted"] is True
        assert data["data"]["milestone_number"] == number
        print(f"✓ Delete milestone passed (number={number})")

    def test_create_milestone_missing_title(self):
        """Test create milestone returns 400 when title is missing."""
        if not GITHUB_TOKEN:
            print("⊘ Skipping test_create_milestone_missing_title (no token)")
            return

        response = requests.post(
            f"{BASE_URL}/api/repos/BOSEAN-SEO/github-api-backend/milestones",
            json={"description": "No title provided"},
            timeout=10
        )
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        print("✓ Create milestone (missing title) validation passed")


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
        test.test_list_milestones,
        test.test_create_milestone,
        test.test_get_milestone,
        test.test_update_milestone,
        test.test_delete_milestone,
        test.test_create_milestone_missing_title,
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
