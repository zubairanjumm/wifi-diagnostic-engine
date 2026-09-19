from app.diagnostics.models import NetworkEvidence
from app.diagnostics.rules import diagnose


def test_local_network_problem():
    evidence = NetworkEvidence(
        router_reachable=False,
        internet_reachable=False,
        dns_working=False,
    )

    assert diagnose(evidence) == "local_network_problem"


def test_local_network_instability():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=10.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_internet_connection_problem():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=False,
        dns_working=True,
    )

    assert diagnose(evidence) == "internet_connection_problem"


def test_dns_problem():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=False,
    )

    assert diagnose(evidence) == "dns_problem"


def test_internet_path_instability():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        internet_packet_loss_percent=10.0,
    )

    assert diagnose(evidence) == "internet_path_instability"


def test_high_latency():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        internet_latency_average_ms=200.0,
    )

    assert diagnose(evidence) == "high_latency"


def test_high_latency_with_p95():
    evidence = NetworkEvidence(
        browser_latency_average_ms=180.0,
        browser_latency_median_ms=170.0,
        browser_latency_p95_ms=300.0,
    )

    assert diagnose(evidence) == "high_latency"


def test_no_obvious_problem():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        internet_latency_average_ms=50.0,
        internet_packet_loss_percent=0.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_router_unreachable_takes_priority_over_packet_loss():
    evidence = NetworkEvidence(
        router_reachable=False,
        router_packet_loss_percent=100.0,
    )

    assert diagnose(evidence) == "local_network_problem"


def test_internet_problem_takes_priority_over_dns_failure():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=False,
        dns_working=False,
    )

    assert diagnose(evidence) == "internet_connection_problem"


def test_dns_problem_takes_priority_over_internet_packet_loss():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=False,
        internet_packet_loss_percent=10.0,
    )

    assert diagnose(evidence) == "dns_problem"


def test_packet_loss_takes_priority_over_high_latency():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        internet_packet_loss_percent=10.0,
        internet_latency_average_ms=200.0,
    )

    assert diagnose(evidence) == "internet_path_instability"


def test_router_packet_loss_below_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        router_packet_loss_percent=4.9,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_router_packet_loss_at_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        router_packet_loss_percent=5.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_latency_at_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        internet_latency_average_ms=150.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_latency_above_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        internet_latency_average_ms=150.1,
    )

    assert diagnose(evidence) == "high_latency"


def test_local_packet_loss_with_stable_internet_path():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=10.0,
        internet_packet_loss_percent=0.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_internet_packet_loss_with_stable_router():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=10.0,
    )

    assert diagnose(evidence) == "internet_path_instability"


# -------------------------
# Browser evidence
# -------------------------


def test_browser_connection_instability():
    evidence = NetworkEvidence(
        request_count=10,
        failed_request_count=3,
        request_failure_rate=30.0,
    )

    assert diagnose(evidence) == "browser_connection_instability"


def test_browser_failure_rate_below_threshold():
    evidence = NetworkEvidence(
        request_count=10,
        failed_request_count=1,
        request_failure_rate=10.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_browser_failure_count_can_detect_instability():
    evidence = NetworkEvidence(
        failed_request_count=3,
        request_failure_rate=None,
    )

    assert diagnose(evidence) == "browser_connection_instability"


def test_browser_high_average_latency():
    evidence = NetworkEvidence(
        request_count=12,
        browser_latency_average_ms=200.0,
        browser_latency_median_ms=190.0,
        browser_latency_p95_ms=300.0,
    )

    assert diagnose(evidence) == "high_latency"


def test_browser_high_jitter():
    evidence = NetworkEvidence(
        request_count=12,
        browser_latency_average_ms=80.0,
        browser_latency_median_ms=70.0,
        browser_latency_p95_ms=180.0,
        browser_latency_jitter_ms=120.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_browser_jitter_alone_with_enough_requests():
    evidence = NetworkEvidence(
        request_count=12,
        browser_latency_jitter_ms=120.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_browser_jitter_with_too_few_requests():
    evidence = NetworkEvidence(
        request_count=3,
        browser_latency_jitter_ms=120.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_browser_high_p95_with_normal_average():
    evidence = NetworkEvidence(
        request_count=12,
        browser_latency_average_ms=70.0,
        browser_latency_median_ms=65.0,
        browser_latency_p95_ms=300.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_browser_normal_latency():
    evidence = NetworkEvidence(
        request_count=12,
        successful_request_count=12,
        failed_request_count=0,
        request_success_rate=100.0,
        request_failure_rate=0.0,
        browser_latency_average_ms=50.0,
        browser_latency_median_ms=48.0,
        browser_latency_p95_ms=70.0,
        browser_latency_jitter_ms=20.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_speed_does_not_create_diagnosis():
    evidence = NetworkEvidence(
        request_count=12,
        request_success_rate=100.0,
        request_failure_rate=0.0,
        browser_latency_average_ms=30.0,
        browser_latency_median_ms=29.0,
        browser_latency_p95_ms=45.0,
        browser_latency_jitter_ms=8.0,
        download_mbps=500.0,
        upload_mbps=100.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"