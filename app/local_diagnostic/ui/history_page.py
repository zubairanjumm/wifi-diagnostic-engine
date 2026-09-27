from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.history = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        title = QLabel("Diagnostic History")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Previous diagnostic results from this session."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.list = QListWidget()
        layout.addWidget(self.list)

    def add_result(self, result):
        self.history.insert(0, result)

        evidence = result.evidence
        finding = result.finding

        latency = self._metric(
            evidence.internet_latency_average_ms,
            "ms",
        )

        jitter = self._metric(
            evidence.internet_jitter_ms,
            "ms",
        )

        packet_loss = self._metric(
            evidence.internet_packet_loss_percent,
            "%",
        )

        item = QListWidgetItem()

        card = QFrame()
        card.setObjectName("Card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(6)

        title_row = QHBoxLayout()

        finding_label = QLabel(finding.title)
        finding_label.setObjectName("CardSectionTitle")

        confidence_label = QLabel(
            f"Confidence: {finding.confidence}"
        )
        confidence_label.setObjectName("CardTitle")

        title_row.addWidget(finding_label)
        title_row.addStretch()
        title_row.addWidget(confidence_label)

        card_layout.addLayout(title_row)

        summary = QLabel(finding.summary)
        summary.setWordWrap(True)
        summary.setObjectName("PageSubtitle")

        card_layout.addWidget(summary)

        metrics = QLabel(
            f"Latency: {latency}    "
            f"Jitter: {jitter}    "
            f"Packet loss: {packet_loss}"
        )
        metrics.setObjectName("EvidenceValue")

        card_layout.addWidget(metrics)

        affected = QLabel(
            f"Affected area: {finding.affected_layer}"
        )
        affected.setObjectName("CardTitle")

        card_layout.addWidget(affected)

        self.list.insertItem(0, item)
        item.setSizeHint(card.sizeHint())
        self.list.setItemWidget(item, card)

    @staticmethod
    def _metric(value, unit):
        if value is None:
            return "--"

        return f"{value:.1f} {unit}"