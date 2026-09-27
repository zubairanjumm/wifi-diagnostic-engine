from unittest.mock import patch

from app.local_diagnostic.collector import collect_local_diagnostic
from app.local_diagnostic.report import generate_isp_report


def test_generate_isp_report(tmp_path):
    with (
        patch(
            "app.local_diagnostic.collector.get_default_gateway",
            return_value="192.168.1.1",
        ),
        patch(
            "app.local_diagnostic.collector.collect_windows_wifi_evidence",
            return_value=type(
                "FakeWiFiEvidence",
                (),
                {
                    "connected": True,
                    "signal_percent": 80.0,
                    "receive_rate_mbps": 866.0,
                    "transmit_rate_mbps": 866.0,
                    "channel": 36,
                    "radio_type": "802.11ac",
                },
            )(),
        ),
        patch(
            "app.local_diagnostic.collector.measure_router_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_internet_ping",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.measure_dns_latency",
            return_value=None,
        ),
        patch(
            "app.local_diagnostic.collector.test_dns",
            return_value=False,
        ),
    ):
        result = collect_local_diagnostic()

    output = tmp_path / "diagnostic_report.html"

    report_path = generate_isp_report(result, output)

    assert report_path.exists()

    content = report_path.read_text(encoding="utf-8")

    assert "Internet Connection Diagnostic Report" in content
    assert "Summary for ISP" in content
    assert "Observed Evidence" in content
    assert "Recommendation" in content