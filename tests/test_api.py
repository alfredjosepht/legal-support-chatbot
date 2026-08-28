#!/usr/bin/env python3
"""Basic API endpoint tests using FastAPI TestClient."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Backend running"
    print("[PASS] test_root")


def test_locations():
    response = client.get("/locations")
    assert response.status_code == 200
    data = response.json()
    assert "locations" in data
    assert isinstance(data["locations"], list)
    assert "national" in data["locations"]
    print("[PASS] test_locations")


def test_chat_empty():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "unknown"
    assert data["confidence"] == 0.0
    print("[PASS] test_chat_empty")


def test_chat_valid():
    response = client.post("/chat", json={"message": "Someone beat me up"})
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "confidence" in data
    assert "matched_categories" in data
    assert "laws" in data
    assert "steps" in data
    assert "resources" in data
    print("[PASS] test_chat_valid")


def test_chat_categories():
    # Sexual assault test - must not include cyber_bullying
    res = client.post("/chat", json={"message": "he raped me"}).json()
    assert res["category"] == "sexual_assault"
    matched = [m["category"] for m in res["matched_categories"]]
    assert "sexual_assault" in matched
    assert "cyber_bullying" not in matched

    # Bullying test
    res = client.post("/chat", json={"message": "he bullied me"}).json()
    assert res["category"] == "ragging"

    # Assault test
    res = client.post("/chat", json={"message": "someone punched me"}).json()
    assert res["category"] == "physical_assault"

    print("[PASS] test_chat_categories")


def test_signup_and_login():
    import time
    unique_user = f"test_user_{int(time.time())}"
    
    # Signup
    response = client.post("/signup", json={"username": unique_user, "password": "testpass123"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
    # Login
    response = client.post("/login", json={"username": unique_user, "password": "testpass123"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
    # Login with wrong password
    response = client.post("/login", json={"username": unique_user, "password": "wrong"})
    assert response.status_code == 401
    
    print("[PASS] test_signup_and_login")


def test_consultations():
    response = client.get("/consultations/nonexistent_user_xyz")
    assert response.status_code == 200
    data = response.json()
    assert "consultations" in data
    assert data["consultations"] == []
    print("[PASS] test_consultations")


if __name__ == "__main__":
    test_root()
    test_locations()
    test_chat_empty()
    test_chat_valid()
    test_chat_categories()
    test_signup_and_login()
    test_consultations()
    print("\n[ALL PASS] All API tests passed!")
