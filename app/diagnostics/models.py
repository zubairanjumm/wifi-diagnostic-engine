from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticFinding:
    code: str
    title: str
    summary: str
    affected_layer: str
    confidence: str
    evidence: tuple[str, ...]


@dataclass
class NetworkEvidence:
    router_reachable: bool | None = None
    internet_reachable: bool | None = None
    dns_working: bool | None = None
    dns_latency_ms: float | None = None

    router_latency_min_ms: float | None = None
    router_latency_average_ms: float | None = None
    router_latency_max_ms: float | None = None
    router_jitter_ms: float | None = None

    internet_latency_min_ms: float | None = None
    internet_latency_average_ms: float | None = None
    internet_latency_max_ms: float | None = None
    internet_jitter_ms: float | None = None

    router_packet_loss_percent: float | None = None
    internet_packet_loss_percent: float | None = None

    # Packet loss from each diagnostic round.
    # Keeping these values lets the rules distinguish an isolated
    # loss event from repeated packet loss.
    router_packet_loss_samples: tuple[float, ...] = ()
    internet_packet_loss_samples: tuple[float, ...] = ()

    # Number of diagnostic rounds that experienced any packet loss.
    router_loss_affected_samples: int = 0
    internet_loss_affected_samples: int = 0

    # Individual latency measurements collected across all rounds.
    router_sample_count: int = 0
    router_high_latency_samples: int = 0
    router_high_latency_rate_percent: float | None = None

    internet_sample_count: int = 0
    internet_high_latency_samples: int = 0
    internet_high_latency_rate_percent: float | None = None

    wifi_connected: bool | None = None
    wifi_signal_percent: float | None = None
    wifi_receive_rate_mbps: float | None = None
    wifi_transmit_rate_mbps: float | None = None
    wifi_channel: int | None = None
    wifi_radio_type: str | None = None

    https_reachable: bool | None = None

    request_count: int = 0
    successful_request_count: int = 0
    failed_request_count: int = 0

    request_success_rate: float | None = None
    request_failure_rate: float | None = None

    browser_latency_min_ms: float | None = None
    browser_latency_average_ms: float | None = None
    browser_latency_median_ms: float | None = None
    browser_latency_p95_ms: float | None = None
    browser_latency_max_ms: float | None = None
    browser_latency_jitter_ms: float | None = None

    download_mbps: float | None = None
    upload_mbps: float | None = None