from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class EvidencePage(QWidget):
    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(35, 30, 35, 30)

        title = QLabel("Evidence")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Raw measurements collected by the diagnostic engine."
        )
        subtitle.setObjectName("PageSubtitle")

        outer.addWidget(title)
        outer.addWidget(subtitle)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)

        self.label = QLabel(
            "Run a diagnostic to view evidence."
        )
        self.label.setWordWrap(True)

        self.layout.addWidget(self.label)
        self.layout.addStretch()

        self.scroll.setWidget(self.content)

        outer.addWidget(self.scroll)

    def update_result(self, result):
        evidence = result.evidence

        lines = [
            f"Diagnosis: {result.diagnosis}",
            "",
            f"Router reachable: {evidence.router_reachable}",
            f"Internet reachable: {evidence.internet_reachable}",
            f"DNS working: {evidence.dns_working}",
            "",
            f"Router packet loss: {evidence.router_packet_loss_percent}",
            f"Router latency: {evidence.router_latency_average_ms}",
            f"Router jitter: {evidence.router_jitter_ms}",
            "",
            f"Internet packet loss: {evidence.internet_packet_loss_percent}",
            f"Internet latency: {evidence.internet_latency_average_ms}",
            f"Internet jitter: {evidence.internet_jitter_ms}",
            "",
            f"Browser success rate: {evidence.request_success_rate}",
            f"Browser failure rate: {evidence.request_failure_rate}",
            f"Browser latency: {evidence.browser_latency_average_ms}",
            f"Download: {evidence.download_mbps}",
            f"Upload: {evidence.upload_mbps}",
        ]

        self.label.setText(
            "\n".join(lines)
        )