from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StatusCard(QFrame):
    def __init__(self, title: str):
        super().__init__()

        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

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
            "A simple view of what we found on your connection."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -----------------------------------------------------
        # Main status
        # -----------------------------------------------------

        health_card = QFrame()
        health_card.setObjectName("Card")

        health_layout = QVBoxLayout(health_card)
        health_layout.setContentsMargins(24, 22, 24, 22)
        health_layout.setSpacing(8)

        health_title = QLabel("Current status")
        health_title.setObjectName("CardTitle")

        self.health_status = QLabel("No diagnostic yet")
        self.health_status.setObjectName("PageTitle")

        self.health_message = QLabel(
            "Run a diagnostic to check your connection."
        )
        self.health_message.setObjectName("PageSubtitle")
        self.health_message.setWordWrap(True)

        health_layout.addWidget(health_title)
        health_layout.addWidget(self.health_status)
        health_layout.addWidget(self.health_message)

        layout.addWidget(health_card)

        # -----------------------------------------------------
        # Simple status cards
        # -----------------------------------------------------

        grid = QGridLayout()
        grid.setSpacing(14)

        self.wifi_card = StatusCard("Wi-Fi")
        self.internet_card = StatusCard("Internet")
        self.websites_card = StatusCard("Websites")
        self.consistency_card = StatusCard("Connection")

        grid.addWidget(self.wifi_card, 0, 0)
        grid.addWidget(self.internet_card, 0, 1)
        grid.addWidget(self.websites_card, 1, 0)
        grid.addWidget(self.consistency_card, 1, 1)

        layout.addLayout(grid)

        # -----------------------------------------------------
        # Diagnostic button
        # -----------------------------------------------------

        self.run_button = QPushButton("Run Diagnostic")
        self.run_button.clicked.connect(self.run_requested.emit)

        layout.addWidget(self.run_button)
        layout.addStretch()

    def update_result(self, result):
        diagnosis = result.diagnosis
        evidence = result.evidence

        diagnosis_titles = {
            "no_obvious_problem": "Connection looks healthy",
            "local_network_problem": "Problem reaching your router",
            "local_network_instability": "Local connection is unstable",
            "internet_connection_problem": "Internet connection is unavailable",
            "internet_path_instability": "Internet connection is unstable",
            "dns_problem": "Website name lookup is failing",
            "high_latency": "Connection is responding slowly",
            "high_jitter": "Connection is inconsistent",
            "browser_connection_instability": "Some connection requests are failing",
        }

        self.health_status.setText(
            diagnosis_titles.get(
                diagnosis,
                "Unusual connection condition",
            )
        )

        self.health_message.setText(
            result.finding.summary
        )

        # -----------------------------------------------------
        # Wi-Fi
        # -----------------------------------------------------

        if evidence.wifi_connected is True:
            self.wifi_card.value.setText("Connected")
            self.wifi_card.detail.setText("Your device is connected to Wi-Fi.")
        elif evidence.wifi_connected is False:
            self.wifi_card.value.setText("Not connected")
            self.wifi_card.detail.setText("Your device is not connected to Wi-Fi.")
        else:
            self.wifi_card.value.setText("Unknown")
            self.wifi_card.detail.setText("Wi-Fi status could not be checked.")

        # -----------------------------------------------------
        # Internet
        # -----------------------------------------------------

        if evidence.internet_reachable is True:
            self.internet_card.value.setText("Available")
            self.internet_card.detail.setText(
                "Your device can reach the internet."
            )
        elif evidence.internet_reachable is False:
            self.internet_card.value.setText("Unavailable")
            self.internet_card.detail.setText(
                "Your device could not reach the internet."
            )
        else:
            self.internet_card.value.setText("Unknown")
            self.internet_card.detail.setText(
                "Internet availability could not be confirmed."
            )

        # -----------------------------------------------------
        # Websites / DNS
        # -----------------------------------------------------

        if evidence.dns_working is True:
            self.websites_card.value.setText("Working")
            self.websites_card.detail.setText(
                "Website name lookup is working."
            )
        elif evidence.dns_working is False:
            self.websites_card.value.setText("Problem")
            self.websites_card.detail.setText(
                "Website name lookup is failing."
            )
        else:
            self.websites_card.value.setText("Unknown")
            self.websites_card.detail.setText(
                "Website lookup could not be confirmed."
            )

        # -----------------------------------------------------
        # Overall consistency
        # -----------------------------------------------------

        stable_diagnoses = {
            "no_obvious_problem",
        }

        if diagnosis in stable_diagnoses:
            self.consistency_card.value.setText("Consistent")
            self.consistency_card.detail.setText(
                "No repeated instability was detected."
            )
        else:
            self.consistency_card.value.setText("Needs attention")
            self.consistency_card.detail.setText(
                "The diagnostic found evidence worth investigating."
            )