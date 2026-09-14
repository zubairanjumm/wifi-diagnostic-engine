from app.diagnostics.models import NetworkEvidence
from app.network.connectivity import get_default_gateway, test_router, test_internet
from app.network.dns import test_dns
from app.network.latency import measure_latency


def collect_evidence() -> NetworkEvidence:
    """Collect the network evidence needed by the diagnostic engine."""

    gateway = get_default_gateway()

    return NetworkEvidence(
        router_reachable=test_router(gateway),
        internet_reachable=test_internet(),
        dns_working=test_dns(),
        latency_ms=measure_latency(),
    )