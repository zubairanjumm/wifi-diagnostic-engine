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
        "title": "Your connection looks stable",
        "message": (
            "We did not detect significant connection failures, "
            "latency problems, or instability."
        ),
        "next_action": (
            "If you're still having problems, run the diagnostic again "
            "while the problem is happening."
        ),
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
        "title": "Your connection appears unstable",
        "message": (
            "Some connection requests are failing repeatedly. "
            "This can cause pages, apps, or videos to load inconsistently."
        ),
        "next_action": (
            "Move closer to your router if possible, then run the "
            "diagnostic again."
        ),
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
        "title": "Your connection is fluctuating",
        "message": (
            "The delay between requests is changing significantly. "
            "This can cause problems with calls, gaming, and live video."
        ),
        "next_action": (
            "Move closer to your router and run the diagnostic again."
        ),
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


def test_diagnostic_test_endpoint():
    response = client.get("/api/diagnostic-test")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"
    assert "timestamp" in response.json()