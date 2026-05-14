"""
Finovate StreamX AI - Complete Integration Module
Bridges UI, Player, DVR, and IPTV Parser for seamless operation
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
Contact: 01225155329 | gogom8870@gmail.com
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging
import asyncio

from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import QObject, Signal, Slot, QTimer

# Import modules
from player.enhanced_player import EnhancedVLCPlayerWidget
from dvr import DVRManager
from iptv.parser import M3UParser
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class IntegrationController(QObject):
    """
    Main integration controller that bridges all components:
    - UI Pages
    - VLC Player
    - DVR Recording
    - IPTV Parser
    - Database
    """
    
    # Signals
    channel_loaded = Signal(dict)
    playback_started = Signal(str)
    recording_started = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.player: Optional[EnhancedVLCPlayerWidget] = None
        self.dvr_manager: Optional[DVRManager] = None
        self.iptv_parser: Optional[M3UParser] = None
        self.db_manager: Optional[DatabaseManager] = None
        
        # State
        self.current_channel = None
        self.loaded_channels: List[dict] = []
        self.favorite_channels: List[str] = []
        
        # Update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        
        logger.info("Integration Controller initialized")
    
    def initialize_components(self, parent_widget=None):
        """Initialize all components"""
        try:
            # Initialize Player
            self.player = EnhancedVLCPlayerWidget(parent_widget)
            self.player.playback_started.connect(lambda ch: self.playback_started.emit(ch))
            self.player.error_occurred.connect(lambda err: self.error_occurred.emit(err))
            
            # Initialize DVR
            self.dvr_manager = DVRManager()
            self.player.set_dvr_manager(self.dvr_manager)
            
            # Initialize IPTV Parser
            self.iptv_parser = M3UParser()
            
            # Initialize Database
            self.db_manager = DatabaseManager()
            asyncio.run(self.db_manager.initialize())
            
            # Connect player to DVR
            self.player.set_dvr_manager(self.dvr_manager)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            self.error_occurred.emit(f"Initialization failed: {str(e)}")
    
    def load_playlist(self, playlist_path: str) -> bool:
        """Load M3U/M3U8 playlist"""
        try:
            if not self.iptv_parser:
                raise Exception("IPTV Parser not initialized")
            
            # Parse playlist
            channels = self.iptv_parser.parse_file(playlist_path)
            
            if not channels:
                raise Exception("No channels found in playlist")
            
            self.loaded_channels = channels
            
            # Save to database
            if self.db_manager:
                asyncio.run(self._save_channels_to_db(channels))
            
            logger.info(f"Loaded {len(channels)} channels from {playlist_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load playlist: {e}")
            self.error_occurred.emit(f"Failed to load playlist: {str(e)}")
            return False
    
    async def _save_channels_to_db(self, channels: List[dict]):
        """Save channels to database"""
        try:
            for channel in channels:
                await self.db_manager.add_channel(
                    name=channel.get('name', 'Unknown'),
                    url=channel.get('url', ''),
                    category=channel.get('category', 'General'),
                    country=channel.get('country', 'Unknown'),
                    logo=channel.get('logo', '')
                )
        except Exception as e:
            logger.error(f"Failed to save channels to DB: {e}")
    
    def play_channel(self, channel: dict) -> bool:
        """Play a specific channel"""
        try:
            if not self.player:
                raise Exception("Player not initialized")
            
            channel_name = channel.get('name', 'Unknown')
            channel_url = channel.get('url', '')
            
            if not channel_url:
                raise Exception("Channel URL is empty")
            
            # Load and play
            self.player.load_channel(channel_name, channel_url, channel)
            self.player.play()
            
            self.current_channel = channel
            
            # Add to history
            if self.db_manager:
                asyncio.run(self.db_manager.add_watch_history(
                    content_id=channel_name,
                    content_type='channel',
                    title=channel_name
                ))
            
            self.channel_loaded.emit(channel)
            logger.info(f"Playing channel: {channel_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to play channel: {e}")
            self.error_occurred.emit(f"Failed to play channel: {str(e)}")
            return False
    
    def toggle_recording(self) -> bool:
        """Toggle recording for current channel"""
        if not self.player or not self.dvr_manager:
            return False
        
        self.player.toggle_recording()
        return True
    
    def get_channels_by_category(self, category: str) -> List[dict]:
        """Get channels filtered by category"""
        if category.lower() == 'all':
            return self.loaded_channels
        
        return [
            ch for ch in self.loaded_channels 
            if ch.get('category', '').lower() == category.lower()
        ]
    
    def get_channels_by_country(self, country: str) -> List[dict]:
        """Get channels filtered by country"""
        if country.lower() == 'all':
            return self.loaded_channels
        
        return [
            ch for ch in self.loaded_channels 
            if ch.get('country', '').lower() == country.lower()
        ]
    
    def search_channels(self, query: str) -> List[dict]:
        """Search channels by name"""
        query = query.lower()
        return [
            ch for ch in self.loaded_channels 
            if query in ch.get('name', '').lower()
        ]
    
    def add_to_favorites(self, channel_name: str) -> bool:
        """Add channel to favorites"""
        if channel_name not in self.favorite_channels:
            self.favorite_channels.append(channel_name)
            
            if self.db_manager:
                asyncio.run(self.db_manager.add_to_favorites(
                    content_id=channel_name,
                    content_type='channel'
                ))
            
            logger.info(f"Added to favorites: {channel_name}")
            return True
        return False
    
    def remove_from_favorites(self, channel_name: str) -> bool:
        """Remove channel from favorites"""
        if channel_name in self.favorite_channels:
            self.favorite_channels.remove(channel_name)
            
            if self.db_manager:
                asyncio.run(self.db_manager.remove_from_favorites(
                    content_id=channel_name,
                    content_type='channel'
                ))
            
            logger.info(f"Removed from favorites: {channel_name}")
            return True
        return False
    
    def get_favorites(self) -> List[dict]:
        """Get favorite channels"""
        return [
            ch for ch in self.loaded_channels 
            if ch.get('name') in self.favorite_channels
        ]
    
    def get_recording_status(self) -> dict:
        """Get current recording status"""
        if not self.dvr_manager:
            return {'active': False}
        
        active_recordings = self.dvr_manager.active_recordings
        stats = self.dvr_manager.get_storage_stats()
        
        return {
            'active': len(active_recordings) > 0,
            'count': len(active_recordings),
            'recordings': list(active_recordings.values()),
            'storage': stats
        }
    
    def get_playback_status(self) -> dict:
        """Get current playback status"""
        if not self.player:
            return {'playing': False}
        
        return {
            'playing': self.player._is_playing if hasattr(self.player, '_is_playing') else False,
            'paused': self.player._is_paused if hasattr(self.player, '_is_paused') else False,
            'channel': self.current_channel,
            'volume': self.player.get_volume() if hasattr(self.player, 'get_volume') else 80
        }
    
    @Slot()
    def _update_status(self):
        """Periodic status update"""
        # Could emit status signals here
        pass
    
    def cleanup(self):
        """Cleanup all resources"""
        logger.info("Cleaning up integration controller...")
        
        if self.status_timer:
            self.status_timer.stop()
        
        if self.player:
            self.player.cleanup()
        
        if self.db_manager:
            asyncio.run(self.db_manager.close())
        
        logger.info("Cleanup complete")


# Singleton instance
_integration_controller: Optional[IntegrationController] = None


def get_integration_controller() -> IntegrationController:
    """Get singleton instance of integration controller"""
    global _integration_controller
    if _integration_controller is None:
        _integration_controller = IntegrationController()
    return _integration_controller


# Test function
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    controller = get_integration_controller()
    controller.initialize_components()
    
    print("✅ Integration Controller Ready!")
    print(f"📺 Loaded Channels: {len(controller.loaded_channels)}")
    print(f"⭐ Favorites: {len(controller.favorite_channels)}")
    print(f"🎬 Playback Status: {controller.get_playback_status()}")
    print(f"📼 Recording Status: {controller.get_recording_status()}")
    
    sys.exit(app.exec())
