from src.app import activities


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    original_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == original_count + 1


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 400
    assert body["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    original_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == original_count - 1


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_not_registered(client):
    # Arrange
    activity_name = "Art Studio"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Student is not signed up for this activity"
