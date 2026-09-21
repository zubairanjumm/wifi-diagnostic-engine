from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MetricCard(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        self.value = QLabel("--")
        self.value.setObjectName("CardValue")

        self.detail = QLabel("")
        self.detail.setObjectName("CardTitle")

        layout.addWidget(title_label)
        layout.addWidget(self.value)
        layout.addWidget(self.detail)


class DashboardPage(QWidget):
    run_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        title = QLabel("Connection Health")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Understand the condition of your home network."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        health_card = QFrame()
        health_card.setObjectName("Card")

        health_layout = QVBoxLayout(health_card)
        health_layout.setContentsMargins(24, 20, 24, 20)

        health_title = QLabel("Current status")
        health_title.setObjectName("CardTitle")

        self.health_status = QLabel("No diagnostic yet")
        self.health_status.setObjectName("PageTitle")

        self.health_message = QLabel(
            "Run a diagnostic to measure your connection."
        )
        self.health_message.setObjectName("PageSubtitle")

        health_layout.addWidget(health_title)
        health_layout.addWidget(self.health_status)
        health_layout.addWidget(self.health_message)

        layout.addWidget(health_card)

        grid = QGridLayout()
        grid.setSpacing(14)

        self.router_card = MetricCard("Router")
        self.internet_card = MetricCard("Internet")
        self.dns_card = MetricCard("DNS")
        self.latency_card = MetricCard("Latency")

        grid.addWidget(self.router_card, 0, 0)
        grid.addWidget(self.internet_card, 0, 1)
        grid.addWidget(self.dns_card, 1, 0)
        grid.addWidget(self.latency_card, 1, 1)

        layout.addLayout(grid)

        bottom = QHBoxLayout()

        self.run_button = QPushButton("Run Diagnostic")
        self.run_button.clicked.connect(self.run_requested.emit)

        bottom.addWidget(self.run_button)
        bottom.addStretch()

        layout.addLayout(bottom)
        layout.addStretch()

    def update_result(self, result):
        diagnosis = result.diagnosis
        evidence = result.evidence

        diagnosis_titles = {
            "no_obvious_problem": "Stable",
            "local_network_problem": "Local network problem",
            "local_network_instability": "Local instability",
            "internet_connection_problem": "Internet unavailable",
            "internet_path_instability": "Internet instability",
            "dns_problem": "DNS problem",
            "high_latency": "High latency",
            "high_jitter": "High jitter",
            "browser_connection_instability": "Connection instability",
        }

        self.health_status.setText(
            diagnosis_titles.get(
                diagnosis,
                "Unusual network condition",
            )
        )

        self.health_message.setText(
            result.recommendation.title
        )

        self.router_card.value.setText(
            "OK" if evidence.router_reachable else "Problem"
        )

        self.router_card.detail.setText(
            self._metric(
                evidence.router_latency_average_ms,
                "ms",
            )
        )

        self.internet_card.value.setText(
            "OK" if evidence.internet_reachable else "Problem"
        )

        self.internet_card.detail.setText(
            self._metric(
                evidence.internet_latency_average_ms,
                "ms",
            )
        )

        self.dns_card.value.setText(
            "Working" if evidence.dns_working else "Problem"
        )

        self.dns_card.detail.setText("DNS resolution")

        self.latency_card.value.setText(
            self._metric(
                evidence.internet_latency_average_ms,
                "ms",
            )
        )

        self.latency_card.detail.setText(
            self._metric(
                evidence.internet_jitter_ms,
                "jitter",
            )
        )

    @staticmethod
    def _metric(value, suffix):
        if value is None:
            return "--"

        return f"{value:.1f} {suffix}"