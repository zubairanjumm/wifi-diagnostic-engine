from unittest.mock import patch
from app.diagnostics.engine import collect_evidence
from app.network.connectivity import PingStats


def test_collect_evidence_healthy_network():
    router_ping = PingStats(
        packet_loss_percent=0.0,
        min_ms=2.0,
        average_ms=4.0,
        max_ms=7.0,
        jitter_ms=5.0,
    )

    internet_ping = PingStats(
        packet_loss_percent=0.0,
        min_ms=20.0,
        average_ms=25.0,
        max_ms=30.0,
        jitter_ms=10.0,
    )

    with (
        patch(
            "app.diagnostics.engine.get_default_gateway",
            return_value="192.168.1.1",
        ),
        patch(
            "app.diagnostics.engine.measure_router_ping",
            return_value=router_ping,
        ),
        patch(
            "app.diagnostics.engine.measure_internet_ping",
            return_value=internet_ping,
        ),
        patch(
            "app.diagnostics.engine.test_dns",
            return_value=True,
        ),
        patch(
            "app.diagnostics.engine.measure_dns_latency",
            return_value=12.0,
        ),
    ):
        evidence = collect_evidence()

    assert evidence.router_reachable is True
    assert evidence.internet_reachable is True
    assert evidence.dns_working is True
    assert evidence.dns_latency_ms == 12.0

    assert evidence.router_packet_loss_percent == 0.0
    assert evidence.internet_packet_loss_percent == 0.0

    assert evidence.router_latency_min_ms == 2.0
    assert evidence.router_latency_average_ms == 4.0
    assert evidence.router_latency_max_ms == 7.0
    assert evidence.router_jitter_ms == 5.0

    assert evidence.internet_latency_min_ms == 20.0
    assert evidence.internet_latency_average_ms == 25.0
    assert evidence.internet_latency_max_ms == 30.0
    assert evidence.internet_jitter_ms == 10.0