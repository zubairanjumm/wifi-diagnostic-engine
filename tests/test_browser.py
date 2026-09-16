import pytest

from app.network.browser import validate_browser_evidence


def test_valid_browser_evidence():
    data = {
        "https_reachable": True,
        "request_success_rate": 95,
        "request_failure_rate": 5,
        "browser_latency_min_ms": 20,
        "browser_latency_average_ms": 35,
        "browser_latency_max_ms": 60,
        "browser_latency_jitter_ms": 40,
        "download_mbps": 50,
        "upload_mbps": 10,
    }

    result = validate_browser_evidence(data)

    assert result["https_reachable"] is True
    assert result["request_success_rate"] == 95.0
    assert result["download_mbps"] == 50.0


def test_empty_browser_evidence():
    result = validate_browser_evidence({})

    assert result["https_reachable"] is None
    assert result["download_mbps"] is None


def test_invalid_percentage():
    with pytest.raises(ValueError):
        validate_browser_evidence({
            "request_success_rate": 150,
        })


def test_negative_latency():
    with pytest.raises(ValueError):
        validate_browser_evidence({
            "browser_latency_average_ms": -10,
        })


def test_negative_speed():
    with pytest.raises(ValueError):
        validate_browser_evidence({
            "download_mbps": -5,
        })


def test_invalid_boolean():
    with pytest.raises(ValueError):
        validate_browser_evidence({
            "https_reachable": "yes",
        })


def test_invalid_input_type():
    with pytest.raises(TypeError):
        validate_browser_evidence([])