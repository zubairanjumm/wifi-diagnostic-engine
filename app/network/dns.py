import socket


def resolve_hostname(hostname: str) -> str | None:
    """Resolve a hostname and return its IP address."""

    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def test_dns() -> bool:
    """Check whether DNS resolution is working."""

    return resolve_hostname("google.com") is not None