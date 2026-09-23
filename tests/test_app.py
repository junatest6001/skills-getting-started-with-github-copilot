from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_adds_student_to_activity():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    before = list(activities[activity_name]["participants"])

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert activities[activity_name]["participants"].count(email) == 1

    # Clean up state to avoid affecting other tests.
    activities[activity_name]["participants"] = before


def test_cannot_signup_same_student_twice():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    before = list(activities[activity_name]["participants"])
    activities[activity_name]["participants"].append(email)

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert activities[activity_name]["participants"].count(email) == 1

    activities[activity_name]["participants"] = before


def test_unregister_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "remove.student@mergington.edu"

    before = list(activities[activity_name]["participants"])
    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    activities[activity_name]["participants"] = before
