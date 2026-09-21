import sys

from PySide6.QtWidgets import QApplication

from app.local_diagnostic.ui.main_window import MainWindow
from app.local_diagnostic.ui.styles import application_stylesheet


class WiFiDiagnosticGUI:
    """
    Compatibility wrapper for the existing test suite.

    The actual desktop interface is implemented by MainWindow.
    """

    def __init__(self, root=None):
        self.app = QApplication.instance()

        if self.app is None:
            self.app = QApplication(sys.argv)

        self.app.setStyleSheet(
            application_stylesheet()
        )

        self.window = MainWindow()

    def show(self):
        self.window.show()


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(
        application_stylesheet()
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()