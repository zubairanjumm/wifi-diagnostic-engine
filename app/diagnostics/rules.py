from app.diagnostics.models import DiagnosticFinding, NetworkEvidence


HIGH_JITTER_THRESHOLD_MS = 100.0
HIGH_LATENCY_THRESHOLD_MS = 150.0
HIGH_P95_LATENCY_THRESHOLD_MS = 250.0

BROWSER_FAILURE_RATE_THRESHOLD_PERCENT = 20.0
BROWSER_FAILURE_COUNT_THRESHOLD = 2

PACKET_LOSS_THRESHOLD_PERCENT = 5.0

WEAK_WIFI_SIGNAL_THRESHOLD_PERCENT = 40.0


def diagnose(evidence: NetworkEvidence) -> str:
    """
    Determine the most likely network problem by combining
    multiple pieces of evidence.
    """

    if evidence.router_reachable is False:
        return "local_network_problem"

    if (
        evidence.router_reachable is True
        and evidence.internet_reachable is False
    ):
        return "internet_connection_problem"

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

    local_problem_signals = sum(
        [
            local_loss_bad,
            local_latency_bad,
            local_jitter_bad,
        ]
    )

    weak_wifi_signal = (
        evidence.wifi_signal_percent is not None
        and evidence.wifi_signal_percent < WEAK_WIFI_SIGNAL_THRESHOLD_PERCENT
    )

    if local_loss_bad:
        return "local_network_instability"

    if local_problem_signals >= 2:
        return "local_network_instability"

    if weak_wifi_signal and local_latency_bad:
        return "local_network_instability"

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

    if (
        evidence.internet_reachable is True
        and evidence.dns_working is False
    ):
        return "dns_problem"

    if internet_loss_bad:
        return "internet_path_instability"

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

    if local_latency_bad and internet_latency_bad:
        return "high_latency"

    if internet_latency_bad:
        return "high_latency"

    if browser_average is not None:
        if browser_average > HIGH_LATENCY_THRESHOLD_MS:
            return "high_latency"

    if internet_jitter_bad and not local_problem_signals:
        return "high_jitter"

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

    return "no_obvious_problem"


def _format_ms(value: float | None) -> str:
    if value is None:
        return "not measured"

    return f"{value:.1f} ms"


def _format_percent(value: float | None) -> str:
    if value is None:
        return "not measured"

    return f"{value:.1f}%"


def build_diagnostic_finding(
    evidence: NetworkEvidence,
) -> DiagnosticFinding:
    """
    Convert raw network evidence into a structured diagnostic finding.

    This does not replace diagnose(). It adds the explanation layer
    required by the UI and future ISP report.
    """

    code = diagnose(evidence)

    if code == "local_network_problem":
        return DiagnosticFinding(
            code=code,
            title="Local network connection problem",
            summary=(
                "The device could not establish a reliable connection "
                "to the local router."
            ),
            affected_layer="Local network",
            confidence="high",
            evidence=(
                f"Router reachable: {evidence.router_reachable}",
                f"Router packet loss: "
                f"{_format_percent(evidence.router_packet_loss_percent)}",
                f"Wi-Fi connected: {evidence.wifi_connected}",
            ),
        )

    if code == "internet_connection_problem":
        return DiagnosticFinding(
            code=code,
            title="Internet connection problem",
            summary=(
                "The local router was reachable, but the diagnostic "
                "could not reach the internet."
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
            f"Router jitter: "
            f"{_format_ms(evidence.router_jitter_ms)}",
        ]

        if evidence.wifi_signal_percent is not None:
            evidence_items.append(
                f"Wi-Fi signal: {evidence.wifi_signal_percent:.0f}%"
            )

        return DiagnosticFinding(
            code=code,
            title="Local network instability",
            summary=(
                "The connection between the device and the local router "
                "shows signs of instability."
            ),
            affected_layer="Local Wi-Fi / LAN",
            confidence="high",
            evidence=tuple(evidence_items),
        )

    if code == "internet_path_instability":
        return DiagnosticFinding(
            code=code,
            title="Internet path instability",
            summary=(
                "The router remained reachable while packet loss was "
                "observed on the internet path."
            ),
            affected_layer="Internet path",
            confidence="high",
            evidence=(
                "Router reachable: True",
                f"Router packet loss: "
                f"{_format_percent(evidence.router_packet_loss_percent)}",
                f"Internet packet loss: "
                f"{_format_percent(evidence.internet_packet_loss_percent)}",
                f"Internet latency: "
                f"{_format_ms(evidence.internet_latency_average_ms)}",
                f"Internet jitter: "
                f"{_format_ms(evidence.internet_jitter_ms)}",
            ),
        )

    if code == "dns_problem":
        return DiagnosticFinding(
            code=code,
            title="DNS resolution problem",
            summary=(
                "Internet connectivity was available, but DNS resolution "
                "failed during the diagnostic."
            ),
            affected_layer="DNS",
            confidence="high",
            evidence=(
                "Internet reachable: True",
                "DNS working: False",
                f"DNS latency: {_format_ms(evidence.dns_latency_ms)}",
                f"Internet packet loss: "
                f"{_format_percent(evidence.internet_packet_loss_percent)}",
            ),
        )

    if code == "browser_connection_instability":
        return DiagnosticFinding(
            code=code,
            title="Connection request instability",
            summary=(
                "Repeated application-level connection requests failed "
                "at a rate above the diagnostic threshold."
            ),
            affected_layer="Application / internet path",
            confidence="medium",
            evidence=(
                f"Requests tested: {evidence.request_count}",
                f"Failed requests: {evidence.failed_request_count}",
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

        if evidence.browser_latency_average_ms is not None:
            evidence_items.append(
                f"Browser latency: "
                f"{_format_ms(evidence.browser_latency_average_ms)}"
            )

        return DiagnosticFinding(
            code=code,
            title="High network latency",
            summary=(
                "The diagnostic measured sustained network delay above "
                "the configured threshold."
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
                "Latency varied significantly during the diagnostic, "
                "indicating an inconsistent connection."
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
            "The measured network evidence did not show a significant "
            "failure or instability during this diagnostic."
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