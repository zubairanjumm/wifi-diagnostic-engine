BACKGROUND = "#f6f7f9"
SURFACE = "#ffffff"
TEXT = "#111318"
SECONDARY = "#686d78"
BORDER = "#e4e6eb"
SUCCESS = "#16803c"
WARNING = "#a15c00"
DANGER = "#c62828"
ACCENT = "#111318"


def application_stylesheet() -> str:
    return f"""
    QWidget {{
        font-family: "Segoe UI";
        color: {TEXT};
    }}

    QMainWindow {{
        background: {BACKGROUND};
    }}

    QFrame#Sidebar {{
        background: {SURFACE};
        border-right: 1px solid {BORDER};
    }}

    QLabel#AppTitle {{
        font-size: 20px;
        font-weight: 700;
    }}

    QLabel#PageTitle {{
        font-size: 28px;
        font-weight: 700;
    }}

    QLabel#PageSubtitle {{
        font-size: 13px;
        color: {SECONDARY};
    }}

    QLabel#CardTitle {{
        font-size: 12px;
        color: {SECONDARY};
    }}

    QLabel#CardValue {{
        font-size: 24px;
        font-weight: 700;
    }}

    QLabel#Status {{
        font-size: 13px;
        font-weight: 600;
    }}

    QFrame#Card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}

    QPushButton {{
        background: {ACCENT};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background: #2b2e34;
    }}

    QPushButton:disabled {{
        background: #b9bcc3;
    }}

    QPushButton#SecondaryButton {{
        background: {SURFACE};
        color: {TEXT};
        border: 1px solid {BORDER};
    }}

    QPushButton#SecondaryButton:hover {{
        background: #f0f1f3;
    }}

    QPushButton#NavButton {{
        background: transparent;
        color: {SECONDARY};
        text-align: left;
        padding: 11px 14px;
        border-radius: 7px;
        font-weight: 500;
    }}

    QPushButton#NavButton:hover {{
        background: #f0f1f3;
        color: {TEXT};
    }}

    QPushButton#NavButton:checked {{
        background: #111318;
        color: white;
    }}

    QProgressBar {{
        background: #e9ebef;
        border: none;
        border-radius: 4px;
        height: 8px;
        text-align: center;
    }}

    QProgressBar::chunk {{
        background: #111318;
        border-radius: 4px;
    }}

    QScrollArea {{
        border: none;
        background: transparent;
    }}

    QListWidget {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 6px;
    }}

    QListWidget::item {{
        padding: 12px;
        border-radius: 7px;
    }}

    QListWidget::item:selected {{
        background: #f0f1f3;
        color: {TEXT};
    }}
    """