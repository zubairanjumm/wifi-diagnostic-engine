import time

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

from app.local_diagnostic.monitor import (
    DiagnosticMonitor,
    MonitorRun,
)


class MonitorPage(QWidget):
    result_received = Signal(object)

    def __init__(self):
        super().__init__()

        self.monitor = None
        self.started_at = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        title = QLabel("Continuous Monitor")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Repeatedly measure your connection until you stop monitoring."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        status_card = QFrame()
        status_card.setObjectName("Card")

        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(20, 20, 20, 20)

        self.status = QLabel("Not monitoring")
        self.status.setObjectName("PageTitle")

        self.run_number = QLabel("Runs: 0")
        self.run_number.setObjectName("PageSubtitle")

        self.duration = QLabel("Duration: 0s")
        self.duration.setObjectName("PageSubtitle")

        status_layout.addWidget(self.status)
        status_layout.addWidget(self.run_number)
        status_layout.addWidget(self.duration)

        layout.addWidget(status_card)

        grid = QGridLayout()
        grid.setSpacing(14)

        self.latency = self.make_metric("Latency")
        self.jitter = self.make_metric("Jitter")
        self.packet_loss = self.make_metric("Packet Loss")
        self.diagnosis = self.make_metric("Diagnosis")

        grid.addWidget(self.latency, 0, 0)
        grid.addWidget(self.jitter, 0, 1)
        grid.addWidget(self.packet_loss, 1, 0)
        grid.addWidget(self.diagnosis, 1, 1)

        layout.addLayout(grid)

        buttons = QHBoxLayout()

        self.start_button = QPushButton("Start Monitoring")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("SecondaryButton")

        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)

        self.stop_button.setEnabled(False)

        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)
        buttons.addStretch()

        layout.addLayout(buttons)
        layout.addStretch()

    def make_metric(self, title):
        frame = QFrame()
        frame.setObjectName("Card")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 16, 18, 16)

        label = QLabel(title)
        label.setObjectName("CardTitle")

        value = QLabel("--")
        value.setObjectName("CardValue")

        layout.addWidget(label)
        layout.addWidget(value)

        frame.value_label = value

        return frame

    def start_monitoring(self):
        if self.monitor and self.monitor.running:
            return

        self.started_at = time.time()

        self.monitor = DiagnosticMonitor(
            interval_seconds=30,
            on_result=self.handle_result,
            on_error=self.handle_error,
        )

        self.status.setText("Monitoring...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.monitor.start()

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop()

        self.status.setText("Monitoring stopped")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def handle_result(self, monitor_run: MonitorRun):
        self.run_number.setText(
            f"Runs: {monitor_run.number}"
        )

        evidence = monitor_run.result.evidence

        latency = evidence.internet_latency_average_ms
        jitter = evidence.internet_jitter_ms
        loss = evidence.internet_packet_loss_percent

        self.latency.value_label.setText(
            "--" if latency is None else f"{latency:.1f} ms"
        )

        self.jitter.value_label.setText(
            "--" if jitter is None else f"{jitter:.1f} ms"
        )

        self.packet_loss.value_label.setText(
            "--" if loss is None else f"{loss:.1f}%"
        )

        self.diagnosis.value_label.setText(
            monitor_run.result.diagnosis.replace("_", " ").title()
        )

        if self.started_at:
            elapsed = int(time.time() - self.started_at)
            self.duration.setText(
                f"Duration: {elapsed}s"
            )

        self.result_received.emit(monitor_run)

    def handle_error(self, error):
        self.status.setText(
            f"Monitoring error: {error}"
        )