from app.diagnostics.models import NetworkEvidence
from app.diagnostics.verification import verify_improvement


def test_verification_detects_latency_improvement():
    before = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_latency_average_ms=200.0,
    )

    after = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_latency_average_ms=40.0,
    )

    result = verify_improvement(before, after)

    assert result.status == "improved"


def test_verification_detects_packet_loss_improvement():
    before = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=20.0,
    )

    after = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=2.0,
    )

    result = verify_improvement(before, after)

    assert result.status == "improved"


def test_verification_detects_internet_recovery():
    before = NetworkEvidence(
        router_reachable=True,
        internet_reachable=False,
        dns_working=False,
    )

    after = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
    )

    result = verify_improvement(before, after)

    assert result.status == "improved"


def test_verification_detects_worse_connection():
    before = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_latency_average_ms=30.0,
    )

    after = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_latency_average_ms=200.0,
    )

    result = verify_improvement(before, after)

    assert result.status == "worse"


def test_verification_detects_inconclusive_result():
    before = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_latency_average_ms=50.0,
    )

    after = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_latency_average_ms=55.0,
    )

    result = verify_improvement(before, after)

    assert result.status == "inconclusive"