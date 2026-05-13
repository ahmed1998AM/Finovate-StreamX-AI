"""
Home Page Module
=================
Dashboard with quick access, recommendations, and continue watching.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame, QGridLayout, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class HomePage(QWidget):
    """Home dashboard page."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the home page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Welcome section
        welcome_frame = self._create_welcome_section()
        main_layout.addWidget(welcome_frame)
        
        # Continue watching section
        continue_watching = self._create_continue_watching()
        main_layout.addWidget(continue_watching)
        
        # Quick categories
        categories = self._create_quick_categories()
        main_layout.addWidget(categories)
        
        # Recommendations
        recommendations = self._create_recommendations()
        main_layout.addWidget(recommendations)
        
        # Add stretch to push content up
        main_layout.addStretch()
    
    def _create_welcome_section(self) -> QFrame:
        """Create welcome banner section."""
        frame = QFrame()
        frame.setObjectName("accentFrame")
        frame.setFixedHeight(150)
        
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("🎯 Welcome to Finovate StreamX AI")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        layout.addWidget(title)
        
        subtitle = QLabel("Your Ultimate AI-Powered IPTV & Media Center")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setFont(QFont("Segoe UI", 14))
        layout.addWidget(subtitle)
        
        return frame
    
    def _create_continue_watching(self) -> QFrame:
        """Create continue watching section."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        
        layout = QVBoxLayout(frame)
        
        section_title = QLabel("🕐 Continue Watching")
        section_title.setObjectName("titleLabel")
        section_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(section_title)
        
        # Grid for thumbnails
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Placeholder thumbnails
        for i in range(6):
            thumb = self._create_thumbnail_card(f"Channel {i+1}", f"Episode {i+1}")
            row = i // 3
            col = i % 3
            grid.addWidget(thumb, row, col)
        
        layout.addLayout(grid)
        
        return frame
    
    def _create_quick_categories(self) -> QFrame:
        """Create quick access categories."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        
        layout = QVBoxLayout(frame)
        
        section_title = QLabel("📂 Quick Categories")
        section_title.setObjectName("titleLabel")
        section_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(section_title)
        
        # Category buttons
        cat_layout = QHBoxLayout()
        cat_layout.setSpacing(10)
        
        categories = [
            ("📺 Live TV", "live_tv"),
            ("🎬 Movies", "movies"),
            ("📀 Series", "series"),
            ("⚽ Sports", "sports"),
            ("👶 Kids", "kids"),
            ("❤️ Favorites", "favorites"),
        ]
        
        for cat_name, cat_id in categories:
            btn = QPushButton(cat_name)
            btn.setObjectName("primaryButton")
            btn.setFixedHeight(60)
            btn.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(btn)
            cat_layout.addWidget(btn)
        
        layout.addLayout(cat_layout)
        
        return frame
    
    def _create_recommendations(self) -> QFrame:
        """Create AI recommendations section."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        
        layout = QVBoxLayout(frame)
        
        section_title = QLabel("🤖 AI Recommendations")
        section_title.setObjectName("titleLabel")
        section_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(section_title)
        
        # Recommendation cards
        rec_layout = QHBoxLayout()
        rec_layout.setSpacing(15)
        
        for i in range(4):
            card = self._create_recommendation_card(f"Recommendation {i+1}")
            rec_layout.addWidget(card)
        
        layout.addLayout(rec_layout)
        
        return frame
    
    def _create_thumbnail_card(self, title: str, subtitle: str) -> QFrame:
        """Create a thumbnail card widget."""
        card = QFrame()
        card.setObjectName("cardWidget")
        card.setFixedSize(200, 140)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        sub_label = QLabel(subtitle)
        sub_label.setObjectName("secondaryLabel")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_label)
        
        return card
    
    def _create_recommendation_card(self, title: str) -> QFrame:
        """Create a recommendation card widget."""
        card = QFrame()
        card.setObjectName("cardWidget")
        card.setFixedSize(220, 160)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        return card
