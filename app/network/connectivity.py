import re
import statistics
import subprocess
from dataclasses import dataclass


CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# Windows ping uses a small payload by default.
# A moderately larger payload gives the diagnostic a more useful
# network-quality measurement without turning this into an MTU test.
DIAGNOSTIC_PAYLOAD_SIZE = 128


@dataclass
class PingStats:
    packet_loss_percent: float
    min_ms: float
    average_ms: float
    max_ms: float
    jitter_ms: float
    latencies_ms: tuple[float, ...] = ()


def get_default_gateway() -> str | None:
    """Return the default IPv4 gateway on Windows."""
    result = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        creationflags=CREATE_NO_WINDOW,
    )

    for line in result.stdout.splitlines():
        if "Default Gateway" not in line:
            continue

        gateway = line.split(":", 1)[-1].strip()

        if gateway:
            return gateway

    return None


def _calculate_jitter(latencies: list[float]) -> float:
    """
    Calculate typical latency variation.

    We use the median absolute change between consecutive
    measurements instead of max - min.

    This prevents one isolated latency spike from being
    interpreted as continuous instability.
    """
    if len(latencies) < 2:
        return 0.0

    differences = [
        abs(current - previous)
        for previous, current in zip(
            latencies,
            latencies[1:],
        )
    ]

    return statistics.median(differences)


def measure_ping(
    host: str,
    count: int = 10,
    payload_size: int = DIAGNOSTIC_PAYLOAD_SIZE,
) -> PingStats | None:
    """
    Measure packet loss and latency using Windows ping.

    payload_size controls the ICMP payload in bytes.
    """

    result = subprocess.run(
        [
            "ping",
            "-n",
            str(count),
            "-l",
            str(payload_size),
            host,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        creationflags=CREATE_NO_WINDOW,
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
            latencies_ms=(),
        )

    minimum = min(latencies)
    average = sum(latencies) / len(latencies)
    maximum = max(latencies)
    jitter = _calculate_jitter(latencies)

    return PingStats(
        packet_loss_percent=packet_loss,
        min_ms=minimum,
        average_ms=average,
        max_ms=maximum,
        jitter_ms=jitter,
        latencies_ms=tuple(latencies),
    )


def test_router(gateway: str | None) -> bool:
    """Check whether the local router is reachable."""
    if not gateway:
        return False

    stats = measure_ping(gateway, count=4)

    return (
        stats is not None
        and stats.packet_loss_percent < 100
    )


def test_internet(host: str = "8.8.8.8") -> bool:
    """Check whether an external internet host is reachable."""
    stats = measure_ping(host, count=4)

    return (
        stats is not None
        and stats.packet_loss_percent < 100
    )


def measure_router_ping(
    gateway: str | None,
    count: int = 10,
) -> PingStats | None:
    """Measure latency between the computer and router."""
    if not gateway:
        return None

    return measure_ping(
        gateway,
        count=count,
        payload_size=DIAGNOSTIC_PAYLOAD_SIZE,
    )


def measure_internet_ping(
    host: str = "8.8.8.8",
    count: int = 10,
) -> PingStats | None:
    """Measure latency between the computer and internet."""
    return measure_ping(
        host,
        count=count,
        payload_size=DIAGNOSTIC_PAYLOAD_SIZE,
    )