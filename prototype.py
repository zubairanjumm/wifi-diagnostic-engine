import socket
import subprocess
import time
import re

from app.network.dns import measure_dns_latency


# --------------------------------------------------
# 1. GET YOUR DEFAULT GATEWAY
# --------------------------------------------------

def get_default_gateway():
    """
    Finds the default gateway (usually your home router).
    """

    try:
        result = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        for line in result.stdout.splitlines():
            if "Default Gateway" in line:
                gateway = line.split(":")[-1].strip()

                if gateway:
                    return gateway

    except Exception as e:
        print(f"Gateway detection error: {e}")

    return None


# --------------------------------------------------
# 2. TEST ROUTER CONNECTIVITY
# --------------------------------------------------

def test_router(gateway):
    """
    Measures connectivity and packet loss to the home router.
    """

    if not gateway:
        return {
            "status": "failed",
            "packet_loss_percent": None,
            "message": "Could not find the default gateway."
        }

    try:
        result = subprocess.run(
            ["ping", "-n", "10", gateway],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        loss_match = re.search(
            r"\((\d+)%\s*loss\)",
            result.stdout
        )

        if not loss_match:
            return {
                "status": "failed",
                "packet_loss_percent": None,
                "message": "Could not determine router packet loss."
            }

        packet_loss = float(loss_match.group(1))

        if packet_loss < 100:
            return {
                "status": "ok",
                "packet_loss_percent": packet_loss,
                "message": f"Router {gateway} is reachable."
            }

        return {
            "status": "failed",
            "packet_loss_percent": packet_loss,
            "message": f"Router {gateway} is not reachable."
        }

    except Exception as e:
        return {
            "status": "failed",
            "packet_loss_percent": None,
            "message": str(e)
        }


# --------------------------------------------------
# 3. TEST INTERNET CONNECTIVITY
# --------------------------------------------------

def test_internet():
    """
    Measures internet connectivity and packet loss.
    """

    target = "8.8.8.8"

    try:
        result = subprocess.run(
            ["ping", "-n", "10", target],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        loss_match = re.search(
            r"\((\d+)%\s*loss\)",
            result.stdout
        )

        if not loss_match:
            return {
                "status": "failed",
                "packet_loss_percent": None,
                "message": "Could not determine internet packet loss."
            }

        packet_loss = float(loss_match.group(1))

        if packet_loss < 100:
            return {
                "status": "ok",
                "packet_loss_percent": packet_loss,
                "message": "Internet is reachable."
            }

        return {
            "status": "failed",
            "packet_loss_percent": packet_loss,
            "message": "Internet is not reachable."
        }

    except Exception as e:
        return {
            "status": "failed",
            "packet_loss_percent": None,
            "message": str(e)
        }


# --------------------------------------------------
# 4. TEST DNS
# --------------------------------------------------

def test_dns():
    """
    Tests whether DNS can resolve a domain name.
    """

    domain = "google.com"

    try:
        ip = socket.gethostbyname(domain)

        return {
            "status": "ok",
            "message": f"DNS is working. {domain} -> {ip}"
        }

    except socket.gaierror:
        return {
            "status": "failed",
            "message": "DNS resolution failed."
        }


# --------------------------------------------------
# 5. MEASURE LATENCY
# --------------------------------------------------

def measure_latency():
    target = "8.8.8.8"

    try:
        result = subprocess.run(
            ["ping", "-n", "10", target],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        latencies = []

        for line in result.stdout.splitlines():
            match = re.search(r"time[=<](\d+(?:\.\d+)?)ms", line)

            if match:
                latencies.append(float(match.group(1)))

        if not latencies:
            return {
                "status": "failed",
                "message": "Could not measure latency."
            }

        minimum = min(latencies)
        maximum = max(latencies)
        average = sum(latencies) / len(latencies)
        jitter = maximum - minimum

        return {
            "status": "ok",
            "min_ms": round(minimum, 2),
            "average_ms": round(average, 2),
            "max_ms": round(maximum, 2),
            "jitter_ms": round(jitter, 2),
            "message": (
                f"Average latency: {average:.2f} ms | "
                f"Min: {minimum:.2f} ms | "
                f"Max: {maximum:.2f} ms | "
                f"Jitter: {jitter:.2f} ms"
            )
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }

# --------------------------------------------------
# 6. RUN COMPLETE DIAGNOSTIC
# --------------------------------------------------

def run_diagnostic():

    print("=" * 50)
    print("        WIFI DIAGNOSTIC PROTOTYPE")
    print("=" * 50)

    print("\n[1] Finding router...")

    gateway = get_default_gateway()

    if gateway:
        print(f"    Router found: {gateway}")
    else:
        print("    Router not found.")

    print("\n[2] Testing router connectivity...")

    router_result = test_router(gateway)

    print(f"    {router_result['message']}")

    if router_result["packet_loss_percent"] is not None:
        print(
            f"    Router packet loss: "
            f"{router_result['packet_loss_percent']:.1f}%"
        )

    print("\n[3] Testing internet connectivity...")

    internet_result = test_internet()

    print(f"    {internet_result['message']}")

    if internet_result["packet_loss_percent"] is not None:
        print(
            f"    Internet packet loss: "
            f"{internet_result['packet_loss_percent']:.1f}%"
        )

    print("\n[4] Testing DNS...")

    dns_result = test_dns()

    print(f"    {dns_result['message']}")

    dns_latency = measure_dns_latency()

    if dns_latency is not None:
        print(
            f"    DNS response time: "
            f"{dns_latency:.1f} ms"
        )
    else:
        print("    DNS response time: unavailable")

    print("\n[5] Measuring latency...")

    latency_result = measure_latency()

    print(f"    {latency_result['message']}")

    # ----------------------------------------------
    # DIAGNOSIS
    # ----------------------------------------------

    print("\n" + "=" * 50)
    print("DIAGNOSIS")
    print("=" * 50)

    if router_result["status"] == "failed":

        print("\nProblem: Your computer cannot reach your router.")
        print("Likely area: Local Wi-Fi/network connection.")

    elif internet_result["status"] == "failed":

        print("\nProblem: Your router is reachable, but the internet")
        print("cannot be reached.")
        print("Likely area: ISP/modem/internet connection.")

    elif dns_result["status"] == "failed":

        print("\nProblem: Internet connectivity works, but DNS")
        print("resolution is failing.")
        print("Likely area: DNS configuration/service.")

    else:

        print("\nNo obvious connectivity problem detected.")
        print("Router: reachable")
        print("Internet: reachable")
        print("DNS: working")

    if latency_result["status"] == "ok":
        print(f"Average latency: {latency_result['average_ms']} ms")
        print(f"Minimum latency: {latency_result['min_ms']} ms")
        print(f"Maximum latency: {latency_result['max_ms']} ms")
        print(f"Jitter: {latency_result['jitter_ms']} ms")

    print("\n" + "=" * 50)


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    run_diagnostic()

