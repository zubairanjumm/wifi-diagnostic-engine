import re
import subprocess
from dataclasses import dataclass


@dataclass
class PingStats:
    packet_loss_percent: float
    min_ms: float
    average_ms: float
    max_ms: float
    jitter_ms: float


def get_default_gateway() -> str | None:
    """Return the default IPv4 gateway on Windows."""

    result = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    for line in result.stdout.splitlines():
        if "Default Gateway" not in line:
            continue

        gateway = line.split(":", 1)[-1].strip()

        if gateway:
            return gateway

    return None


def measure_ping(host: str, count: int = 10) -> PingStats | None:
    """Measure packet loss and latency using Windows ping."""

    result = subprocess.run(
        ["ping", "-n", str(count), host],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    output = result.stdout

    loss_match = re.search(
        r"(\d+(?:\.\d+)?)%\s*loss",
        output,
        re.IGNORECASE,
    )

    if not loss_match:
        return None

    packet_loss = float(loss_match.group(1))

    latencies = [
        float(value)
        for value in re.findall(
            r"time[=<](\d+(?:\.\d+)?)ms",
            output,
            re.IGNORECASE,
        )
    ]

    if not latencies:
        return PingStats(
            packet_loss_percent=packet_loss,
            min_ms=0.0,
            average_ms=0.0,
            max_ms=0.0,
            jitter_ms=0.0,
        )

    minimum = min(latencies)
    average = sum(latencies) / len(latencies)
    maximum = max(latencies)

    # Keep the existing jitter definition because
    # the current tests and diagnostic engine depend on it.
    jitter = maximum - minimum

    return PingStats(
        packet_loss_percent=packet_loss,
        min_ms=minimum,
        average_ms=average,
        max_ms=maximum,
        jitter_ms=jitter,
    )


def test_router(gateway: str | None) -> bool:
    """Check whether the local router is reachable."""

    if not gateway:
        return False

    stats = measure_ping(gateway, count=4)

    return stats is not None and stats.packet_loss_percent < 100


def test_internet(host: str = "8.8.8.8") -> bool:
    """Check whether an external internet host is reachable."""

    stats = measure_ping(host, count=4)

    return stats is not None and stats.packet_loss_percent < 100


def measure_router_ping(
    gateway: str | None,
    count: int = 10,
) -> PingStats | None:
    """Measure latency between the computer and router."""

    if not gateway:
        return None

    return measure_ping(gateway, count=count)


def measure_internet_ping(
    host: str = "8.8.8.8",
    count: int = 10,
) -> PingStats | None:
    """Measure latency between the computer and internet."""

    return measure_ping(host, count=count)