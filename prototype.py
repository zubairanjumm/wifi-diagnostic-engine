import socket
import subprocess
import time


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
    Checks whether we can reach the home router.
    """

    if not gateway:
        return {
            "status": "failed",
            "message": "Could not find the default gateway."
        }

    try:
        result = subprocess.run(
            ["ping", "-n", "4", gateway],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if result.returncode == 0:
            return {
                "status": "ok",
                "message": f"Router {gateway} is reachable."
            }

        return {
            "status": "failed",
            "message": f"Router {gateway} is not reachable."
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }


# --------------------------------------------------
# 3. TEST INTERNET CONNECTIVITY
# --------------------------------------------------

def test_internet():
    """
    Checks whether the computer can reach the internet.
    """

    target = "8.8.8.8"

    try:
        result = subprocess.run(
            ["ping", "-n", "4", target],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if result.returncode == 0:
            return {
                "status": "ok",
                "message": "Internet is reachable."
            }

        return {
            "status": "failed",
            "message": "Internet is not reachable."
        }

    except Exception as e:
        return {
            "status": "failed",
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
    """
    Measures approximate latency to Google's DNS server.
    """

    target = "8.8.8.8"

    try:
        start = time.perf_counter()

        result = subprocess.run(
            ["ping", "-n", "1", target],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        end = time.perf_counter()

        if result.returncode == 0:
            latency_ms = round((end - start) * 1000, 2)

            return {
                "status": "ok",
                "latency_ms": latency_ms,
                "message": f"Latency is approximately {latency_ms} ms."
            }

        return {
            "status": "failed",
            "message": "Could not measure latency."
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

    print("\n[3] Testing internet connectivity...")

    internet_result = test_internet()

    print(f"    {internet_result['message']}")

    print("\n[4] Testing DNS...")

    dns_result = test_dns()

    print(f"    {dns_result['message']}")

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
            print(f"Latency: {latency_result['latency_ms']} ms")

    print("\n" + "=" * 50)


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    run_diagnostic()