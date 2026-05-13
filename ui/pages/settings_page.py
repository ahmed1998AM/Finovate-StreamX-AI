"""
Settings Page Module
=====================
Application settings and configuration.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QTabWidget, QCheckBox, QSpinBox,
    QLineEdit, QPushButton, QComboBox, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SettingsPage(QWidget):
    """Settings page with all configuration options."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the Settings page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        title = QLabel("⚙️ Settings")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        # Tab widget for settings categories
        tabs = QTabWidget()
        tabs.setObjectName("settingsTabs")
        
        # General settings tab
        tabs.addTab(self._create_general_tab(), "🏠 General")
        
        # IPTV settings tab
        tabs.addTab(self._create_iptv_tab(), "📺 IPTV")
        
        # Player settings tab
        tabs.addTab(self._create_player_tab(), "▶️ Player")
        
        # AI settings tab
        tabs.addTab(self._create_ai_tab(), "🤖 AI")
        
        # Security tab
        tabs.addTab(self._create_security_tab(), "🔒 Security")
        
        # Network tab
        tabs.addTab(self._create_network_tab(), "🌐 Network")
        
        main_layout.addWidget(tabs)
    
    def _create_general_tab(self) -> QWidget:
        """Create general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Language
        lang_group = QGroupBox("Language / اللغة")
        lang_layout = QVBoxLayout(lang_group)
        
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Arabic / العربية"])
        lang_layout.addWidget(lang_combo)
        layout.addWidget(lang_group)
        
        # Theme
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout(theme_group)
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark Neon", "Light", "Cyberpunk", "Plex Style", "Netflix Style"])
        theme_layout.addWidget(theme_combo)
        layout.addWidget(theme_group)
        
        # Performance
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout(perf_group)
        
        gpu_check = QCheckBox("Enable GPU Acceleration")
        gpu_check.setChecked(True)
        perf_layout.addWidget(gpu_check)
        
        anim_check = QCheckBox("Enable Animations")
        anim_check.setChecked(True)
        perf_layout.addWidget(anim_check)
        
        cache_check = QCheckBox("Enable Cache")
        cache_check.setChecked(True)
        perf_layout.addWidget(cache_check)
        
        layout.addWidget(perf_group)
        
        layout.addStretch()
        
        # Save button
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setObjectName("primaryButton")
        layout.addWidget(save_btn)
        
        return widget
    
    def _create_iptv_tab(self) -> QWidget:
        """Create IPTV settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Playlist management
        playlist_group = QGroupBox("Playlist Management")
        playlist_layout = QVBoxLayout(playlist_group)
        
        m3u_input = QLineEdit()
        m3u_input.setPlaceholderText("Enter M3U/M3U8 URL or file path")
        playlist_layout.addWidget(m3u_input)
        
        import_btn = QPushButton("📥 Import Playlist")
        import_btn.setObjectName("primaryButton")
        playlist_layout.addWidget(import_btn)
        
        refresh_check = QCheckBox("Auto-refresh playlists")
        playlist_layout.addWidget(refresh_check)
        
        layout.addWidget(playlist_group)
        
        # EPG settings
        epg_group = QGroupBox("EPG Settings")
        epg_layout = QVBoxLayout(epg_group)
        
        epg_url = QLineEdit()
        epg_url.setPlaceholderText("EPG XMLTV URL")
        epg_layout.addWidget(epg_url)
        
        epg_refresh = QCheckBox("Auto-update EPG")
        epg_layout.addWidget(epg_refresh)
        
        layout.addWidget(epg_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_player_tab(self) -> QWidget:
        """Create player settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Player selection
        player_group = QGroupBox("Video Player")
        player_layout = QVBoxLayout(player_group)
        
        player_combo = QComboBox()
        player_combo.addItems(["VLC", "MPV"])
        player_layout.addWidget(player_combo)
        
        layout.addWidget(player_group)
        
        # Hardware acceleration
        hw_group = QGroupBox("Hardware Acceleration")
        hw_layout = QVBoxLayout(hw_group)
        
        cuda_check = QCheckBox("CUDA (NVIDIA)")
        hw_layout.addWidget(cuda_check)
        
        dxva_check = QCheckBox("DXVA2 (Windows)")
        hw_layout.addWidget(dxva_check)
        
        vulkan_check = QCheckBox("Vulkan")
        hw_layout.addWidget(vulkan_check)
        
        layout.addWidget(hw_group)
        
        # Playback options
        playback_group = QGroupBox("Playback Options")
        playback_layout = QVBoxLayout(playback_group)
        
        low_latency = QCheckBox("Low Latency Mode")
        playback_layout.addWidget(low_latency)
        
        volume_norm = QCheckBox("Volume Normalization")
        playback_layout.addWidget(volume_norm)
        
        layout.addWidget(playback_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_ai_tab(self) -> QWidget:
        """Create AI settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Provider selection
        provider_group = QGroupBox("AI Provider")
        provider_layout = QVBoxLayout(provider_group)
        
        provider_combo = QComboBox()
        provider_combo.addItems([
            "OpenAI", "Gemini", "Claude", "DeepSeek",
            "Grok", "OpenRouter", "Ollama", "LM Studio"
        ])
        provider_layout.addWidget(provider_combo)
        
        api_key_input = QLineEdit()
        api_key_input.setPlaceholderText("Enter API Key")
        api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        provider_layout.addWidget(api_key_input)
        
        layout.addWidget(provider_group)
        
        # AI features
        features_group = QGroupBox("AI Features")
        features_layout = QVBoxLayout(features_group)
        
        chat_check = QCheckBox("Enable AI Chat")
        features_layout.addWidget(chat_check)
        
        voice_check = QCheckBox("Enable Voice Commands")
        features_layout.addWidget(voice_check)
        
        subtitle_check = QCheckBox("Auto Subtitle Generation")
        features_layout.addWidget(subtitle_check)
        
        recommend_check = QCheckBox("Smart Recommendations")
        features_layout.addWidget(recommend_check)
        
        layout.addWidget(features_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_security_tab(self) -> QWidget:
        """Create security settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # PIN lock
        pin_group = QGroupBox("PIN Lock")
        pin_layout = QVBoxLayout(pin_group)
        
        pin_check = QCheckBox("Enable PIN Lock")
        pin_layout.addWidget(pin_check)
        
        pin_input = QLineEdit()
        pin_input.setPlaceholderText("Enter 4-digit PIN")
        pin_input.setMaxLength(4)
        pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        pin_layout.addWidget(pin_input)
        
        layout.addWidget(pin_group)
        
        # Parental control
        parental_group = QGroupBox("Parental Control")
        parental_layout = QVBoxLayout(parental_group)
        
        adult_lock = QCheckBox("Lock Adult Content (18+)")
        adult_lock.setChecked(True)
        parental_layout.addWidget(adult_lock)
        
        kids_mode = QCheckBox("Kids Mode")
        parental_layout.addWidget(kids_mode)
        
        layout.addWidget(parental_group)
        
        # Encryption
        encrypt_group = QGroupBox("Encryption")
        encrypt_layout = QVBoxLayout(encrypt_group)
        
        encrypt_settings = QCheckBox("Encrypt Settings")
        encrypt_layout.addWidget(encrypt_settings)
        
        encrypt_keys = QCheckBox("Encrypt API Keys")
        encrypt_layout.addWidget(encrypt_keys)
        
        layout.addWidget(encrypt_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_network_tab(self) -> QWidget:
        """Create network settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Connection settings
        conn_group = QGroupBox("Connection")
        conn_layout = QVBoxLayout(conn_group)
        
        timeout_spin = QSpinBox()
        timeout_spin.setRange(5, 120)
        timeout_spin.setValue(30)
        timeout_spin.setSuffix(" seconds")
        conn_layout.addWidget(QLabel("Request Timeout:"))
        conn_layout.addWidget(timeout_spin)
        
        concurrent_spin = QSpinBox()
        concurrent_spin.setRange(1, 50)
        concurrent_spin.setValue(10)
        conn_layout.addWidget(QLabel("Max Concurrent Requests:"))
        conn_layout.addWidget(concurrent_spin)
        
        layout.addWidget(conn_group)
        
        # Cloud sync
        cloud_group = QGroupBox("Cloud Sync")
        cloud_layout = QVBoxLayout(cloud_group)
        
        cloud_combo = QComboBox()
        cloud_combo.addItems([
            "Supabase", "Firebase", "Google Drive", 
            "Dropbox", "OneDrive", "Disabled"
        ])
        cloud_layout.addWidget(cloud_combo)
        
        sync_check = QCheckBox("Enable Cloud Sync")
        cloud_layout.addWidget(sync_check)
        
        backup_check = QCheckBox("Auto Backup Settings")
        cloud_layout.addWidget(backup_check)
        
        layout.addWidget(cloud_group)
        
        layout.addStretch()
        
        return widget
