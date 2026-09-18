from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_diagnose_normal_browser_evidence():
    response = client.post(
        "/api/diagnose",
        json={
            "https_reachable": True,
            "request_success_rate": 100,
            "request_failure_rate": 0,
            "browser_latency_min_ms": 20,
            "browser_latency_average_ms": 35,
            "browser_latency_max_ms": 50,
            "browser_latency_jitter_ms": 10,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "diagnosis": "no_obvious_problem",
    }


def test_diagnose_browser_instability():
    response = client.post(
        "/api/diagnose",
        json={
            "https_reachable": True,
            "request_success_rate": 70,
            "request_failure_rate": 30,
            "browser_latency_min_ms": 20,
            "browser_latency_average_ms": 45,
            "browser_latency_max_ms": 90,
            "browser_latency_jitter_ms": 25,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "diagnosis": "browser_connection_instability",
    }


def test_diagnose_high_jitter():
    response = client.post(
        "/api/diagnose",
        json={
            "https_reachable": True,
            "request_success_rate": 100,
            "request_failure_rate": 0,
            "browser_latency_min_ms": 20,
            "browser_latency_average_ms": 120,
            "browser_latency_max_ms": 300,
            "browser_latency_jitter_ms": 150,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "diagnosis": "high_jitter",
    }


def test_diagnose_rejects_invalid_percentage():
    response = client.post(
        "/api/diagnose",
        json={
            "request_success_rate": 120,
            "request_failure_rate": 0,
        },
    )

    assert response.status_code == 422