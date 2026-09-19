from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosisExplanation:
    title: str
    message: str
    next_action: str


DIAGNOSIS_EXPLANATIONS = {
    "no_obvious_problem": DiagnosisExplanation(
        title="Your connection looks stable",
        message=(
            "We did not detect significant connection failures, "
            "latency problems, or instability."
        ),
        next_action=(
            "If you're still having problems, run the diagnostic again "
            "while the problem is happening."
        ),
    ),
    "browser_connection_instability": DiagnosisExplanation(
        title="Your connection appears unstable",
        message=(
            "Some connection requests are failing repeatedly. "
            "This can cause pages, apps, or videos to load inconsistently."
        ),
        next_action=(
            "Move closer to your router if possible, then run the "
            "diagnostic again."
        ),
    ),
    "high_jitter": DiagnosisExplanation(
        title="Your connection is fluctuating",
        message=(
            "The delay between requests is changing significantly. "
            "This can cause problems with calls, gaming, and live video."
        ),
        next_action=(
            "Move closer to your router and run the diagnostic again."
        ),
    ),
    "high_latency": DiagnosisExplanation(
        title="Your connection has high delay",
        message=(
            "Requests are taking longer than expected to reach the "
            "diagnostic server."
        ),
        next_action=(
            "Try moving closer to your router and run the diagnostic again."
        ),
    ),
    "local_network_problem": DiagnosisExplanation(
        title="Your device cannot reliably reach the router",
        message=(
            "The problem appears to be between your device and your "
            "local network."
        ),
        next_action=(
            "Check your Wi-Fi connection and move closer to your router."
        ),
    ),
    "local_network_instability": DiagnosisExplanation(
        title="Your local Wi-Fi connection appears unstable",
        message=(
            "We detected packet loss between your device and the router."
        ),
        next_action=(
            "Move closer to your router and check whether other devices "
            "are experiencing the same problem."
        ),
    ),
    "internet_connection_problem": DiagnosisExplanation(
        title="Your internet connection appears unavailable",
        message=(
            "Your device can reach the router, but it cannot reliably "
            "reach the internet."
        ),
        next_action=(
            "Check your router and modem, then run the diagnostic again."
        ),
    ),
    "dns_problem": DiagnosisExplanation(
        title="There may be a DNS problem",
        message=(
            "Your device can reach the internet, but domain-name "
            "resolution is not working correctly."
        ),
        next_action=(
            "Restart your router and run the diagnostic again."
        ),
    ),
    "internet_path_instability": DiagnosisExplanation(
        title="Your internet connection appears unstable",
        message=(
            "We detected packet loss beyond your local router."
        ),
        next_action=(
            "Run the diagnostic again. If the problem continues, "
            "your internet connection may need further investigation."
        ),
    ),
}


def explain_diagnosis(diagnosis: str) -> DiagnosisExplanation:
    return DIAGNOSIS_EXPLANATIONS.get(
        diagnosis,
        DiagnosisExplanation(
            title="We found something unusual",
            message=(
                "The diagnostic detected a condition that needs "
                "further investigation."
            ),
            next_action="Run the diagnostic again.",
        ),
    )