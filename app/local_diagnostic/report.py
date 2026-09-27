from datetime import datetime
from html import escape
from pathlib import Path

from app.local_diagnostic.collector import LocalDiagnosticResult


def _value(value: object, unit: str = "") -> str:
    if value is None:
        return "Not measured"

    return f"{value}{unit}"


def _status(value: bool | None) -> str:
    if value is True:
        return "Yes"

    if value is False:
        return "No"

    return "Not determined"


def _build_isp_summary(result: LocalDiagnosticResult) -> str:
    finding = result.finding

    if finding.code == "internet_path_instability":
        return (
            "The local router was reachable during testing, but packet loss "
            "was detected on the internet path. This pattern may indicate a "
            "problem beyond the local Wi-Fi network. ISP investigation is "
            "recommended."
        )

    if finding.code == "local_network_instability":
        return (
            "The router connection showed signs of instability during testing. "
            "This suggests the problem may be within the local Wi-Fi or LAN "
            "connection rather than the wider internet path."
        )

    if finding.code == "internet_connection_problem":
        return (
            "The local router was reachable, but the internet connection "
            "could not be reached during testing. Please investigate the "
            "internet/WAN connection."
        )

    if finding.code == "dns_problem":
        return (
            "Internet connectivity was available, but DNS resolution failed "
            "during testing. DNS configuration or the ISP DNS service may "
            "need investigation."
        )

    if finding.code == "high_latency":
        return (
            "The connection showed higher-than-expected latency during testing. "
            "This can cause slow responses and delays in applications."
        )

    if finding.code == "high_jitter":
        return (
            "The connection showed significant variation in latency during "
            "testing. This can affect calls, gaming, and other real-time traffic."
        )

    if finding.code == "browser_connection_instability":
        return (
            "Repeated connection requests showed instability. Further ISP "
            "investigation may be useful if the problem is reproducible."
        )

    return (
        "No obvious network problem was detected during this diagnostic. "
        "The issue may be intermittent or may not have been present during testing."
    )


def _build_evidence_rows(result: LocalDiagnosticResult) -> str:
    evidence = result.evidence

    rows = [
        ("Router reachable", _status(evidence.router_reachable)),
        ("Internet reachable", _status(evidence.internet_reachable)),
        ("DNS working", _status(evidence.dns_working)),
        (
            "Router packet loss",
            _value(evidence.router_packet_loss_percent, "%"),
        ),
        (
            "Internet packet loss",
            _value(evidence.internet_packet_loss_percent, "%"),
        ),
        (
            "Router average latency",
            _value(evidence.router_latency_average_ms, " ms"),
        ),
        (
            "Internet average latency",
            _value(evidence.internet_latency_average_ms, " ms"),
        ),
        (
            "Router jitter",
            _value(evidence.router_jitter_ms, " ms"),
        ),
        (
            "Internet jitter",
            _value(evidence.internet_jitter_ms, " ms"),
        ),
        (
            "DNS latency",
            _value(evidence.dns_latency_ms, " ms"),
        ),
        ("Wi-Fi connected", _status(evidence.wifi_connected)),
        (
            "Wi-Fi signal",
            _value(evidence.wifi_signal_percent, "%"),
        ),
        (
            "Wi-Fi receive rate",
            _value(evidence.wifi_receive_rate_mbps, " Mbps"),
        ),
        (
            "Wi-Fi transmit rate",
            _value(evidence.wifi_transmit_rate_mbps, " Mbps"),
        ),
        (
            "Wi-Fi channel",
            _value(evidence.wifi_channel),
        ),
        (
            "Wi-Fi radio type",
            _value(evidence.wifi_radio_type),
        ),
    ]

    return "\n".join(
        f"""
        <tr>
            <td>{escape(label)}</td>
            <td>{escape(value)}</td>
        </tr>
        """
        for label, value in rows
    )


def _build_recommendation(result: LocalDiagnosticResult) -> str:
    recommendation = result.recommendation

    steps = "\n".join(
        f"<li>{escape(step)}</li>"
        for step in recommendation.steps
    )

    return f"""
        <p>
            <strong>{escape(recommendation.title)}</strong>
        </p>

        <ul>
            {steps}
        </ul>
    """


def generate_isp_report(
    result: LocalDiagnosticResult,
    output_path: str | Path,
) -> Path:
    """Generate a simple HTML report that can be provided to an ISP."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    evidence_rows = _build_evidence_rows(result)
    isp_summary = _build_isp_summary(result)
    recommendation = _build_recommendation(result)

    evidence_list = "\n".join(
        f"<li>{escape(item)}</li>"
        for item in result.finding.evidence
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Internet Connection Diagnostic Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 40px auto;
            padding: 0 24px;
            color: #222;
            line-height: 1.5;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        h2 {{
            margin-top: 32px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 6px;
        }}

        .summary {{
            border: 1px solid #ccc;
            padding: 18px;
            margin-top: 20px;
        }}

        .finding {{
            font-size: 20px;
            font-weight: bold;
        }}

        .meta {{
            color: #666;
            font-size: 14px;
        }}

        .isp {{
            background: #f5f5f5;
            border-left: 4px solid #333;
            padding: 16px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th,
        td {{
            border-bottom: 1px solid #ddd;
            padding: 9px;
            text-align: left;
        }}

        th {{
            background: #f5f5f5;
        }}

        .footer {{
            margin-top: 40px;
            color: #777;
            font-size: 13px;
        }}
    </style>
</head>

<body>

    <h1>Internet Connection Diagnostic Report</h1>

    <p class="meta">
        Generated: {escape(generated_at)}
    </p>

    <div class="summary">

        <div class="finding">
            {escape(result.finding.title)}
        </div>

        <p>
            {escape(result.finding.summary)}
        </p>

        <p>
            <strong>Affected area:</strong>
            {escape(result.finding.affected_layer)}
        </p>

        <p>
            <strong>Confidence:</strong>
            {escape(result.finding.confidence)}
        </p>

    </div>

    <h2>Summary for ISP</h2>

    <div class="isp">
        {escape(isp_summary)}
    </div>

    <h2>Observed Evidence</h2>

    <table>

        <thead>
            <tr>
                <th>Measurement</th>
                <th>Result</th>
            </tr>
        </thead>

        <tbody>
            {evidence_rows}
        </tbody>

    </table>

    <h2>Why This Finding Was Made</h2>

    <ul>
        {evidence_list}
    </ul>

    <h2>Recommendation</h2>

    {recommendation}

    <h2>Diagnostic Result</h2>

    <p>
        <strong>Diagnosis:</strong>
        {escape(result.diagnosis)}
    </p>

    <div class="footer">
        This report contains measurements collected during the diagnostic
        period. It does not guarantee the location of the fault. Network
        conditions can change over time.
    </div>

</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")

    return output_path