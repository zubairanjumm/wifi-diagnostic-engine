import socket
import time


def test_dns(hostname: str = "google.com") -> bool:
    """Check whether DNS resolution is working."""

    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False


def measure_dns_latency(
    hostname: str = "google.com",
) -> float | None:
    """Measure how long DNS resolution takes."""

    start = time.perf_counter()

    try:
        socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

    end = time.perf_counter()

    return (end - start) * 1000