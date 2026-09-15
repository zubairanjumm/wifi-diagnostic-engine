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
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=10.0,
    )

    assert diagnose(evidence) == "internet_path_instability"

def test_jitter_alone_does_not_create_diagnosis():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=26.5,
        internet_jitter_ms=23.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"

def test_jitter_below_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
        internet_jitter_ms=99.9,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_jitter_at_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
        internet_jitter_ms=100.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_jitter_above_threshold():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
        internet_jitter_ms=120.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_packet_loss_takes_priority_over_jitter():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=10.0,
        internet_jitter_ms=150.0,
    )

    assert diagnose(evidence) == "internet_path_instability"