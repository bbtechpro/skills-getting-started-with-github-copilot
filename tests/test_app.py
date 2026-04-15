import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary before each test."""
    activities.clear()
    activities["Soccer"] = {
        "description": "Play soccer",
        "schedule": "Daily",
        "max_participants": 10,
        "participants": []
    }
    activities["Basketball"] = {
        "description": "Play basketball",
        "schedule": "Daily",
        "max_participants": 10,
        "participants": []
    }
    activities["Tennis"] = {
        "description": "Play tennis",
        "schedule": "Daily",
        "max_participants": 10,
        "participants": []
    }

client = TestClient(app)

def test_get_activities():
    """Test GET /activities endpoint."""
    # Arrange: Activities are already set up by fixture

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response
    assert response.status_code == 200
    data = response.json()
    assert "Soccer" in data
    assert "Basketball" in data
    assert "Tennis" in data
    assert isinstance(data["Soccer"], dict)
    assert "participants" in data["Soccer"]

def test_signup_success():
    """Test successful signup to an activity."""
    # Arrange: No participants in Soccer

    # Act: Make POST request to signup
    response = client.post("/activities/Soccer/signup", params={"email": "alice@example.com"})

    # Assert: Check status code and that participant was added
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up alice@example.com for Soccer"
    assert "alice@example.com" in activities["Soccer"]["participants"]

def test_signup_duplicate():
    """Test signup with duplicate email."""
    # Arrange: Add alice@example.com to Soccer first
    activities["Soccer"]["participants"].append("alice@example.com")

    # Act: Try to signup alice@example.com again
    response = client.post("/activities/Soccer/signup", params={"email": "alice@example.com"})

    # Assert: Check status code and error message
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_delete_participant_success():
    """Test successful deletion of a participant."""
    # Arrange: Add alice@example.com to Soccer
    activities["Soccer"]["participants"].append("alice@example.com")

    # Act: Make DELETE request
    response = client.delete("/activities/Soccer/participants", params={"email": "alice@example.com"})

    # Assert: Check status code and that participant was removed
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Removed alice@example.com from Soccer"
    assert "alice@example.com" not in activities["Soccer"]["participants"]

def test_delete_participant_missing():
    """Test deletion of a non-existent participant."""
    # Arrange: Soccer has no participants

    # Act: Try to delete alice@example.com
    response = client.delete("/activities/Soccer/participants", params={"email": "alice@example.com"})

    # Assert: Check status code and error message
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Participant not found"