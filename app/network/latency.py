import re
import subprocess
from dataclasses import dataclass


@dataclass
class LatencyStats:
    """Summary of multiple latency measurements."""

    min_ms: float
    average_ms: float
    max_ms: float


def measure_latency(
    host: str = "8.8.8.8",
    count: int = 10,
) -> LatencyStats | None:
    """Measure latency multiple times and return summary statistics."""

    try:
        result = subprocess.run(
            ["ping", "-n", str(count), host],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        if result.returncode != 0:
            return None

        latencies = []

        for line in result.stdout.splitlines():
            match = re.search(r"time[=<](\d+(?:\.\d+)?)ms", line)

            if match:
                latencies.append(float(match.group(1)))

        if not latencies:
            return None

        return LatencyStats(
            min_ms=min(latencies),
            average_ms=sum(latencies) / len(latencies),
            max_ms=max(latencies),
        )

    except (ValueError, OSError):
        return None