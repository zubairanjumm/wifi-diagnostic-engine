from app.diagnostics.models import NetworkEvidence


HIGH_JITTER_THRESHOLD_MS = 100.0
HIGH_LATENCY_THRESHOLD_MS = 150.0
HIGH_P95_LATENCY_THRESHOLD_MS = 250.0

BROWSER_FAILURE_RATE_THRESHOLD_PERCENT = 20.0
BROWSER_FAILURE_COUNT_THRESHOLD = 2

PACKET_LOSS_THRESHOLD_PERCENT = 5.0


def diagnose(evidence: NetworkEvidence) -> str:
    """
    Determine the most likely network problem by combining
    multiple pieces of evidence.

    The engine prioritizes:
    1. Basic connectivity failures
    2. Local network problems
    3. Internet path problems
    4. DNS problems
    5. Browser failures
    6. Persistent latency
    7. Intermittent latency / jitter
    8. No obvious problem
    """

    # ============================================================
    # 1. FUNDAMENTAL CONNECTIVITY
    # ============================================================

    # No router means the PC cannot communicate with the local network.
    if evidence.router_reachable is False:
        return "local_network_problem"

    # Router works but the internet cannot be reached.
    if (
        evidence.router_reachable is True
        and evidence.internet_reachable is False
    ):
        return "internet_connection_problem"

    # ============================================================
    # 2. LOCAL NETWORK EVIDENCE
    # ============================================================

    local_loss = evidence.router_packet_loss_percent
    local_latency = evidence.router_latency_average_ms
    local_jitter = evidence.router_jitter_ms

    local_loss_bad = (
        local_loss is not None
        and local_loss >= PACKET_LOSS_THRESHOLD_PERCENT
    )

    local_latency_bad = (
        local_latency is not None
        and local_latency > HIGH_LATENCY_THRESHOLD_MS
    )

    local_jitter_bad = (
        local_jitter is not None
        and local_jitter >= HIGH_JITTER_THRESHOLD_MS
    )

    # Multiple local indicators together are strong evidence
    # of a problem between the computer and router.
    local_problem_signals = sum(
        [
            local_loss_bad,
            local_latency_bad,
            local_jitter_bad,
        ]
    )

    if local_loss_bad:
        return "local_network_instability"

    if local_problem_signals >= 2:
        return "local_network_instability"

    # ============================================================
    # 3. INTERNET PATH EVIDENCE
    # ============================================================
    
    internet_loss = evidence.internet_packet_loss_percent
    internet_latency = evidence.internet_latency_average_ms
    internet_jitter = evidence.internet_jitter_ms

    internet_loss_bad = (
        internet_loss is not None
        and internet_loss >= PACKET_LOSS_THRESHOLD_PERCENT
    )

    internet_latency_bad = (
        internet_latency is not None
        and internet_latency > HIGH_LATENCY_THRESHOLD_MS
    )

    internet_jitter_bad = (
        internet_jitter is not None
        and internet_jitter >= HIGH_JITTER_THRESHOLD_MS
    )

    # DNS failure takes priority when internet connectivity exists.
    if (
        evidence.internet_reachable is True
        and evidence.dns_working is False
    ):
        return "dns_problem"

    if internet_loss_bad:
        return "internet_path_instability"
    
    # ============================================================
    # 5. BROWSER EVIDENCE
    # ============================================================

    failure_rate = evidence.request_failure_rate
    failure_count = evidence.failed_request_count
    request_count = evidence.request_count

    browser_average = evidence.browser_latency_average_ms
    browser_median = evidence.browser_latency_median_ms
    browser_p95 = evidence.browser_latency_p95_ms
    browser_jitter = evidence.browser_latency_jitter_ms

    browser_failures = (
        failure_rate is not None
        and failure_rate >= BROWSER_FAILURE_RATE_THRESHOLD_PERCENT
    )

    if browser_failures:
        return "browser_connection_instability"

    if (
        failure_rate is None
        and failure_count >= BROWSER_FAILURE_COUNT_THRESHOLD
    ):
        return "browser_connection_instability"

    if (
        request_count > 0
        and failure_count >= BROWSER_FAILURE_COUNT_THRESHOLD
        and failure_count / request_count >= 0.20
    ):
        return "browser_connection_instability"

    # ============================================================
    # 6. HIGH LATENCY
    # ============================================================

    # We distinguish sustained latency from occasional spikes.
    #
    # If both local and internet latency are high, the local
    # problem takes priority because the delay starts locally.
    if local_latency_bad and internet_latency_bad:
        return "high_latency"

    if internet_latency_bad:
        return "high_latency"

    if browser_average is not None:
        if browser_average > HIGH_LATENCY_THRESHOLD_MS:
            return "high_latency"

    # ============================================================
    # 7. HIGH JITTER / INTERMITTENT LATENCY
    # ============================================================

    # Internet jitter becomes much more meaningful when the
    # local router connection is stable.
    if internet_jitter_bad and not local_problem_signals:
        return "high_jitter"

    # Browser P95 can reveal occasional spikes even when the
    # average is normal.
    if (
        browser_p95 is not None
        and browser_p95 > HIGH_P95_LATENCY_THRESHOLD_MS
        and (
            browser_average is None
            or browser_average <= HIGH_LATENCY_THRESHOLD_MS
        )
    ):
        return "high_jitter"

    if (
        browser_jitter is not None
        and browser_jitter >= HIGH_JITTER_THRESHOLD_MS
        and (
            request_count == 0
            or request_count >= 5
        )
    ):
        return "high_jitter"

    if (
        browser_median is not None
        and browser_p95 is not None
        and browser_median <= HIGH_LATENCY_THRESHOLD_MS
        and browser_p95 > HIGH_P95_LATENCY_THRESHOLD_MS
    ):
        return "high_jitter"

    # ============================================================
    # 8. NORMAL
    # ============================================================

    return "no_obvious_problem"