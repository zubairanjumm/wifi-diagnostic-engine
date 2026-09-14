import subprocess


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


def ping_host(host: str, count: int = 4) -> bool:
    """Check whether a host responds to ping."""

    try:
        result = subprocess.run(
            ["ping", "-n", str(count), host],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        return result.returncode == 0

    except Exception:
        return False


def test_router(gateway: str | None) -> bool:
    """Check whether the local router is reachable."""

    if not gateway:
        return False

    return ping_host(gateway)


def test_internet() -> bool:
    """Check whether an external internet target is reachable."""

    return ping_host("8.8.8.8")