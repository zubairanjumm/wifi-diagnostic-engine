from app.diagnostics.models import NetworkEvidence


HIGH_JITTER_THRESHOLD_MS = 100.0


def diagnose(evidence: NetworkEvidence) -> str:
    """Determine the most likely network problem from collected evidence."""

    if evidence.router_reachable is False:
        return "local_network_problem"

    if (
        evidence.router_packet_loss_percent is not None
        and evidence.router_packet_loss_percent >= 5
    ):
        return "local_network_instability"

    if (
        evidence.router_reachable is True
        and evidence.internet_reachable is False
    ):
        return "internet_connection_problem"

    if (
        evidence.internet_reachable is True
        and evidence.dns_working is False
    ):
        return "dns_problem"

    if (
        evidence.internet_packet_loss_percent is not None
        and evidence.internet_packet_loss_percent >= 5
    ):
        return "internet_path_instability"

    if (
        evidence.internet_jitter_ms is not None
        and evidence.internet_jitter_ms >= HIGH_JITTER_THRESHOLD_MS
    ):
        return "high_jitter"

    if (
        evidence.internet_latency_average_ms is not None
        and evidence.internet_latency_average_ms > 150
    ):
        return "high_latency"

    return "no_obvious_problem"