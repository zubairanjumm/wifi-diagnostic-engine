import re
import subprocess
from dataclasses import dataclass


@dataclass
class PingStats:
    """Statistics collected from a single ping session."""

    packet_loss_percent: float
    min_ms: float | None
    average_ms: float | None
    max_ms: float | None
    jitter_ms: float | None


def get_default_gateway() -> str | None:
    """Return the default gateway IP address."""
    try:
        result = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        for line in result.stdout.splitlines():
            if "Default Gateway" in line:
                gateway = line.split(":")[-1].strip()

                if gateway:
                    return gateway

    except Exception:
        return None

    return None


def measure_ping(host: str, count: int = 10) -> PingStats | None:
    """Run one ping session and collect packet loss and latency statistics."""
    try:
        result = subprocess.run(
            ["ping", "-n", str(count), host],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        loss_match = re.search(
            r"\((\d+)%\s*loss\)",
            result.stdout,
        )

        if not loss_match:
            return None

        packet_loss = float(loss_match.group(1))

        latencies = []

        for line in result.stdout.splitlines():
            match = re.search(
                r"time[=<](\d+(?:\.\d+)?)ms",
                line,
            )

            if match:
                latencies.append(float(match.group(1)))

        if latencies:
            minimum = min(latencies)
            maximum = max(latencies)
            average = sum(latencies) / len(latencies)
            jitter = maximum - minimum
        else:
            minimum = None
            maximum = None
            average = None
            jitter = None

        return PingStats(
            packet_loss_percent=packet_loss,
            min_ms=minimum,
            average_ms=average,
            max_ms=maximum,
            jitter_ms=jitter,
        )

    except (ValueError, OSError):
        return None


def test_router(gateway: str | None) -> bool:
    """Check whether the local router is reachable."""
    if not gateway:
        return False

    stats = measure_ping(gateway, count=4)

    return stats is not None and stats.packet_loss_percent < 100


def test_internet() -> bool:
    """Check whether an external internet target is reachable."""
    stats = measure_ping("8.8.8.8", count=4)

    return stats is not None and stats.packet_loss_percent < 100


def measure_router_ping(gateway: str | None) -> PingStats | None:
    """Measure the connection between the device and local router."""
    if not gateway:
        return None

    return measure_ping(gateway)


def measure_internet_ping() -> PingStats | None:
    """Measure the connection to an external internet target."""
    return measure_ping("8.8.8.8")