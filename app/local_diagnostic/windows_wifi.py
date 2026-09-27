import re
import subprocess
from dataclasses import dataclass


CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


@dataclass
class WindowsWiFiEvidence:
    connected: bool | None = None
    signal_percent: float | None = None
    receive_rate_mbps: float | None = None
    transmit_rate_mbps: float | None = None
    channel: int | None = None
    radio_type: str | None = None


def _run_netsh_wlan() -> str | None:
    """Return Windows Wi-Fi interface information."""

    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            creationflags=CREATE_NO_WINDOW,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    return result.stdout


def _extract_number(
    output: str,
    pattern: str,
) -> float | None:
    match = re.search(
        pattern,
        output,
        re.IGNORECASE,
    )

    if not match:
        return None

    try:
        return float(match.group(1))
    except ValueError:
        return None


def collect_windows_wifi_evidence() -> WindowsWiFiEvidence:
    """
    Collect lightweight Wi-Fi interface evidence from Windows.

    SSID and BSSID are intentionally not collected because they are
    unnecessary for the diagnostic engine.
    """

    output = _run_netsh_wlan()

    if not output:
        return WindowsWiFiEvidence()

    state_match = re.search(
        r"^\s*State\s*:\s*(.+?)\s*$",
        output,
        re.IGNORECASE | re.MULTILINE,
    )

    state = state_match.group(1).strip().lower() if state_match else None

    signal = _extract_number(
        output,
        r"^\s*Signal\s*:\s*(\d+(?:\.\d+)?)\s*%",
    )

    receive_rate = _extract_number(
        output,
        r"^\s*Receive rate \(Mbps\)\s*:\s*(\d+(?:\.\d+)?)",
    )

    transmit_rate = _extract_number(
        output,
        r"^\s*Transmit rate \(Mbps\)\s*:\s*(\d+(?:\.\d+)?)",
    )

    channel_value = _extract_number(
        output,
        r"^\s*Channel\s*:\s*(\d+)",
    )

    radio_match = re.search(
        r"^\s*Radio type\s*:\s*(.+?)\s*$",
        output,
        re.IGNORECASE | re.MULTILINE,
    )

    radio_type = (
        radio_match.group(1).strip()
        if radio_match
        else None
    )

    connected = None

    if state is not None:
        connected = state == "connected"

    return WindowsWiFiEvidence(
        connected=connected,
        signal_percent=signal,
        receive_rate_mbps=receive_rate,
        transmit_rate_mbps=transmit_rate,
        channel=(
            int(channel_value)
            if channel_value is not None
            else None
        ),
        radio_type=radio_type,
    )