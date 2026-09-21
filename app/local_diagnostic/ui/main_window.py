from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.local_diagnostic.ui.dashboard import DashboardPage
from app.local_diagnostic.ui.diagnostic_page import DiagnosticPage
from app.local_diagnostic.ui.evidence_page import EvidencePage
from app.local_diagnostic.ui.history_page import HistoryPage
from app.local_diagnostic.ui.monitor_page import MonitorPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WiFi Diagnostic")
        self.resize(1180, 760)
        self.setMinimumSize(1000, 680)

        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self.create_sidebar()
        root_layout.addWidget(sidebar)

        self.pages = QStackedWidget()

        self.dashboard = DashboardPage()
        self.diagnostic = DiagnosticPage()
        self.monitor = MonitorPage()
        self.history = HistoryPage()
        self.evidence = EvidencePage()

        self.pages.addWidget(self.dashboard)
        self.pages.addWidget(self.diagnostic)
        self.pages.addWidget(self.monitor)
        self.pages.addWidget(self.history)
        self.pages.addWidget(self.evidence)

        root_layout.addWidget(self.pages)

        self.setCentralWidget(root)

        self.dashboard.run_requested.connect(
            lambda: self.show_page(1)
        )

        self.diagnostic.finished.connect(
            self.handle_result
        )

        self.monitor.result_received.connect(
            self.handle_monitor_result
        )

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 25, 18, 20)
        layout.setSpacing(7)

        title = QLabel("WiFi Diagnostic")
        title.setObjectName("AppTitle")

        subtitle = QLabel("Home network health")
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(25)

        self.nav_buttons = []

        buttons = [
            ("Dashboard", 0),
            ("Diagnose", 1),
            ("Monitor", 2),
            ("History", 3),
            ("Evidence", 4),
        ]

        for text, index in buttons:
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setCheckable(True)

            button.clicked.connect(
                lambda checked=False, i=index: self.show_page(i)
            )

            layout.addWidget(button)
            self.nav_buttons.append(button)

        layout.addStretch()

        version = QLabel("Local diagnostic")
        version.setObjectName("PageSubtitle")

        layout.addWidget(version)

        self.nav_buttons[0].setChecked(True)

        return sidebar

    def show_page(self, index):
        self.pages.setCurrentIndex(index)

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)

    def handle_result(self, result):
        self.dashboard.update_result(result)
        self.evidence.update_result(result)
        self.history.add_result(result)

        self.show_page(0)

    def handle_monitor_result(self, monitor_run):
        result = monitor_run.result

        self.dashboard.update_result(result)
        self.evidence.update_result(result)
        self.history.add_result(result)