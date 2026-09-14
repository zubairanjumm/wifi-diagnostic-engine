from dataclasses import dataclass


@dataclass
class NetworkEvidence:
    router_reachable: bool | None = None
    internet_reachable: bool | None = None
    dns_working: bool | None = None
    latency_ms: float | None = None