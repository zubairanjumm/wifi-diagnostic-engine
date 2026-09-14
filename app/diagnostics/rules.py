from app.diagnostics.models import NetworkEvidence


def diagnose(evidence: NetworkEvidence) -> str:
    """Determine the most likely network problem from collected evidence."""

    if evidence.router_reachable is False:
        return "local_network_problem"

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

    if evidence.latency_ms is not None and evidence.latency_ms > 150:
        return "high_latency"

    return "no_obvious_problem"