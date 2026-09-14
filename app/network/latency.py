import subprocess


def measure_latency(host: str = "8.8.8.8") -> float | None:
    """Measure approximate latency to a host in milliseconds."""

    try:
        result = subprocess.run(
            ["ping", "-n", "1", host],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            if "Average" in line:
                latency = line.split("=")[-1].strip()
                latency = latency.replace("ms", "").strip()
                return float(latency)

        return None

    except (ValueError, OSError):
        return None