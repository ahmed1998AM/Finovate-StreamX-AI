"""Favorites Page - User favorites."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class FavoritesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("❤️ Favorites")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
