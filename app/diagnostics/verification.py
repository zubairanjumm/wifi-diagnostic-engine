from dataclasses import dataclass

from app.diagnostics.models import NetworkEvidence


@dataclass(frozen=True)
class VerificationResult:
    status: str
    title: str
    message: str


def _percentage_change(
    before: float | None,
    after: float | None,
) -> float | None:
    if before is None or after is None:
        return None

    if before == 0:
        return None

    return ((after - before) / before) * 100


def verify_improvement(
    before: NetworkEvidence,
    after: NetworkEvidence,
) -> VerificationResult:
    """
    Compare two diagnostic runs and determine whether
    the connection improved after a troubleshooting action.
    """

    improvements = 0
    regressions = 0

    metrics: list[tuple[float | None, float | None, str]] = [
        (
            before.router_packet_loss_percent,
            after.router_packet_loss_percent,
            "router packet loss",
        ),
        (
            before.internet_packet_loss_percent,
            after.internet_packet_loss_percent,
            "internet packet loss",
        ),
        (
            before.router_latency_average_ms,
            after.router_latency_average_ms,
            "router latency",
        ),
        (
            before.internet_latency_average_ms,
            after.internet_latency_average_ms,
            "internet latency",
        ),
        (
            before.router_jitter_ms,
            after.router_jitter_ms,
            "router jitter",
        ),
        (
            before.internet_jitter_ms,
            after.internet_jitter_ms,
            "internet jitter",
        ),
    ]

    for before_value, after_value, _ in metrics:
        if before_value is None or after_value is None:
            continue

        change = _percentage_change(
            before_value,
            after_value,
        )

        if change is None:
            continue

        if change <= -20:
            improvements += 1
        elif change >= 20:
            regressions += 1

    if (
        before.internet_reachable is False
        and after.internet_reachable is True
    ):
        improvements += 2

    if (
        before.router_reachable is False
        and after.router_reachable is True
    ):
        improvements += 2

    if (
        before.dns_working is False
        and after.dns_working is True
    ):
        improvements += 2

    if (
        before.internet_reachable is True
        and after.internet_reachable is False
    ):
        regressions += 2

    if (
        before.router_reachable is True
        and after.router_reachable is False
    ):
        regressions += 2

    if (
        before.dns_working is True
        and after.dns_working is False
    ):
        regressions += 2

    if improvements > regressions:
        return VerificationResult(
            status="improved",
            title="Your connection improved",
            message=(
                "The second diagnostic shows a meaningful improvement "
                "compared with the first diagnostic."
            ),
        )

    if regressions > improvements:
        return VerificationResult(
            status="worse",
            title="Your connection got worse",
            message=(
                "The second diagnostic shows worse network conditions "
                "compared with the first diagnostic."
            ),
        )

    return VerificationResult(
        status="inconclusive",
        title="The result is inconclusive",
        message=(
            "The second diagnostic did not show a clear enough change "
            "to confirm whether the connection improved."
        ),
    )