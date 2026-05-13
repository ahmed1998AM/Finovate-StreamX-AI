"""
VLC Player Module
=================
Video player implementation using python-vlc with hardware acceleration.
"""

import vlc
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, Signal, Slot, QTimer
from typing import Optional, Dict, Any
from enum import Enum


class PlayerState(Enum):
    """Player state enumeration."""
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    BUFFERING = 3
    ERROR = 4
    ENDED = 5


class VLCPlayerWidget(QWidget):
    """VLC-based video player widget."""
    
    # Signals
    state_changed = Signal(PlayerState)
    position_changed = Signal(int)  # milliseconds
    duration_changed = Signal(int)  # milliseconds
    volume_changed = Signal(int)
    error_occurred = Signal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self._instance: Optional[vlc.Instance] = None
        self._player: Optional[vlc.MediaPlayer] = None
        self._media: Optional[vlc.Media] = None
        self._state = PlayerState.STOPPED
        
        # Setup UI
        self._setup_ui()
        
        # Initialize VLC
        self._initialize_vlc()
        
        # Position update timer
        self._position_timer = QTimer(self)
        self._position_timer.timeout.connect(self._update_position)
    
    def _setup_ui(self):
        """Setup user interface."""
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #000000;")
    
    def _initialize_vlc(self):
        """Initialize VLC instance with optimized settings."""
        # VLC arguments for optimization
        args = [
            '--no-video-title-show',
            '--quiet',
            '--network-caching=1000',
            '--live-caching=1000',
            '--file-caching=1000',
            '--clock-synchronization',
            '--sout-mux-caching=1000',
        ]
        
        # Hardware acceleration options
        args.extend([
            '--avcodec-hw=dxva2',  # Windows DirectX
            '--avcodec-hw=any',
        ])
        
        try:
            self._instance = vlc.Instance(args)
            self._player = self._instance.media_player_new()
            
            # Set player to our widget
            if hasattr(self.winId, '__call__'):
                self._player.set_hwnd(self.winId())
            else:
                self._player.set_hwnd(self.winId())
            
            # Setup event manager
            event_manager = self._player.event_manager()
            event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, self._on_playing)
            event_manager.event_attach(vlc.EventType.MediaPlayerPaused, self._on_paused)
            event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self._on_stopped)
            event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_ended)
            event_manager.event_attach(vlc.EventType.MediaPlayerError, self._on_error)
            event_manager.event_attach(vlc.EventType.MediaPlayerBuffering, self._on_buffering)
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize VLC: {str(e)}")
    
    def load_media(self, url: str, options: Optional[Dict[str, Any]] = None):
        """
        Load media from URL or file path.
        
        Args:
            url: Media URL or file path
            options: Optional media options
        """
        if not self._player:
            self.error_occurred.emit("Player not initialized")
            return
        
        try:
            self._media = self._instance.media_new(url)
            
            # Add custom options
            if options:
                for key, value in options.items():
                    self._media.add_option(f"--{key}={value}")
            
            self._player.set_media(self._media)
            self._state = PlayerState.BUFFERING
            self.state_changed.emit(self._state)
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to load media: {str(e)}")
    
    def play(self):
        """Start or resume playback."""
        if self._player:
            self._player.play()
            self._position_timer.start(500)  # Update every 500ms
    
    def pause(self):
        """Pause playback."""
        if self._player:
            self._player.pause()
    
    def stop(self):
        """Stop playback."""
        if self._player:
            self._player.stop()
            self._position_timer.stop()
            self._state = PlayerState.STOPPED
            self.state_changed.emit(self._state)
    
    def toggle_play_pause(self):
        """Toggle between play and pause."""
        if self._player and self._player.is_playing():
            self.pause()
        else:
            self.play()
    
    def set_volume(self, volume: int):
        """
        Set volume level.
        
        Args:
            volume: Volume level (0-100)
        """
        if self._player:
            volume = max(0, min(100, volume))
            self._player.audio_set_volume(volume)
            self.volume_changed.emit(volume)
    
    def get_volume(self) -> int:
        """Get current volume level."""
        if self._player:
            return self._player.audio_get_volume()
        return 0
    
    def set_position(self, position: float):
        """
        Set playback position.
        
        Args:
            position: Position as percentage (0.0-1.0)
        """
        if self._player:
            position = max(0.0, min(1.0, position))
            self._player.set_position(position)
    
    def get_position(self) -> float:
        """Get current playback position as percentage."""
        if self._player:
            return self._player.get_position()
        return 0.0
    
    def get_position_ms(self) -> int:
        """Get current playback position in milliseconds."""
        if self._player:
            return self._player.get_time()
        return 0
    
    def get_duration_ms(self) -> int:
        """Get media duration in milliseconds."""
        if self._player:
            return self._player.get_length()
        return 0
    
    def seek_forward(self, seconds: int = 10):
        """Seek forward by specified seconds."""
        if self._player:
            current = self.get_position_ms()
            self._player.set_time(current + (seconds * 1000))
    
    def seek_backward(self, seconds: int = 10):
        """Seek backward by specified seconds."""
        if self._player:
            current = self.get_position_ms()
            self._player.set_time(max(0, current - (seconds * 1000)))
    
    def set_playback_rate(self, rate: float):
        """
        Set playback speed.
        
        Args:
            rate: Playback rate (0.5-2.0)
        """
        if self._player:
            rate = max(0.5, min(2.0, rate))
            self._player.set_rate(rate)
    
    def take_snapshot(self, path: str):
        """
        Take a snapshot of current frame.
        
        Args:
            path: Path to save snapshot
        """
        if self._player:
            self._player.video_take_snapshot(0, path, 0, 0)
    
    def is_playing(self) -> bool:
        """Check if media is currently playing."""
        if self._player:
            return self._player.is_playing()
        return False
    
    def get_state(self) -> PlayerState:
        """Get current player state."""
        return self._state
    
    @Slot()
    def _update_position(self):
        """Update position and emit signals."""
        if self._player and self._state == PlayerState.PLAYING:
            position = self.get_position_ms()
            duration = self.get_duration_ms()
            
            if position > 0:
                self.position_changed.emit(position)
            
            if duration > 0:
                self.duration_changed.emit(duration)
    
    @Slot()
    def _on_playing(self, event):
        """Handle playing event."""
        self._state = PlayerState.PLAYING
        self.state_changed.emit(self._state)
    
    @Slot()
    def _on_paused(self, event):
        """Handle paused event."""
        self._state = PlayerState.PAUSED
        self.state_changed.emit(self._state)
    
    @Slot()
    def _on_stopped(self, event):
        """Handle stopped event."""
        self._state = PlayerState.STOPPED
        self.state_changed.emit(self._state)
    
    @Slot()
    def _on_ended(self, event):
        """Handle media ended event."""
        self._state = PlayerState.ENDED
        self.state_changed.emit(self._state)
        self._position_timer.stop()
    
    @Slot()
    def _on_buffering(self, event):
        """Handle buffering event."""
        self._state = PlayerState.BUFFERING
        self.state_changed.emit(self._state)
    
    @Slot()
    def _on_error(self, event):
        """Handle error event."""
        self._state = PlayerState.ERROR
        self.state_changed.emit(self._state)
        self.error_occurred.emit("Playback error occurred")
    
    def cleanup(self):
        """Cleanup player resources."""
        if self._position_timer:
            self._position_timer.stop()
        
        if self._player:
            self._player.stop()
            self._player.release()
        
        if self._instance:
            self._instance.release()
