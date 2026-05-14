"""
Finovate StreamX AI - Enhanced VLC Integration Module
Complete VLC Player Integration with UI, DVR, and EPG
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
Contact: 01225155329 | gogom8870@gmail.com
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging
import json

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSlider, QFrame, QGroupBox,
    QProgressBar, QSpinBox, QComboBox, QMessageBox,
    QFileDialog, QApplication
)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QPalette, QColor

# Import VLC Player
try:
    import vlc
    VLC_AVAILABLE = True
except ImportError:
    VLC_AVAILABLE = False
    print("⚠️ Warning: python-vlc not installed. Install with: pip install python-vlc")

logger = logging.getLogger(__name__)


class EnhancedVLCPlayerWidget(QWidget):
    """Enhanced VLC Player with full UI controls and DVR integration"""
    
    # Signals
    playback_started = Signal(str)
    playback_paused = Signal()
    playback_stopped = Signal()
    playback_ended = Signal()
    recording_started = Signal(str)
    recording_stopped = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self._instance: Optional[vlc.Instance] = None
        self._player: Optional[vlc.MediaPlayer] = None
        self._media: Optional[vlc.Media] = None
        self._is_playing = False
        self._is_paused = False
        self._current_channel = None
        self._current_url = None
        
        # DVR Integration
        self.dvr_manager = None
        self.active_recording = None
        
        # Setup UI
        self._setup_ui()
        
        # Initialize VLC if available
        if VLC_AVAILABLE:
            self._initialize_vlc()
        else:
            self._show_vlc_warning()
        
        # Update timer
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_ui)
        self._update_timer.setInterval(500)
    
    def _setup_ui(self):
        """Setup complete player UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Video display area
        self.video_widget = QWidget()
        self.video_widget.setObjectName("videoDisplay")
        self.video_widget.setStyleSheet("""
            QWidget#videoDisplay {
                background-color: #000000;
                border: none;
            }
        """)
        video_layout = QVBoxLayout(self.video_widget)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder label
        self.placeholder_label = QLabel("📺 Ready to Play")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        video_layout.addWidget(self.placeholder_label)
        
        main_layout.addWidget(self.video_widget, 1)
        
        # Control panel
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Set minimum height
        self.setMinimumHeight(400)
    
    def _create_control_panel(self) -> QFrame:
        """Create comprehensive control panel"""
        panel = QFrame()
        panel.setObjectName("controlPanel")
        panel.setStyleSheet("""
            QFrame#controlPanel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 136, 229, 0.9),
                    stop:1 rgba(11, 16, 32, 0.95));
                border-top: 2px solid #00E5FF;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #1E88E5);
                border-radius: 3px;
            }
        """)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("")
        layout.addWidget(self.progress_bar)
        
        # Main controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # Play/Pause button
        self.play_pause_btn = QPushButton("▶ Play")
        self.play_pause_btn.setObjectName("playButton")
        self.play_pause_btn.setFixedSize(80, 40)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.play_pause_btn.setStyleSheet("""
            QPushButton#playButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #1E88E5);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#playButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00FFFF, stop:1 #42A5F5);
            }
            QPushButton#playButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00B8D4, stop:1 #1565C0);
            }
        """)
        controls_layout.addWidget(self.play_pause_btn)
        
        # Stop button
        stop_btn = QPushButton("⏹ Stop")
        stop_btn.setObjectName("stopButton")
        stop_btn.setFixedSize(80, 40)
        stop_btn.clicked.connect(self.stop_playback)
        stop_btn.setStyleSheet("""
            QPushButton#stopButton {
                background-color: #FF5252;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#stopButton:hover {
                background-color: #FF1744;
            }
        """)
        controls_layout.addWidget(stop_btn)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊")
        volume_label.setStyleSheet("color: white; font-size: 16px;")
        controls_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(150)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(255, 255, 255, 0.2);
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #00E5FF;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #1E88E5);
                border-radius: 3px;
            }
        """)
        controls_layout.addWidget(self.volume_slider)
        
        self.volume_value_label = QLabel("80%")
        self.volume_value_label.setStyleSheet("color: white; font-weight: bold;")
        controls_layout.addWidget(self.volume_value_label)
        
        controls_layout.addStretch()
        
        # Record button
        self.record_btn = QPushButton("⏺ Record")
        self.record_btn.setObjectName("recordButton")
        self.record_btn.setFixedSize(100, 40)
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setStyleSheet("""
            QPushButton#recordButton {
                background-color: #FF5252;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#recordButton:hover {
                background-color: #FF1744;
            }
            QPushButton#recordButton:checked {
                background-color: #00E676;
                animation: pulse 1s infinite;
            }
        """)
        controls_layout.addWidget(self.record_btn)
        
        # Channel info
        self.channel_info_label = QLabel("No channel selected")
        self.channel_info_label.setStyleSheet("""
            QLabel {
                color: #B0BEC5;
                font-size: 12px;
                padding: 5px;
            }
        """)
        controls_layout.addWidget(self.channel_info_label)
        
        controls_layout.addStretch()
        
        # Fullscreen button
        fullscreen_btn = QPushButton("⛶ Fullscreen")
        fullscreen_btn.setObjectName("fullscreenButton")
        fullscreen_btn.setFixedSize(100, 40)
        fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        fullscreen_btn.setStyleSheet("""
            QPushButton#fullscreenButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#fullscreenButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        controls_layout.addWidget(fullscreen_btn)
        
        layout.addLayout(controls_layout)
        
        return panel
    
    def _initialize_vlc(self):
        """Initialize VLC instance with hardware acceleration"""
        try:
            args = [
                '--no-video-title-show',
                '--quiet',
                '--network-caching=3000',
                '--live-caching=3000',
                '--file-caching=3000',
                '--clock-synchronization',
                '--sout-mux-caching=3000',
                '--avcodec-hw=any',  # Hardware acceleration
                '--ffmpeg-hw=any',
            ]
            
            self._instance = vlc.Instance(args)
            self._player = self._instance.media_player_new()
            
            # Set player to our widget
            if sys.platform == 'win32':
                self._player.set_hwnd(self.video_widget.winId())
            elif sys.platform == 'darwin':
                self._player.set_nsobject(int(self.video_widget.winId()))
            else:
                self._player.set_xwindow(self.video_widget.winId())
            
            logger.info("VLC initialized successfully with hardware acceleration")
            
        except Exception as e:
            logger.error(f"Failed to initialize VLC: {e}")
            self.error_occurred.emit(f"VLC initialization failed: {str(e)}")
    
    def _show_vlc_warning(self):
        """Show warning when VLC is not available"""
        self.placeholder_label.setText("⚠️ VLC Not Installed\nInstall: pip install python-vlc")
        self.placeholder_label.setStyleSheet("""
            QLabel {
                color: #FF5252;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
            }
        """)
    
    def load_channel(self, channel_name: str, channel_url: str, metadata: Dict = None):
        """Load a TV channel for playback"""
        if not VLC_AVAILABLE or not self._player:
            QMessageBox.warning(self, "VLC Not Available", 
                              "Please install python-vlc: pip install python-vlc")
            return
        
        try:
            self._current_channel = channel_name
            self._current_url = channel_url
            
            self._media = self._instance.media_new(channel_url)
            
            # Add streaming options
            self._media.add_option('--network-caching=3000')
            self._media.add_option('--live-caching=3000')
            
            self._player.set_media(self._media)
            
            # Update UI
            self.channel_info_label.setText(f"📺 {channel_name}")
            self.placeholder_label.hide()
            
            logger.info(f"Loaded channel: {channel_name}")
            
        except Exception as e:
            logger.error(f"Failed to load channel: {e}")
            self.error_occurred.emit(f"Failed to load channel: {str(e)}")
    
    def play(self):
        """Start playback"""
        if self._player:
            self._player.play()
            self._is_playing = True
            self._is_paused = False
            self._update_timer.start()
            self.play_pause_btn.setText("⏸ Pause")
            self.playback_started.emit(self._current_channel or "Unknown")
            logger.info(f"Playing: {self._current_channel}")
    
    def pause(self):
        """Pause playback"""
        if self._player:
            self._player.pause()
            self._is_paused = True
            self.play_pause_btn.setText("▶ Resume")
            self.playback_paused.emit()
            logger.info("Playback paused")
    
    def stop_playback(self):
        """Stop playback"""
        if self._player:
            self._player.stop()
            self._is_playing = False
            self._is_paused = False
            self._update_timer.stop()
            self.play_pause_btn.setText("▶ Play")
            self.progress_bar.setValue(0)
            self.placeholder_label.show()
            self.playback_stopped.emit()
            logger.info("Playback stopped")
    
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if self._is_playing and not self._is_paused:
            self.pause()
        else:
            self.play()
    
    def set_volume(self, volume: int):
        """Set volume level"""
        if self._player:
            self._player.audio_set_volume(volume)
            self.volume_value_label.setText(f"{volume}%")
    
    def toggle_recording(self):
        """Toggle DVR recording"""
        if self.active_recording:
            # Stop recording
            if self.dvr_manager and self.active_recording:
                self.dvr_manager.stop_recording(self.active_recording.id)
                self.active_recording = None
                self.record_btn.setText("⏺ Record")
                self.record_btn.setChecked(False)
                self.recording_stopped.emit(self._current_channel)
                logger.info(f"Stopped recording: {self._current_channel}")
        else:
            # Start recording
            if self.dvr_manager and self._current_channel and self._current_url:
                self.active_recording = self.dvr_manager.start_live_recording(
                    channel_name=self._current_channel,
                    channel_url=self._current_url,
                    duration_minutes=120
                )
                self.record_btn.setText("⏹ Stop Rec")
                self.record_btn.setChecked(True)
                self.recording_started.emit(self._current_channel)
                logger.info(f"Started recording: {self._current_channel}")
            else:
                QMessageBox.warning(self, "DVR Not Available",
                                  "DVR Manager not initialized")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    @Slot()
    def _update_ui(self):
        """Update UI elements"""
        if self._player and self._is_playing:
            # Update progress
            duration = self._player.get_length()
            position = self._player.get_time()
            
            if duration > 0:
                progress = int((position / duration) * 100)
                self.progress_bar.setValue(progress)
    
    def set_dvr_manager(self, dvr_manager):
        """Set DVR manager for recording functionality"""
        self.dvr_manager = dvr_manager
        logger.info("DVR Manager connected to player")
    
    def cleanup(self):
        """Cleanup player resources"""
        if self._update_timer:
            self._update_timer.stop()
        
        if self._player:
            self._player.stop()
            self._player.release()
        
        if self._instance:
            self._instance.release()
        
        logger.info("Player cleaned up")


# Test function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    player = EnhancedVLCPlayerWidget()
    player.setWindowTitle("Enhanced VLC Player Test")
    player.resize(800, 600)
    player.show()
    
    # Test loading a channel
    test_channel = {
        "name": "Test Channel",
        "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    }
    player.load_channel(test_channel["name"], test_channel["url"])
    
    sys.exit(app.exec())
