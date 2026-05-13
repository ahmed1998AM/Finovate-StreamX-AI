"""Movies Page - VOD movies library."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MoviesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("🎬 Movies Library")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
