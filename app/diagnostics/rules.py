from app.diagnostics.models import NetworkEvidence


HIGH_JITTER_THRESHOLD_MS = 100.0
HIGH_LATENCY_THRESHOLD_MS = 150.0
HIGH_P95_LATENCY_THRESHOLD_MS = 250.0

BROWSER_FAILURE_RATE_THRESHOLD_PERCENT = 20.0
BROWSER_FAILURE_COUNT_THRESHOLD = 2


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
    # Browser evidence
    # -------------------------

    failure_rate = evidence.request_failure_rate
    failure_count = evidence.failed_request_count
    request_count = evidence.request_count

    average_latency = evidence.browser_latency_average_ms
    median_latency = evidence.browser_latency_median_ms
    p95_latency = evidence.browser_latency_p95_ms
    jitter = evidence.browser_latency_jitter_ms

    # --------------------------------
    # 1. Browser request failures
    # --------------------------------

    if (
        failure_rate is not None
        and failure_rate >= BROWSER_FAILURE_RATE_THRESHOLD_PERCENT
    ):
        return "browser_connection_instability"

    # If percentage isn't available, a meaningful number
    # of failed requests can still indicate instability.
    if (
        failure_rate is None
        and failure_count >= BROWSER_FAILURE_COUNT_THRESHOLD
    ):
        return "browser_connection_instability"

    # If we know how many requests were tested, avoid
    # interpreting a single failure as serious instability.
    if (
        request_count > 0
        and failure_count >= BROWSER_FAILURE_COUNT_THRESHOLD
        and failure_count / request_count >= 0.20
    ):
        return "browser_connection_instability"

    # --------------------------------
    # 2. Sustained high latency
    # --------------------------------

    # Average latency tells us whether delay is consistently
    # elevated across successful requests.
    if (
        average_latency is not None
        and average_latency > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_latency"

    # --------------------------------
    # 3. Intermittent high latency
    # --------------------------------

    # A normal median/average with a very high P95 means
    # most requests are okay but some are taking much longer.
    if (
        p95_latency is not None
        and p95_latency > HIGH_P95_LATENCY_THRESHOLD_MS
        and average_latency is not None
        and average_latency <= HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_jitter"

    # --------------------------------
    # 4. High jitter
    # --------------------------------

    # Jitter is stronger evidence when we have enough
    # requests to calculate it reliably.
    if (
        jitter is not None
        and jitter >= HIGH_JITTER_THRESHOLD_MS
        and (
            request_count == 0
            or request_count >= 5
        )
    ):
        return "high_jitter"

    # --------------------------------
    # 5. Median/P95 consistency check
    # --------------------------------

    # If the median is normal but P95 is significantly
    # elevated, treat it as intermittent instability.
    if (
        median_latency is not None
        and p95_latency is not None
        and median_latency <= HIGH_LATENCY_THRESHOLD_MS
        and p95_latency > HIGH_P95_LATENCY_THRESHOLD_MS
    ):
        return "high_jitter"

    return "no_obvious_problem"