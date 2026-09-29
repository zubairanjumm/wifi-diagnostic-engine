from app.diagnostics.models import (
    DiagnosticFinding,
    NetworkEvidence,
)


HIGH_JITTER_THRESHOLD_MS = 100.0
HIGH_LATENCY_THRESHOLD_MS = 150.0
HIGH_P95_LATENCY_THRESHOLD_MS = 250.0

BROWSER_FAILURE_RATE_THRESHOLD_PERCENT = 20.0
BROWSER_FAILURE_COUNT_THRESHOLD = 2

PACKET_LOSS_THRESHOLD_PERCENT = 10.0
MIN_LOSS_AFFECTED_SAMPLES = 2

WEAK_WIFI_SIGNAL_THRESHOLD_PERCENT = 40.0

INSTABILITY_HIGH_LATENCY_RATE_PERCENT = 25.0
CONSISTENT_HIGH_LATENCY_RATE_PERCENT = 75.0


def _latency_rate_is(
    rate: float | None,
    threshold: float,
) -> bool:
    return (
        rate is not None
        and rate >= threshold
    )


def _repeated_packet_loss(
    packet_loss_percent: float | None,
    affected_samples: int,
    sample_count: int,
) -> bool:
    """
    Determine whether packet loss is persistent enough to
    contribute to an instability diagnosis.

    We require both:
    - meaningful packet loss
    - loss appearing in multiple diagnostic rounds
    """

    if packet_loss_percent is None:
        return False

    if packet_loss_percent < PACKET_LOSS_THRESHOLD_PERCENT:
        return False

    if affected_samples < MIN_LOSS_AFFECTED_SAMPLES:
        return False

    if sample_count < MIN_LOSS_AFFECTED_SAMPLES:
        return False

    return True


def diagnose(
    evidence: NetworkEvidence,
) -> str:
    """
    Determine the most likely network problem.

    The engine deliberately prefers repeated patterns over
    isolated measurements.

    Evidence hierarchy:

    1. Basic connectivity
    2. Repeated local packet loss
    3. Repeated local latency problems
    4. DNS
    5. Repeated internet packet loss
    6. Repeated internet latency problems
    7. Browser/application evidence
    8. High latency
    9. High jitter
    10. No obvious problem
    """

    # ---------------------------------------------------------
    # 1. Basic connectivity
    # ---------------------------------------------------------

    if evidence.router_reachable is False:
        return "local_network_problem"

    if (
        evidence.router_reachable is True
        and evidence.internet_reachable is False
    ):
        return "internet_connection_problem"

    # ---------------------------------------------------------
    # 2. Local packet loss
    # ---------------------------------------------------------

    local_loss_repeated = _repeated_packet_loss(
        evidence.router_packet_loss_percent,
        evidence.router_loss_affected_samples,
        len(evidence.router_packet_loss_samples),
    )

    if local_loss_repeated:
        return "local_network_instability"

    # ---------------------------------------------------------
    # 3. Local latency pattern
    # ---------------------------------------------------------

    local_high_latency_rate = (
        evidence.router_high_latency_rate_percent
    )

    local_has_repeated_measurements = (
        evidence.router_sample_count > 0
    )

    local_latency_repeated = _latency_rate_is(
        local_high_latency_rate,
        INSTABILITY_HIGH_LATENCY_RATE_PERCENT,
    )

    local_latency_consistent = _latency_rate_is(
        local_high_latency_rate,
        CONSISTENT_HIGH_LATENCY_RATE_PERCENT,
    )

    weak_wifi_signal = (
        evidence.wifi_signal_percent is not None
        and evidence.wifi_signal_percent
        < WEAK_WIFI_SIGNAL_THRESHOLD_PERCENT
    )

    # Strong local evidence:
    # weak Wi-Fi + high router latency.
    if (
        weak_wifi_signal
        and evidence.router_latency_average_ms is not None
        and evidence.router_latency_average_ms
        > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "local_network_instability"

    # Repeated high latency between the device and router.
    if (
        local_has_repeated_measurements
        and local_latency_repeated
    ):
        return "local_network_instability"

    # Legacy/single-result evidence:
    # very high router latency combined with high jitter.
    if (
        not local_has_repeated_measurements
        and evidence.router_latency_average_ms is not None
        and evidence.router_latency_average_ms
        > HIGH_LATENCY_THRESHOLD_MS
        and evidence.router_jitter_ms is not None
        and evidence.router_jitter_ms
        >= HIGH_JITTER_THRESHOLD_MS
    ):
        return "local_network_instability"

    # ---------------------------------------------------------
    # 4. DNS
    # ---------------------------------------------------------

    if (
        evidence.internet_reachable is True
        and evidence.dns_working is False
    ):
        return "dns_problem"

    # ---------------------------------------------------------
    # 5. Internet packet loss
    # ---------------------------------------------------------

    internet_loss_repeated = _repeated_packet_loss(
        evidence.internet_packet_loss_percent,
        evidence.internet_loss_affected_samples,
        len(evidence.internet_packet_loss_samples),
    )

    if internet_loss_repeated:
        return "internet_path_instability"

    # ---------------------------------------------------------
    # 6. Internet latency pattern
    # ---------------------------------------------------------

    internet_high_latency_rate = (
        evidence.internet_high_latency_rate_percent
    )

    internet_has_repeated_measurements = (
        evidence.internet_sample_count > 0
    )

    internet_latency_repeated = _latency_rate_is(
        internet_high_latency_rate,
        INSTABILITY_HIGH_LATENCY_RATE_PERCENT,
    )

    internet_latency_consistent = _latency_rate_is(
        internet_high_latency_rate,
        CONSISTENT_HIGH_LATENCY_RATE_PERCENT,
    )

    if (
        internet_has_repeated_measurements
        and internet_latency_repeated
        and not internet_latency_consistent
    ):
        return "internet_path_instability"

    # ---------------------------------------------------------
    # 7. Browser/application evidence
    # ---------------------------------------------------------

    failure_rate = evidence.request_failure_rate
    failure_count = evidence.failed_request_count
    request_count = evidence.request_count

    browser_average = (
        evidence.browser_latency_average_ms
    )

    browser_median = (
        evidence.browser_latency_median_ms
    )

    browser_p95 = (
        evidence.browser_latency_p95_ms
    )

    browser_jitter = (
        evidence.browser_latency_jitter_ms
    )

    browser_failures = (
        failure_rate is not None
        and failure_rate
        >= BROWSER_FAILURE_RATE_THRESHOLD_PERCENT
    )

    if browser_failures:
        return "browser_connection_instability"

    if (
        failure_rate is None
        and failure_count
        >= BROWSER_FAILURE_COUNT_THRESHOLD
    ):
        return "browser_connection_instability"

    if (
        request_count > 0
        and failure_count
        >= BROWSER_FAILURE_COUNT_THRESHOLD
        and failure_count / request_count >= 0.20
    ):
        return "browser_connection_instability"

    # ---------------------------------------------------------
    # 8. Consistently high latency
    # ---------------------------------------------------------

    if (
        local_has_repeated_measurements
        and local_latency_consistent
    ):
        return "high_latency"

    if (
        internet_has_repeated_measurements
        and internet_latency_consistent
    ):
        return "high_latency"

    # Compatibility fallback for evidence that doesn't contain
    # individual repeated measurements.

    if (
        not local_has_repeated_measurements
        and evidence.router_latency_average_ms is not None
        and evidence.router_latency_average_ms
        > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_latency"

    if (
        not internet_has_repeated_measurements
        and evidence.internet_latency_average_ms is not None
        and evidence.internet_latency_average_ms
        > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_latency"

    if (
        browser_average is not None
        and browser_average
        > HIGH_LATENCY_THRESHOLD_MS
    ):
        return "high_latency"

    # ---------------------------------------------------------
    # 9. High jitter / latency variation
    # ---------------------------------------------------------

    if (
        evidence.internet_jitter_ms is not None
        and evidence.internet_jitter_ms
        >= HIGH_JITTER_THRESHOLD_MS
        and not internet_latency_repeated
        and not local_latency_repeated
    ):
        return "high_jitter"

    if (
        browser_p95 is not None
        and browser_p95
        > HIGH_P95_LATENCY_THRESHOLD_MS
        and (
            browser_average is None
            or browser_average
            <= HIGH_LATENCY_THRESHOLD_MS
        )
    ):
        return "high_jitter"

    if (
        browser_jitter is not None
        and browser_jitter
        >= HIGH_JITTER_THRESHOLD_MS
        and (
            request_count == 0
            or request_count >= 5
        )
    ):
        return "high_jitter"

    if (
        browser_median is not None
        and browser_p95 is not None
        and browser_median
        <= HIGH_LATENCY_THRESHOLD_MS
        and browser_p95
        > HIGH_P95_LATENCY_THRESHOLD_MS
    ):
        return "high_jitter"

    # ---------------------------------------------------------
    # 10. Nothing significant found
    # ---------------------------------------------------------

    return "no_obvious_problem"


def _format_ms(
    value: float | None,
) -> str:
    if value is None:
        return "not measured"

    return f"{value:.1f} ms"


def _format_percent(
    value: float | None,
) -> str:
    if value is None:
        return "not measured"

    return f"{value:.1f}%"


def build_diagnostic_finding(
    evidence: NetworkEvidence,
) -> DiagnosticFinding:

    code = diagnose(evidence)

    if code == "local_network_problem":
        return DiagnosticFinding(
            code=code,
            title="Local network connection problem",
            summary=(
                "The device could not establish a reliable "
                "connection to the local router."
            ),
            affected_layer="Local network",
            confidence="high",
            evidence=(
                f"Router reachable: "
                f"{evidence.router_reachable}",
                f"Router packet loss: "
                f"{_format_percent(evidence.router_packet_loss_percent)}",
                f"Wi-Fi connected: "
                f"{evidence.wifi_connected}",
            ),
        )

    if code == "internet_connection_problem":
        return DiagnosticFinding(
            code=code,
            title="Internet connection problem",
            summary=(
                "The local router was reachable, but the "
                "diagnostic could not reach the internet."
            ),
            affected_layer="Internet connection",
            confidence="high",
            evidence=(
                "Router reachable: True",
                "Internet reachable: False",
                f"Router packet loss: "
                f"{_format_percent(evidence.router_packet_loss_percent)}",
            ),
        )

    if code == "local_network_instability":
        evidence_items = [
            f"Router packet loss: "
            f"{_format_percent(evidence.router_packet_loss_percent)}",
            f"Router latency: "
            f"{_format_ms(evidence.router_latency_average_ms)}",
            f"Router latency above threshold: "
            f"{evidence.router_high_latency_samples}/"
            f"{evidence.router_sample_count}",
        ]

        if evidence.router_packet_loss_samples:
            evidence_items.append(
                "Router packet-loss rounds: "
                f"{evidence.router_loss_affected_samples}/"
                f"{len(evidence.router_packet_loss_samples)}"
            )

        if evidence.wifi_signal_percent is not None:
            evidence_items.append(
                f"Wi-Fi signal: "
                f"{evidence.wifi_signal_percent:.0f}%"
            )

        return DiagnosticFinding(
            code=code,
            title="Local network instability",
            summary=(
                "Repeated measurements between the device and "
                "router show signs of instability."
            ),
            affected_layer="Local Wi-Fi / LAN",
            confidence="high",
            evidence=tuple(evidence_items),
        )

    if code == "internet_path_instability":
        evidence_items = [
            "Router reachable: True",
            f"Router packet loss: "
            f"{_format_percent(evidence.router_packet_loss_percent)}",
            f"Internet packet loss: "
            f"{_format_percent(evidence.internet_packet_loss_percent)}",
            f"Internet latency: "
            f"{_format_ms(evidence.internet_latency_average_ms)}",
            f"Internet latency above threshold: "
            f"{evidence.internet_high_latency_samples}/"
            f"{evidence.internet_sample_count}",
        ]

        if evidence.internet_packet_loss_samples:
            evidence_items.append(
                "Internet packet-loss rounds: "
                f"{evidence.internet_loss_affected_samples}/"
                f"{len(evidence.internet_packet_loss_samples)}"
            )

        return DiagnosticFinding(
            code=code,
            title="Internet path instability",
            summary=(
                "The router remained reachable while repeated "
                "measurements showed degradation on the "
                "internet path."
            ),
            affected_layer="Internet path",
            confidence="high",
            evidence=tuple(evidence_items),
        )

    if code == "dns_problem":
        return DiagnosticFinding(
            code=code,
            title="DNS resolution problem",
            summary=(
                "Internet connectivity was available, but DNS "
                "resolution failed during the diagnostic."
            ),
            affected_layer="DNS",
            confidence="high",
            evidence=(
                "Internet reachable: True",
                "DNS working: False",
                f"DNS latency: "
                f"{_format_ms(evidence.dns_latency_ms)}",
                f"Internet packet loss: "
                f"{_format_percent(evidence.internet_packet_loss_percent)}",
            ),
        )

    if code == "browser_connection_instability":
        return DiagnosticFinding(
            code=code,
            title="Connection request instability",
            summary=(
                "Repeated application-level connection requests "
                "failed at a rate above the diagnostic threshold."
            ),
            affected_layer="Application / internet path",
            confidence="medium",
            evidence=(
                f"Requests tested: "
                f"{evidence.request_count}",
                f"Failed requests: "
                f"{evidence.failed_request_count}",
                f"Request failure rate: "
                f"{_format_percent(evidence.request_failure_rate)}",
            ),
        )

    if code == "high_latency":
        evidence_items = [
            f"Router latency: "
            f"{_format_ms(evidence.router_latency_average_ms)}",
            f"Internet latency: "
            f"{_format_ms(evidence.internet_latency_average_ms)}",
        ]

        if evidence.router_sample_count:
            evidence_items.append(
                "Router high-latency measurements: "
                f"{evidence.router_high_latency_samples}/"
                f"{evidence.router_sample_count}"
            )

        if evidence.internet_sample_count:
            evidence_items.append(
                "Internet high-latency measurements: "
                f"{evidence.internet_high_latency_samples}/"
                f"{evidence.internet_sample_count}"
            )

        if evidence.browser_latency_average_ms is not None:
            evidence_items.append(
                f"Browser latency: "
                f"{_format_ms(evidence.browser_latency_average_ms)}"
            )

        return DiagnosticFinding(
            code=code,
            title="High network latency",
            summary=(
                "Most of the measurements showed network delay "
                "above the configured threshold."
            ),
            affected_layer="Network path",
            confidence="medium",
            evidence=tuple(evidence_items),
        )

    if code == "high_jitter":
        return DiagnosticFinding(
            code=code,
            title="High latency variation",
            summary=(
                "Latency varied significantly during the "
                "diagnostic, indicating an inconsistent connection."
            ),
            affected_layer="Network path",
            confidence="medium",
            evidence=(
                f"Router jitter: "
                f"{_format_ms(evidence.router_jitter_ms)}",
                f"Internet jitter: "
                f"{_format_ms(evidence.internet_jitter_ms)}",
                f"Browser P95 latency: "
                f"{_format_ms(evidence.browser_latency_p95_ms)}",
            ),
        )

    return DiagnosticFinding(
        code="no_obvious_problem",
        title="No obvious network problem detected",
        summary=(
            "The measured network evidence did not show a "
            "significant failure or repeated instability during "
            "this diagnostic."
        ),
        affected_layer="No significant issue detected",
        confidence="medium",
        evidence=(
            f"Router packet loss: "
            f"{_format_percent(evidence.router_packet_loss_percent)}",
            f"Internet packet loss: "
            f"{_format_percent(evidence.internet_packet_loss_percent)}",
            f"Router latency: "
            f"{_format_ms(evidence.router_latency_average_ms)}",
            f"Internet latency: "
            f"{_format_ms(evidence.internet_latency_average_ms)}",
        ),
    )