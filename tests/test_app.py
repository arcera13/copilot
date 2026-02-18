from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def setup_function():
    # reset activities to initial state for each test by re-importing
    activities.clear()
    activities.update({
        "Test": {
            "description": "desc",
            "schedule": "now",
            "max_participants": 5,
            "participants": []
        }
    })


def test_signup_and_duplicate():
    response = client.post("/activities/Test/signup?email=user@x.com")
    assert response.status_code == 200
    assert "Signed up user@x.com" in response.json()["message"]

    # duplicate
    response2 = client.post("/activities/Test/signup?email=user@x.com")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_remove_participant():
    # add first
    client.post("/activities/Test/signup?email=user@x.com")
    assert "user@x.com" in activities["Test"]["participants"]

    # remove
    resp = client.delete("/activities/Test/participants?email=user@x.com")
    assert resp.status_code == 200
    assert "Removed user@x.com" in resp.json()["message"]
    assert "user@x.com" not in activities["Test"]["participants"]

    # removing again should fail
    resp2 = client.delete("/activities/Test/participants?email=user@x.com")
    assert resp2.status_code == 404
    assert "not found" in resp2.json()["detail"]
