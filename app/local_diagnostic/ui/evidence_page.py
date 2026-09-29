from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.local_diagnostic.report import generate_isp_report


class EvidencePage(QWidget):
    def __init__(self):
        super().__init__()

        self.result = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(35, 30, 35, 30)
        outer.setSpacing(18)

        title = QLabel("Evidence")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Measurements collected during the network diagnostic."
        )
        subtitle.setObjectName("PageSubtitle")

        outer.addWidget(title)
        outer.addWidget(subtitle)

        self.message = QLabel(
            "Run a diagnostic to view network evidence."
        )
        self.message.setObjectName("PageSubtitle")
        outer.addWidget(self.message)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(14)
        self.content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.scroll.setWidget(self.content)
        outer.addWidget(self.scroll)

        buttons = QHBoxLayout()

        self.report_button = QPushButton(
            "Save ISP Report"
        )
        self.report_button.setObjectName(
            "SecondaryButton"
        )
        self.report_button.setEnabled(False)
        self.report_button.clicked.connect(
            self.generate_report
        )

        buttons.addWidget(self.report_button)
        buttons.addStretch()

        outer.addLayout(buttons)

    def update_result(self, result):
        self.result = result
        self.report_button.setEnabled(True)

        self.message.setText(
            "Diagnostic evidence updated."
        )

        self._clear_content()

        finding = result.finding
        evidence = result.evidence

        self._add_finding_card(
            finding.title,
            finding.summary,
            finding.affected_layer,
            finding.confidence,
        )

        self._add_section(
            "Connection",
            [
                (
                    "Wi-Fi connection",
                    self._status(
                        evidence.wifi_connected
                    ),
                ),
                (
                    "Wi-Fi signal",
                    self._percent(
                        evidence.wifi_signal_percent
                    ),
                ),
                (
                    "Router",
                    self._status(
                        evidence.router_reachable
                    ),
                ),
                (
                    "Internet",
                    self._status(
                        evidence.internet_reachable
                    ),
                ),
                (
                    "DNS",
                    self._status(
                        evidence.dns_working
                    ),
                ),
            ],
        )

        local_network_rows = [
            (
                "Router latency",
                self._metric(
                    evidence.router_latency_average_ms,
                    "ms",
                ),
            ),
            (
                "Router jitter",
                self._metric(
                    evidence.router_jitter_ms,
                    "ms",
                ),
            ),
            (
                "Router packet loss",
                self._percent(
                    evidence.router_packet_loss_percent,
                ),
            ),
        ]

        if evidence.router_packet_loss_samples:
            local_network_rows.append(
                (
                    "Loss affected test rounds",
                    self._rounds(
                        evidence.router_loss_affected_samples,
                        len(
                            evidence.router_packet_loss_samples
                        ),
                    ),
                )
            )

        self._add_section(
            "Local network",
            local_network_rows,
        )

        internet_path_rows = [
            (
                "Internet latency",
                self._metric(
                    evidence.internet_latency_average_ms,
                    "ms",
                ),
            ),
            (
                "Internet jitter",
                self._metric(
                    evidence.internet_jitter_ms,
                    "ms",
                ),
            ),
            (
                "Internet packet loss",
                self._percent(
                    evidence.internet_packet_loss_percent,
                ),
            ),
        ]

        if evidence.internet_packet_loss_samples:
            internet_path_rows.append(
                (
                    "Loss affected test rounds",
                    self._rounds(
                        evidence.internet_loss_affected_samples,
                        len(
                            evidence.internet_packet_loss_samples
                        ),
                    ),
                )
            )

        self._add_section(
            "Internet path",
            internet_path_rows,
        )

        self._add_section(
            "Connection quality",
            [
                (
                    "Browser success rate",
                    self._percent(
                        evidence.request_success_rate,
                    ),
                ),
                (
                    "Browser P95 latency",
                    self._metric(
                        evidence.browser_latency_p95_ms,
                        "ms",
                    ),
                ),
                (
                    "Download",
                    self._metric(
                        evidence.download_mbps,
                        "Mbps",
                    ),
                ),
                (
                    "Upload",
                    self._metric(
                        evidence.upload_mbps,
                        "Mbps",
                    ),
                ),
            ],
        )

        self._add_section(
            "Wi-Fi details",
            [
                (
                    "Receive rate",
                    self._metric(
                        evidence.wifi_receive_rate_mbps,
                        "Mbps",
                    ),
                ),
                (
                    "Transmit rate",
                    self._metric(
                        evidence.wifi_transmit_rate_mbps,
                        "Mbps",
                    ),
                ),
                (
                    "Channel",
                    self._value(
                        evidence.wifi_channel
                    ),
                ),
                (
                    "Radio type",
                    self._value(
                        evidence.wifi_radio_type
                    ),
                ),
            ],
        )

        if finding.evidence:
            self._add_section(
                "Why this finding was reached",
                [
                    (
                        f"Evidence {index}",
                        evidence_text,
                    )
                    for index, evidence_text in enumerate(
                        finding.evidence,
                        start=1,
                    )
                ],
            )

        self.content_layout.addStretch()

    def _add_finding_card(
        self,
        title,
        summary,
        affected_layer,
        confidence,
    ):
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )
        layout.setSpacing(7)

        heading = QLabel(
            "Diagnostic finding"
        )
        heading.setObjectName("CardTitle")

        finding = QLabel(title)
        finding.setObjectName(
            "EvidenceFinding"
        )

        summary_label = QLabel(summary)
        summary_label.setWordWrap(True)

        details = QLabel(
            f"Affected area: {affected_layer}    "
            f"Confidence: {confidence}"
        )
        details.setObjectName(
            "PageSubtitle"
        )

        layout.addWidget(heading)
        layout.addWidget(finding)
        layout.addWidget(summary_label)
        layout.addWidget(details)

        self.content_layout.addWidget(card)

    def _add_section(self, title, rows):
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )
        layout.setSpacing(8)

        heading = QLabel(title)
        heading.setObjectName(
            "CardSectionTitle"
        )

        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setHorizontalSpacing(30)
        grid.setVerticalSpacing(8)

        for row, (label_text, value_text) in enumerate(
            rows
        ):
            label = QLabel(label_text)
            label.setObjectName(
                "CardTitle"
            )

            value = QLabel(value_text)
            value.setObjectName(
                "EvidenceValue"
            )

            grid.addWidget(
                label,
                row,
                0,
            )

            grid.addWidget(
                value,
                row,
                1,
            )

        layout.addLayout(grid)

        self.content_layout.addWidget(card)

    def _clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def generate_report(self):
        if self.result is None:
            return

        default_name = (
            "wifi_diagnostic_report.html"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save ISP Diagnostic Report",
            str(
                Path.home()
                / "Downloads"
                / default_name
            ),
            "HTML Files (*.html)",
        )

        if not file_path:
            return

        output_path = generate_isp_report(
            self.result,
            Path(file_path),
        )

        self.message.setText(
            f"ISP report saved to: {output_path}"
        )

    @staticmethod
    def _status(value):
        if value is None:
            return "Not measured"

        return (
            "Working"
            if value
            else "Problem detected"
        )

    @staticmethod
    def _metric(value, unit):
        if value is None:
            return "Not measured"

        return f"{value:.1f} {unit}"

    @staticmethod
    def _percent(value):
        if value is None:
            return "Not measured"

        return f"{value:.1f}%"

    @staticmethod
    def _rounds(affected_rounds, total_rounds):
        return f"{affected_rounds} / {total_rounds}"

    @staticmethod
    def _value(value):
        if value is None:
            return "Not measured"

        return str(value)