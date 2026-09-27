from unittest.mock import patch

from app.diagnostics.models import NetworkEvidence
from app.diagnostics.rules import diagnose, build_diagnostic_finding
from app.local_diagnostic.collector import collect_local_diagnostic
from app.local_diagnostic.gui import WiFiDiagnosticGUI


def test_no_obvious_problem():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=10.0,
        router_jitter_ms=5.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=25.0,
        internet_jitter_ms=8.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_internet_completely_down_but_router_reachable():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=False,
        dns_working=False,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=5.0,
        router_jitter_ms=3.0,
        internet_packet_loss_percent=100.0,
    )

    assert diagnose(evidence) == "internet_connection_problem"


def test_router_unreachable():
    evidence = NetworkEvidence(
        router_reachable=False,
        internet_reachable=False,
        dns_working=False,
        router_packet_loss_percent=100.0,
        internet_packet_loss_percent=100.0,
    )

    assert diagnose(evidence) == "local_network_problem"


def test_router_packet_loss():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=10.0,
        router_latency_average_ms=30.0,
        router_jitter_ms=20.0,
        internet_packet_loss_percent=0.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_high_router_latency_and_jitter():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=200.0,
        router_jitter_ms=150.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=30.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_internet_packet_loss():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=10.0,
        router_jitter_ms=5.0,
        internet_packet_loss_percent=10.0,
        internet_latency_average_ms=30.0,
        internet_jitter_ms=10.0,
    )

    assert diagnose(evidence) == "internet_path_instability"


def test_dns_failure_with_internet_reachable():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=False,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
    )

    assert diagnose(evidence) == "dns_problem"


def test_dns_failure_takes_priority_over_internet_packet_loss():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=False,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=10.0,
    )

    assert diagnose(evidence) == "dns_problem"


def test_high_internet_latency():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=200.0,
        internet_jitter_ms=20.0,
    )

    assert diagnose(evidence) == "high_latency"


def test_high_internet_jitter():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=30.0,
        internet_jitter_ms=150.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_browser_failure_rate():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        request_count=10,
        successful_request_count=7,
        failed_request_count=3,
        request_failure_rate=30.0,
    )

    assert diagnose(evidence) == "browser_connection_instability"


def test_browser_failure_count_without_failure_rate():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        request_count=0,
        failed_request_count=3,
        request_failure_rate=None,
    )

    assert diagnose(evidence) == "browser_connection_instability"


def test_browser_high_p95_latency():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        request_count=10,
        failed_request_count=0,
        browser_latency_average_ms=40.0,
        browser_latency_median_ms=38.0,
        browser_latency_p95_ms=300.0,
    )

    assert diagnose(evidence) == "high_jitter"


def test_router_problem_takes_priority_over_internet_problem():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=20.0,
        internet_packet_loss_percent=20.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_router_unreachable_takes_priority_over_dns_failure():
    evidence = NetworkEvidence(
        router_reachable=False,
        internet_reachable=False,
        dns_working=False,
        router_packet_loss_percent=100.0,
    )

    assert diagnose(evidence) == "local_network_problem"


def test_zero_latency_values_do_not_crash():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=0.0,
        router_jitter_ms=0.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=0.0,
        internet_jitter_ms=0.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_missing_evidence_does_not_crash():
    evidence = NetworkEvidence()

    result = diagnose(evidence)

    assert result == "no_obvious_problem"


def test_local_collector_builds_result():
    with (
        patch(
            "app.local_diagnostic.collector.get_default_gateway",
            return_value="192.168.1.1",
        ),
        patch(
            "app.local_diagnostic.collector.measure_router_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_internet_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_dns_latency",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.test_dns",
            return_value=False,
        ),
    ):
        result = collect_local_diagnostic()

    assert result.gateway == "192.168.1.1"
    assert result.evidence.router_reachable is False
    assert result.evidence.internet_reachable is False
    assert result.evidence.dns_working is False
    assert result.diagnosis == "local_network_problem"

    assert result.recommendation is not None
    assert result.recommendation.title
    assert result.recommendation.steps

def test_weak_wifi_signal_alone_does_not_create_local_problem():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        wifi_connected=True,
        wifi_signal_percent=25.0,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=20.0,
        router_jitter_ms=5.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=30.0,
        internet_jitter_ms=5.0,
    )

    assert diagnose(evidence) == "no_obvious_problem"


def test_weak_wifi_signal_with_high_router_latency_indicates_local_instability():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        wifi_connected=True,
        wifi_signal_percent=25.0,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=180.0,
        router_jitter_ms=20.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=30.0,
        internet_jitter_ms=5.0,
    )

    assert diagnose(evidence) == "local_network_instability"


def test_wifi_evidence_is_preserved_by_collector():
    fake_wifi = type(
        "FakeWiFiEvidence",
        (),
        {
            "connected": True,
            "signal_percent": 78.0,
            "receive_rate_mbps": 866.0,
            "transmit_rate_mbps": 866.0,
            "channel": 36,
            "radio_type": "802.11ac",
        },
    )()

    with (
        patch(
            "app.local_diagnostic.collector.get_default_gateway",
            return_value="192.168.1.1",
        ),
        patch(
            "app.local_diagnostic.collector.collect_windows_wifi_evidence",
            return_value=fake_wifi,
        ),
        patch(
            "app.local_diagnostic.collector.measure_router_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_internet_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_dns_latency",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.test_dns",
            return_value=False,
        ),
    ):
        result = collect_local_diagnostic()

    assert result.evidence.wifi_connected is True
    assert result.evidence.wifi_signal_percent == 78.0
    assert result.evidence.wifi_receive_rate_mbps == 866.0
    assert result.evidence.wifi_transmit_rate_mbps == 866.0
    assert result.evidence.wifi_channel == 36
    assert result.evidence.wifi_radio_type == "802.11ac"

def test_diagnostic_finding_explains_internet_path_instability():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=8.0,
        router_jitter_ms=2.0,
        internet_packet_loss_percent=12.0,
        internet_latency_average_ms=40.0,
        internet_jitter_ms=8.0,
    )

    finding = build_diagnostic_finding(evidence)

    assert finding.code == "internet_path_instability"
    assert finding.title
    assert finding.summary
    assert finding.affected_layer == "Internet path"
    assert finding.confidence == "high"
    assert finding.evidence


def test_diagnostic_finding_explains_local_instability():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        wifi_connected=True,
        wifi_signal_percent=35.0,
        router_packet_loss_percent=8.0,
        router_latency_average_ms=80.0,
        router_jitter_ms=30.0,
        internet_packet_loss_percent=0.0,
        internet_latency_average_ms=30.0,
    )

    finding = build_diagnostic_finding(evidence)

    assert finding.code == "local_network_instability"
    assert finding.affected_layer == "Local Wi-Fi / LAN"
    assert finding.confidence == "high"
    assert any("packet loss" in item.lower() for item in finding.evidence)


def test_collector_returns_structured_finding():
    with (
        patch(
            "app.local_diagnostic.collector.get_default_gateway",
            return_value="192.168.1.1",
        ),
        patch(
            "app.local_diagnostic.collector.collect_windows_wifi_evidence",
            return_value=type(
                "FakeWiFiEvidence",
                (),
                {
                    "connected": True,
                    "signal_percent": 80.0,
                    "receive_rate_mbps": 866.0,
                    "transmit_rate_mbps": 866.0,
                    "channel": 36,
                    "radio_type": "802.11ac",
                },
            )(),
        ),
        patch(
            "app.local_diagnostic.collector.measure_router_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_internet_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_dns_latency",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.test_dns",
            return_value=False,
        ),
    ):
        result = collect_local_diagnostic()

    assert result.finding.code == result.diagnosis
    assert result.finding.title
    assert result.finding.summary
    assert result.finding.evidence