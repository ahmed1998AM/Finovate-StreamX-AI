"""Series Page - TV Series library."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SeriesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("📀 Series Library")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
