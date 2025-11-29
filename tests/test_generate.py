import pytest
from fastapi.testclient import TestClient
from agentforge.api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()

def test_generate_no_prompt():
    r = client.post("/generate", json={"prompt": ""})
    assert r.status_code == 400
