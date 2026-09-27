from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from app.local_diagnostic.collector import collect_local_diagnostic


class DiagnosticWorker(QObject):
    finished = Signal(object)
    failed = Signal(str)
    progress = Signal(str, str)

    @Slot()
    def run(self):
        try:
            result = collect_local_diagnostic(
                progress_callback=self.progress.emit,
            )
            self.finished.emit(result)
        except Exception as error:
            self.failed.emit(str(error))


class DiagnosticPage(QWidget):
    finished = Signal(object)

    def __init__(self):
        super().__init__()

        self.thread = None
        self.worker = None
        self.current_progress = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        title = QLabel("Diagnostic")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Measure your local network, internet path, and DNS."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.status = QLabel("Ready")
        self.status.setObjectName("CardValue")

        layout.addWidget(self.status)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        self.details = QFrame()
        self.details.setObjectName("Card")

        details_layout = QVBoxLayout(self.details)
        details_layout.setContentsMargins(20, 20, 20, 20)

        self.details_label = QLabel(
            "Press Run Diagnostic to begin."
        )
        self.details_label.setWordWrap(True)

        details_layout.addWidget(self.details_label)

        layout.addWidget(self.details)

        buttons = QHBoxLayout()

        self.run_button = QPushButton("Run Diagnostic")
        self.run_button.clicked.connect(self.start)

        buttons.addWidget(self.run_button)
        buttons.addStretch()

        layout.addLayout(buttons)
        layout.addStretch()

    def start(self):
        if self.thread is not None:
            return

        self.run_button.setEnabled(False)
        self.status.setText("Starting diagnostic...")
        self.details_label.setText(
            "Collecting network evidence..."
        )

        self.current_progress = 0
        self.progress.setValue(0)

        self.thread = QThread()
        self.worker = DiagnosticWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.progress.connect(
            self.update_progress
        )

        self.worker.finished.connect(
            self.on_finished
        )

        self.worker.failed.connect(
            self.on_failed
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.failed.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.cleanup_thread
        )

        self.thread.start()

    @Slot(str, str)
    def update_progress(self, step, message):
        values = {
            "setup": 10,
            "router": 35,
            "internet": 60,
            "dns": 80,
            "analysis": 95,
            "complete": 100,
        }

        new_progress = values.get(
            step,
            self.current_progress,
        )

        self.current_progress = max(
            self.current_progress,
            new_progress,
        )

        self.progress.setValue(
            self.current_progress
        )

        self.status.setText(message)

    @Slot(object)
    def on_finished(self, result):
        self.current_progress = 100
        self.progress.setValue(100)

        self.status.setText(
            "Diagnostic complete"
        )

        self.details_label.setText(
            result.recommendation.title
        )

        self.finished.emit(result)

    @Slot(str)
    def on_failed(self, message):
        self.status.setText(
            "Diagnostic failed"
        )

        self.details_label.setText(
            message
        )

    @Slot()
    def cleanup_thread(self):
        thread = self.thread

        self.thread = None
        self.worker = None

        if thread is not None:
            thread.deleteLater()

        self.run_button.setEnabled(True)

    def closeEvent(self, event):
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait()

        event.accept()