"""
Live TV Page Module
====================
Live television channels with EPG support.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QSplitter, QListWidget, QListWidgetItem,
    QLineEdit, QComboBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class LiveTVPage(QWidget):
    """Live TV page with channel list and player."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the Live TV page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Top controls
        controls = self._create_controls()
        main_layout.addWidget(controls)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Channel list
        channel_list = self._create_channel_list()
        splitter.addWidget(channel_list)
        
        # Player area
        player_area = self._create_player_area()
        splitter.addWidget(player_area)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
    
    def _create_controls(self) -> QFrame:
        """Create top control bar."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        frame.setFixedHeight(60)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Search box
        search = QLineEdit()
        search.setPlaceholderText("🔍 Search channels...")
        search.setObjectName("searchBox")
        search.setFixedWidth(300)
        layout.addWidget(search)
        
        # Category filter
        category_combo = QComboBox()
        category_combo.addItems([
            "All Categories", "Sports", "Movies", "Series", 
            "News", "Kids", "Documentary", "Music", "Entertainment"
        ])
        layout.addWidget(category_combo)
        
        # Country filter
        country_combo = QComboBox()
        country_combo.addItems([
            "All Countries", "Egypt", "Saudi Arabia", "UAE", 
            "USA", "UK", "France", "Germany", "Italy"
        ])
        layout.addWidget(country_combo)
        
        layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("accentButton")
        layout.addWidget(refresh_btn)
        
        return frame
    
    def _create_channel_list(self) -> QGroupBox:
        """Create channel list panel."""
        group = QGroupBox("📺 Channels")
        group.setObjectName("channelListGroup")
        
        layout = QVBoxLayout(group)
        
        # Channel list widget
        self.channel_list_widget = QListWidget()
        self.channel_list_widget.setObjectName("channelList")
        
        # Add sample channels
        channels = [
            ("🏆 Sports Premium 1", "HD"),
            ("🎬 Movies HD", "FHD"),
            ("📰 News 24/7", "HD"),
            ("👶 Kids Channel", "HD"),
            ("🎵 Music TV", "SD"),
            ("🎭 Entertainment Plus", "FHD"),
            ("📺 Drama Series", "HD"),
            ("🌍 Documentary World", "FHD"),
        ]
        
        for channel_name, quality in channels:
            item = QListWidgetItem(f"{channel_name} [{quality}]")
            item.setFont(QFont("Segoe UI", 11))
            self.channel_list_widget.addItem(item)
        
        layout.addWidget(self.channel_list_widget)
        
        return group
    
    def _create_player_area(self) -> QGroupBox:
        """Create video player area."""
        group = QGroupBox("▶️ Player")
        group.setObjectName("playerGroup")
        
        layout = QVBoxLayout(group)
        
        # Video placeholder
        video_placeholder = QFrame()
        video_placeholder.setObjectName("videoPlaceholder")
        video_placeholder.setMinimumSize(640, 360)
        video_placeholder.setStyleSheet("""
            QFrame#videoPlaceholder {
                background-color: #000000;
                border: 2px solid #1E88E5;
                border-radius: 10px;
            }
        """)
        
        placeholder_layout = QVBoxLayout(video_placeholder)
        placeholder_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        placeholder_label = QLabel("🎬 Select a channel to start playing")
        placeholder_label.setObjectName("subtitleLabel")
        placeholder_label.setFont(QFont("Segoe UI", 16))
        placeholder_layout.addWidget(placeholder_label)
        
        layout.addWidget(video_placeholder)
        
        # Player controls
        controls_frame = self._create_player_controls()
        layout.addWidget(controls_frame)
        
        # EPG info
        epg_frame = self._create_epg_info()
        layout.addWidget(epg_frame)
        
        return group
    
    def _create_player_controls(self) -> QFrame:
        """Create player control buttons."""
        frame = QFrame()
        frame.setFixedHeight(50)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 5, 0, 5)
        
        # Playback controls
        play_btn = QPushButton("▶️ Play")
        play_btn.setObjectName("primaryButton")
        layout.addWidget(play_btn)
        
        pause_btn = QPushButton("⏸️ Pause")
        layout.addWidget(pause_btn)
        
        stop_btn = QPushButton("⏹️ Stop")
        layout.addWidget(stop_btn)
        
        layout.addStretch()
        
        # Volume
        volume_label = QLabel("🔊")
        layout.addWidget(volume_label)
        
        # Fullscreen
        fullscreen_btn = QPushButton("⛶ Fullscreen")
        fullscreen_btn.setObjectName("accentButton")
        layout.addWidget(fullscreen_btn)
        
        return frame
    
    def _create_epg_info(self) -> QFrame:
        """Create EPG information display."""
        frame = QFrame()
        frame.setObjectName("epgFrame")
        frame.setFixedHeight(100)
        
        layout = QVBoxLayout(frame)
        
        title = QLabel("📋 Now Playing")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        info_label = QLabel("No channel selected")
        info_label.setObjectName("secondaryLabel")
        layout.addWidget(info_label)
        
        progress_label = QLabel("Progress: --:-- / --:--")
        progress_label.setObjectName("secondaryLabel")
        layout.addWidget(progress_label)
        
        return frame
