from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
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
            "Review previous diagnostic runs."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.list = QListWidget()

        layout.addWidget(self.list)

    def add_result(self, result):
        self.history.append(result)

        evidence = result.evidence

        latency = evidence.internet_latency_average_ms

        latency_text = (
            "--"
            if latency is None
            else f"{latency:.1f} ms"
        )

        text = (
            f"{result.diagnosis.replace('_', ' ').title()}   "
            f"•   Latency: {latency_text}"
        )

        self.list.insertItem(
            0,
            text,
        )