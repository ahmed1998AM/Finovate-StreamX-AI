"""Search Page - Global search."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("🔍 Search")
        label.setObjectName("titleLabel")
        layout.addWidget(label)
        search = QLineEdit()
        search.setPlaceholderText("Search channels, movies, series...")
        search.setObjectName("searchBox")
        layout.addWidget(search)
