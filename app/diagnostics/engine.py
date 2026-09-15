from app.diagnostics.models import NetworkEvidence
from app.network.connectivity import (
    get_default_gateway,
    measure_router_ping,
    measure_internet_ping,
)
from app.network.dns import (
    test_dns,
    measure_dns_latency,
)


def collect_evidence() -> NetworkEvidence:
    """Collect the network evidence needed by the diagnostic engine."""

    gateway = get_default_gateway()

    router_ping = measure_router_ping(gateway)
    internet_ping = measure_internet_ping()

    dns_latency = measure_dns_latency()

    return NetworkEvidence(
        router_reachable=(
            router_ping is not None
            and router_ping.packet_loss_percent < 100
        ),
        internet_reachable=(
            internet_ping is not None
            and internet_ping.packet_loss_percent < 100
        ),
        dns_working=test_dns(),
        dns_latency_ms=dns_latency,

        router_latency_min_ms=(
            router_ping.min_ms if router_ping else None
        ),
        router_latency_average_ms=(
            router_ping.average_ms if router_ping else None
        ),
        router_latency_max_ms=(
            router_ping.max_ms if router_ping else None
        ),
        router_jitter_ms=(
            router_ping.jitter_ms if router_ping else None
        ),

        internet_latency_min_ms=(
            internet_ping.min_ms if internet_ping else None
        ),
        internet_latency_average_ms=(
            internet_ping.average_ms if internet_ping else None
        ),
        internet_latency_max_ms=(
            internet_ping.max_ms if internet_ping else None
        ),
        internet_jitter_ms=(
            internet_ping.jitter_ms if internet_ping else None
        ),

        router_packet_loss_percent=(
            router_ping.packet_loss_percent
            if router_ping
            else None
        ),
        internet_packet_loss_percent=(
            internet_ping.packet_loss_percent
            if internet_ping
            else None
        ),
    )