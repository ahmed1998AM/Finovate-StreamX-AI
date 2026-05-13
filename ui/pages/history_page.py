"""History Page - Watch history."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("🕐 Watch History")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
