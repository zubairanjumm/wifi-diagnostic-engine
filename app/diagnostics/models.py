from dataclasses import dataclass


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