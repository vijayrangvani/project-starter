"""Smoke tests: install, imports, liveness and readiness all work. Add real tests next to them."""

import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_checks(monkeypatch):
    monkeypatch.setattr(main, "READINESS_CHECKS", {})  # each test starts with no checks


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready_with_passing_checks():
    main.READINESS_CHECKS["database"] = lambda: None
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready", "checks": ["database"]}


def test_ready_returns_503_when_a_dependency_fails():
    def broken():
        raise ConnectionError("db down")

    main.READINESS_CHECKS["database"] = broken
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.json()["failed"] == {"database": "ConnectionError"}
