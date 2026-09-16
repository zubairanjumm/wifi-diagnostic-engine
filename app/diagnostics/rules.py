from app.diagnostics.models import NetworkEvidence


HIGH_JITTER_THRESHOLD_MS = 100.0
HIGH_LATENCY_THRESHOLD_MS = 150.0
BROWSER_FAILURE_RATE_THRESHOLD_PERCENT = 20.0


def diagnose(evidence: NetworkEvidence) -> str:
    """Determine the most likely network problem from collected evidence."""

    # -------------------------
    # Windows/local network rules
    # -------------------------

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
        and evidence.internet_latency_average_ms > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_latency"

    # -------------------------
    # Browser evidence rules
    # -------------------------

    if (
        evidence.request_failure_rate is not None
        and evidence.request_failure_rate
        >= BROWSER_FAILURE_RATE_THRESHOLD_PERCENT
    ):
        return "browser_connection_instability"

    if (
        evidence.browser_latency_jitter_ms is not None
        and evidence.browser_latency_jitter_ms
        >= HIGH_JITTER_THRESHOLD_MS
    ):
        return "high_jitter"

    if (
        evidence.browser_latency_average_ms is not None
        and evidence.browser_latency_average_ms
        > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_latency"

    return "no_obvious_problem"