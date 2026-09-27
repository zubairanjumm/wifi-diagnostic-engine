from dataclasses import dataclass
from typing import Callable

from app.diagnostics.models import NetworkEvidence,DiagnosticFinding
from app.diagnostics.rules import diagnose,build_diagnostic_finding
from app.diagnostics.recommendations import Recommendation, recommend
from app.local_diagnostic.windows_wifi import collect_windows_wifi_evidence
from app.network.connectivity import (
    get_default_gateway,
    measure_internet_ping,
    measure_router_ping,
)
from app.network.dns import measure_dns_latency, test_dns


SAMPLE_COUNT = 3
PING_COUNT_PER_SAMPLE = 4

ProgressCallback = Callable[[str, str], None]


@dataclass
class LocalDiagnosticResult:
    gateway: str | None
    evidence: NetworkEvidence
    diagnosis: str
    finding : DiagnosticFinding
    recommendation: Recommendation


def average(values: list[float]) -> float | None:
    if not values:
        return None

    return sum(values) / len(values)


def collect_local_diagnostic(
    progress_callback: ProgressCallback | None = None,
) -> LocalDiagnosticResult:
    """Collect repeated local network evidence and diagnose it."""

    def progress(step: str, message: str) -> None:
        if progress_callback:
            progress(step, message)

    progress("setup", "Finding your local router...")

    gateway = get_default_gateway()

    # Collect lightweight Windows Wi-Fi/interface context.
    wifi_evidence = collect_windows_wifi_evidence()

    router_samples = []
    internet_samples = []
    dns_samples = []
    dns_results = []

    for sample_number in range(1, SAMPLE_COUNT + 1):
        progress(
            "router",
            f"Testing router connection ({sample_number}/{SAMPLE_COUNT})...",
        )

        router_ping = measure_router_ping(
            gateway,
            count=PING_COUNT_PER_SAMPLE,
        )

        if router_ping is not None:
            router_samples.append(router_ping)

        progress(
            "internet",
            f"Testing internet connection ({sample_number}/{SAMPLE_COUNT})...",
        )

        internet_ping = measure_internet_ping(
            count=PING_COUNT_PER_SAMPLE,
        )

        if internet_ping is not None:
            internet_samples.append(internet_ping)

        progress(
            "dns",
            f"Testing DNS resolution ({sample_number}/{SAMPLE_COUNT})...",
        )

        dns_latency = measure_dns_latency()
        dns_working = test_dns()

        if dns_latency is not None:
            dns_samples.append(dns_latency)

        dns_results.append(dns_working)

    progress("analysis", "Combining the collected network evidence...")

    router_packet_losses = [
        sample.packet_loss_percent
        for sample in router_samples
    ]

    internet_packet_losses = [
        sample.packet_loss_percent
        for sample in internet_samples
    ]

    router_averages = [
        sample.average_ms
        for sample in router_samples
    ]

    internet_averages = [
        sample.average_ms
        for sample in internet_samples
    ]

    router_min_values = [
        sample.min_ms
        for sample in router_samples
    ]

    router_max_values = [
        sample.max_ms
        for sample in router_samples
    ]

    internet_min_values = [
        sample.min_ms
        for sample in internet_samples
    ]

    internet_max_values = [
        sample.max_ms
        for sample in internet_samples
    ]

    router_jitters = [
        sample.jitter_ms
        for sample in router_samples
    ]

    internet_jitters = [
        sample.jitter_ms
        for sample in internet_samples
    ]

    evidence = NetworkEvidence(
        router_reachable=(
            bool(router_samples)
            and average(router_packet_losses) is not None
            and average(router_packet_losses) < 100
        ),
        internet_reachable=(
            bool(internet_samples)
            and average(internet_packet_losses) is not None
            and average(internet_packet_losses) < 100
        ),
        dns_working=all(dns_results) if dns_results else False,
        dns_latency_ms=average(dns_samples),

        router_latency_min_ms=(
            min(router_min_values)
            if router_min_values
            else None
        ),
        router_latency_average_ms=average(router_averages),
        router_latency_max_ms=(
            max(router_max_values)
            if router_max_values
            else None
        ),
        router_jitter_ms=average(router_jitters),
        router_packet_loss_percent=average(router_packet_losses),

        internet_latency_min_ms=(
            min(internet_min_values)
            if internet_min_values
            else None
        ),
        internet_latency_average_ms=average(internet_averages),
        internet_latency_max_ms=(
            max(internet_max_values)
            if internet_max_values
            else None
        ),
        internet_jitter_ms=average(internet_jitters),
        internet_packet_loss_percent=average(internet_packet_losses),

        wifi_connected=wifi_evidence.connected,
        wifi_signal_percent=wifi_evidence.signal_percent,
        wifi_receive_rate_mbps=wifi_evidence.receive_rate_mbps,
        wifi_transmit_rate_mbps=wifi_evidence.transmit_rate_mbps,
        wifi_channel=wifi_evidence.channel,
        wifi_radio_type=wifi_evidence.radio_type,
    )

    diagnosis = diagnose(evidence)
    finding = build_diagnostic_finding(evidence)

    progress("analysis", "Building the recommended next step...")

    recommendation = recommend(
        diagnosis,
        evidence,
    )

    progress("complete", "Diagnosis complete.")

    return LocalDiagnosticResult(
        gateway=gateway,
        evidence=evidence,
        diagnosis=diagnosis,
        finding = finding,
        recommendation=recommendation,
    )