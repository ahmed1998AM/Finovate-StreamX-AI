"""
IPTV Parser Module
==================
M3U/M3U8 playlist parser with support for various IPTV formats.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import aiohttp
import asyncio


@dataclass
class Channel:
    """Represents an IPTV channel."""
    name: str
    stream_url: str
    logo_url: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    quality: Optional[str] = None
    epg_id: Optional[str] = None
    group_title: Optional[str] = None
    tvg_name: Optional[str] = None
    timeshift: Optional[str] = None
    catchup_days: Optional[str] = None
    catchup_type: Optional[str] = None
    extra_info: Dict[str, str] = field(default_factory=dict)


@dataclass
class Playlist:
    """Represents an IPTV playlist."""
    name: str
    channels: List[Channel] = field(default_factory=list)
    source_url: Optional[str] = None
    source_file: Optional[Path] = None
    format: str = "M3U"
    total_channels: int = 0
    
    def __post_init__(self):
        self.total_channels = len(self.channels)


class M3UParser:
    """Parser for M3U and M3U8 IPTV playlists."""
    
    # Regex patterns for parsing M3U attributes
    ATTR_PATTERN = re.compile(r'([a-zA-Z0-9_-]+)="([^"]*)"')
    INFO_PATTERN = re.compile(r'#EXTINF:(-?\d+),(.+)')
    
    def __init__(self):
        self.channels: List[Channel] = []
    
    def parse_file(self, file_path: Path) -> Playlist:
        """
        Parse M3U file from local path.
        
        Args:
            file_path: Path to M3U file
            
        Returns:
            Playlist object with parsed channels
        """
        if not file_path.exists():
            raise FileNotFoundError(f"M3U file not found: {file_path}")
        
        content = file_path.read_text(encoding='utf-8')
        playlist = self.parse_content(content)
        playlist.source_file = file_path
        
        return playlist
    
    async def parse_url(self, url: str, timeout: int = 30) -> Playlist:
        """
        Parse M3U playlist from URL.
        
        Args:
            url: URL to M3U playlist
            timeout: Request timeout in seconds
            
        Returns:
            Playlist object with parsed channels
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch playlist: HTTP {response.status}")
                
                content = await response.text(encoding='utf-8')
                playlist = self.parse_content(content)
                playlist.source_url = url
                
                return playlist
    
    def parse_content(self, content: str) -> Playlist:
        """
        Parse M3U content string.
        
        Args:
            content: M3U content as string
            
        Returns:
            Playlist object with parsed channels
        """
        self.channels.clear()
        lines = content.strip().split('\n')
        
        # Validate M3U header
        if not lines or not lines[0].startswith('#EXTM3U'):
            raise ValueError("Invalid M3U file: Missing #EXTM3U header")
        
        current_channel_info: Optional[Dict[str, Any]] = None
        
        for line in lines[1:]:
            line = line.strip()
            
            if not line or line.startswith('#EXTM3U'):
                continue
            
            # Parse EXTINF line
            if line.startswith('#EXTINF:'):
                current_channel_info = self._parse_extinf(line)
            
            # Parse stream URL
            elif line.startswith('http') or line.startswith('rtmp') or line.startswith('udp'):
                if current_channel_info:
                    channel = Channel(
                        name=current_channel_info.get('name', 'Unknown'),
                        stream_url=line,
                        **current_channel_info
                    )
                    self.channels.append(channel)
                    current_channel_info = None
            
            # Parse other EXT tags
            elif line.startswith('#'):
                if current_channel_info:
                    self._parse_ext_tag(line, current_channel_info)
        
        return Playlist(
            name="Imported Playlist",
            channels=self.channels.copy(),
            format="M3U8" if any(c.stream_url.endswith('.m3u8') for c in self.channels) else "M3U"
        )
    
    def _parse_extinf(self, line: str) -> Dict[str, Any]:
        """
        Parse #EXTINF line.
        
        Args:
            line: EXTINF line string
            
        Returns:
            Dictionary with channel information
        """
        info = {}
        
        # Extract attributes
        match = self.ATTR_PATTERN.findall(line)
        for key, value in match:
            key_lower = key.lower()
            
            if key_lower == 'tvg-logo':
                info['logo_url'] = value
            elif key_lower == 'tvg-name':
                info['tvg_name'] = value
            elif key_lower == 'tvg-id':
                info['epg_id'] = value
            elif key_lower == 'group-title':
                info['group_title'] = value
                info['category'] = value
            elif key_lower == 'tvg-country':
                info['country'] = value
            elif key_lower == 'tvg-language':
                info['language'] = value
            elif key_lower == 'tvg-chno':
                info['extra_info']['channel_number'] = value
            elif key_lower == 'timeshift':
                info['timeshift'] = value
            elif key_lower == 'catchup-days':
                info['catchup_days'] = value
            elif key_lower == 'catchup-type':
                info['catchup_type'] = value
            else:
                info['extra_info'][key_lower] = value
        
        # Extract channel name after comma
        info_match = self.INFO_PATTERN.search(line)
        if info_match:
            info['name'] = info_match.group(2).strip()
        
        return info
    
    def _parse_ext_tag(self, line: str, info: Dict[str, Any]):
        """
        Parse other EXT tags.
        
        Args:
            line: EXT tag line
            info: Channel info dictionary to update
        """
        if line.startswith('#EXTVLCOPT:'):
            # VLC options
            pass
        elif line.startswith('#KODIPROP:'):
            # Kodi properties
            pass
    
    def get_channels_by_category(self, category: str) -> List[Channel]:
        """Get all channels in a specific category."""
        return [c for c in self.channels if c.category and c.category.lower() == category.lower()]
    
    def get_channels_by_country(self, country: str) -> List[Channel]:
        """Get all channels from a specific country."""
        return [c for c in self.channels if c.country and c.country.lower() == country.lower()]
    
    def get_channels_by_quality(self, quality: str) -> List[Channel]:
        """Get all channels with specific quality."""
        return [c for c in self.channels if c.quality and quality.lower() in c.quality.lower()]
    
    def search_channels(self, query: str) -> List[Channel]:
        """Search channels by name."""
        query_lower = query.lower()
        return [c for c in self.channels if query_lower in c.name.lower()]
    
    def get_unique_categories(self) -> List[str]:
        """Get list of unique categories."""
        categories = set()
        for channel in self.channels:
            if channel.category:
                categories.add(channel.category)
        return sorted(list(categories))
    
    def get_unique_countries(self) -> List[str]:
        """Get list of unique countries."""
        countries = set()
        for channel in self.channels:
            if channel.country:
                countries.add(channel.country)
        return sorted(list(countries))


class XtreamCodesParser:
    """Parser for Xtream Codes API responses."""
    
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def connect(self):
        """Establish connection to Xtream Codes server."""
        self.session = aiohttp.ClientSession()
    
    async def disconnect(self):
        """Close connection."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Xtream Codes server."""
        if not self.session:
            await self.connect()
        
        url = f"{self.base_url}/player_api.php"
        params = {'username': self.username, 'password': self.password}
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('user_info', {}).get('auth', 0) == 1
            return False
    
    async def get_live_streams(self) -> List[Dict[str, Any]]:
        """Get all live streams."""
        url = f"{self.base_url}/player_api.php"
        params = {
            'username': self.username,
            'password': self.password,
            'action': 'get_live_streams'
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []
    
    async def get_vod_streams(self) -> List[Dict[str, Any]]:
        """Get all VOD streams."""
        url = f"{self.base_url}/player_api.php"
        params = {
            'username': self.username,
            'password': self.password,
            'action': 'get_vod_streams'
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []
    
    async def get_series(self) -> List[Dict[str, Any]]:
        """Get all series."""
        url = f"{self.base_url}/player_api.php"
        params = {
            'username': self.username,
            'password': self.password,
            'action': 'get_series'
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []
    
    async def get_short_epg(self, stream_id: int) -> Dict[str, Any]:
        """Get EPG for a specific stream."""
        url = f"{self.base_url}/player_api.php"
        params = {
            'username': self.username,
            'password': self.password,
            'action': 'get_short_epg',
            'stream_id': stream_id
        }
        
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return {}
