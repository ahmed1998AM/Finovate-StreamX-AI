"""Sports Page - Live sports channels."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SportsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("⚽ Sports Channels")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
