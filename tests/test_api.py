import pytest
from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser+signup@example.com"

    # Ensure clean state: try to remove if present (allow 200 or 404)
    pre = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert pre.status_code in (200, 404)

    # Sign up
    r = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Unregister
    d = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert d.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
