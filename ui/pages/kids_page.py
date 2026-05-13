"""Kids Page - Kids content."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class KidsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("👶 Kids Content")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
