from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball",
        "Tennis Club",
        "Drama Club",
        "Art Studio",
        "Debate Team",
        "Science Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert set(result.keys()) == expected_activities
    assert "participants" in result["Chess Club"]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Basketball"
    email = "newstudent@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_removes_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_registered_returns_400(client):
    # Arrange
    activity_name = "Basketball"
    email = "notregistered@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "is not signed up for" in response.json()["detail"]


def test_unregister_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
