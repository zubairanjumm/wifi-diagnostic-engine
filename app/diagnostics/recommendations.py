from dataclasses import dataclass

from app.diagnostics.models import NetworkEvidence


@dataclass(frozen=True)
class Recommendation:
    title: str
    steps: tuple[str, ...]


def recommend(
    diagnosis: str,
    evidence: NetworkEvidence,
) -> Recommendation:
    """
    Generate the next troubleshooting action from both
    the diagnosis and the evidence that produced it.
    """

    if diagnosis == "no_obvious_problem":
        return Recommendation(
            title="No network change is needed right now",
            steps=(
                "Your measured connection looks stable.",
                "If you are still experiencing a problem, run the diagnostic while the problem is happening.",
            ),
        )

    if diagnosis == "local_network_problem":
        return Recommendation(
            title="Check the connection between your device and router",
            steps=(
                "Check that Wi-Fi is enabled and connected to your normal network.",
                "Move closer to the router and run the diagnostic again.",
                "If other devices also cannot connect, check the router itself.",
            ),
        )

    if diagnosis == "local_network_instability":
        if (
            evidence.router_packet_loss_percent is not None
            and evidence.router_packet_loss_percent >= 10
        ):
            return Recommendation(
                title="Your device is losing packets to the router",
                steps=(
                    "Move closer to the router and run the diagnostic again.",
                    "If possible, try a different Wi-Fi band or Ethernet.",
                    "If packet loss remains high near the router, test another device on the same network.",
                ),
            )

        if (
            evidence.router_latency_average_ms is not None
            and evidence.router_latency_average_ms > 150
        ):
            return Recommendation(
                title="The connection to your router is unusually slow",
                steps=(
                    "Check whether the problem improves closer to the router.",
                    "If possible, try another Wi-Fi band or Ethernet.",
                    "Run the diagnostic again after the change.",
                ),
            )

        return Recommendation(
            title="Your local Wi-Fi connection is unstable",
            steps=(
                "Move closer to the router and run the diagnostic again.",
                "If possible, compare the result with Ethernet or another Wi-Fi band.",
            ),
        )

    if diagnosis == "internet_connection_problem":
        return Recommendation(
            title="Your router is reachable, but the internet is not",
            steps=(
                "Check another device connected to the same network.",
                "If multiple devices are offline, check the modem/router connection.",
                "If the problem continues on multiple devices, check your ISP for an outage.",
            ),
        )

    if diagnosis == "internet_path_instability":
        return Recommendation(
            title="The problem appears beyond your local router",
            steps=(
                "Your router is responding normally, but packet loss is occurring beyond it.",
                "Test another device on the same network.",
                "If multiple devices show the same problem, the issue may require ISP investigation.",
                "Run the diagnostic again later to see whether the packet loss persists.",
            ),
        )

    if diagnosis == "dns_problem":
        return Recommendation(
            title="Your internet works, but DNS resolution is failing",
            steps=(
                "Check whether other devices on the same network have the same problem.",
                "If only this device is affected, check its DNS/network settings.",
                "Run the diagnostic again after making a DNS change.",
            ),
        )

    if diagnosis == "high_latency":
        if (
            evidence.router_latency_average_ms is not None
            and evidence.router_latency_average_ms > 150
        ):
            return Recommendation(
                title="Most of the delay appears to be on your local connection",
                steps=(
                    "Move closer to the router and run the diagnostic again.",
                    "If possible, compare the result with Ethernet.",
                    "If latency remains high near the router, investigate local Wi-Fi congestion.",
                ),
            )

        return Recommendation(
            title="Your internet connection has unusually high delay",
            steps=(
                "Run the diagnostic again to confirm the result.",
                "If the router connection is healthy but internet latency remains high, test another device.",
                "If multiple devices show the same result, the issue may be outside your home network.",
            ),
        )

    if diagnosis == "high_jitter":
        if (
            evidence.router_jitter_ms is not None
            and evidence.router_jitter_ms >= 100
        ):
            return Recommendation(
                title="The connection to your router is fluctuating",
                steps=(
                    "Move closer to the router and run the diagnostic again.",
                    "If possible, try another Wi-Fi band or Ethernet.",
                    "Compare the result after the change.",
                ),
            )

        return Recommendation(
            title="Your connection has inconsistent latency",
            steps=(
                "Run the diagnostic again while the problem is happening.",
                "If possible, compare Wi-Fi with Ethernet.",
                "If multiple devices experience the same fluctuation, investigate the wider network connection.",
            ),
        )

    if diagnosis == "browser_connection_instability":
        return Recommendation(
            title="Some connection requests are failing",
            steps=(
                "Run the diagnostic again to confirm the failures are repeatable.",
                "If possible, compare the result on another network.",
                "If failures only occur on this network, investigate the network connection rather than the browser itself.",
            ),
        )

    return Recommendation(
        title="Run the diagnostic again",
        steps=(
            "The available evidence is not sufficient for a more specific recommendation.",
        ),
    )