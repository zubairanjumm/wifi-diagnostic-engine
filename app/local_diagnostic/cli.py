from app.local_diagnostic.collector import collect_local_diagnostic


EXPLANATIONS = {
    "no_obvious_problem": (
        "Your connection looks stable based on the evidence collected."
    ),
    "local_network_problem": (
        "Your computer is having trouble communicating with the router."
    ),
    "local_network_instability": (
        "There is packet loss between your computer and the router."
    ),
    "internet_connection_problem": (
        "Your computer can reach the router, but the internet is not reachable."
    ),
    "internet_path_instability": (
        "There is packet loss between your network and the internet."
    ),
    "high_latency": (
        "The connection is responding more slowly than expected."
    ),
    "high_jitter": (
        "Latency is varying significantly during the test."
    ),
    "dns_problem": (
        "DNS resolution is not working correctly."
    ),
    "browser_connection_instability": (
        "The connection to the diagnostic service is intermittently failing."
    ),
}


ACTIONS = {
    "no_obvious_problem": (
        "No immediate network change is required. "
        "If you still experience problems, run another diagnostic."
    ),
    "local_network_problem": (
        "Move closer to the router and check whether other devices "
        "can connect to it."
    ),
    "local_network_instability": (
        "Move closer to the router and retest. "
        "If multiple devices have the same problem, restart the router."
    ),
    "internet_connection_problem": (
        "Check another device on the same network. "
        "If multiple devices are affected, restart the router."
    ),
    "internet_path_instability": (
        "Retest the connection. If multiple devices are affected, "
        "the problem may be beyond your local network."
    ),
    "high_latency": (
        "Move closer to the router and retest. "
        "If possible, compare the result with an Ethernet connection."
    ),
    "high_jitter": (
        "Move closer to the router and retest. "
        "If the problem continues, compare with Ethernet or another network."
    ),
    "dns_problem": (
        "Check whether other devices have the same DNS problem."
    ),
    "browser_connection_instability": (
        "Retest the connection and compare with another network."
    ),
}


def print_value(label: str, value: object) -> None:
    print(f"{label:<32} {value}")


def print_diagnosis(result) -> None:
    evidence = result.evidence
    diagnosis = result.diagnosis

    print()
    print("=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    print()

    print(diagnosis.replace("_", " ").upper())
    print()

    print(EXPLANATIONS.get(
        diagnosis,
        "The diagnostic engine detected a network condition that needs investigation.",
    ))

    print()
    print("Evidence")
    print("-" * 60)

    print_value("Router packet loss:", evidence.router_packet_loss_percent)
    print_value("Router latency:", evidence.router_latency_average_ms)
    print_value("Router jitter:", evidence.router_jitter_ms)

    print_value("Internet packet loss:", evidence.internet_packet_loss_percent)
    print_value("Internet latency:", evidence.internet_latency_average_ms)
    print_value("Internet jitter:", evidence.internet_jitter_ms)

    print_value("DNS latency:", evidence.dns_latency_ms)

    print()
    print("What to try")
    print("-" * 60)
    print(ACTIONS.get(
        diagnosis,
        "Run the diagnostic again after checking your connection.",
    ))
    print()


def main() -> None:
    print()
    print("=" * 60)
    print("                 WIFI DIAGNOSTIC")
    print("=" * 60)
    print()
    print("Collecting local network evidence...")
    print()

    result = collect_local_diagnostic()

    print()
    print("--- Connection ---")

    evidence = result.evidence

    print_value("Default gateway:", result.gateway)
    print_value("Router reachable:", evidence.router_reachable)
    print_value("Internet reachable:", evidence.internet_reachable)
    print_value("DNS working:", evidence.dns_working)

    print_diagnosis(result)


if __name__ == "__main__":
    main()