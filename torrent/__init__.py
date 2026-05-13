"""
Finovate StreamX AI - Torrent Streaming Module
Magnet/Torrent Streaming, RealDebrid/Premiumize Support
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import os
import asyncio
import threading
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Callable
import json
import logging
from dataclasses import dataclass
import time
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class TorrentStream:
    """Torrent stream metadata"""
    id: str
    magnet_uri: str
    torrent_hash: str
    name: str
    size_bytes: int
    progress: float
    download_speed: float
    upload_speed: float
    peers: int
    seeds: int
    status: str  # downloading, streaming, completed, stopped
    selected_file: Optional[str] = None
    stream_url: Optional[str] = None


class TorrentStreamingEngine:
    """Torrent streaming engine with RealDebrid/Premiumize support"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / "StreamX_Torrent_Cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.active_streams: Dict[str, TorrentStream] = {}
        self.stream_processes: Dict[str, subprocess.Popen] = {}
        
        # Premium services
        self.realdebrid_api_key: Optional[str] = None
        self.premiumize_api_key: Optional[str] = None
        
        # Configuration
        self.max_download_speed_mbps = 0  # 0 = unlimited
        self.cache_size_gb = 10
        self.auto_delete_completed = False
    
    def set_realdebrid_key(self, api_key: str):
        """Set RealDebrid API key for premium streaming"""
        self.realdebrid_api_key = api_key
        logger.info("RealDebrid API key configured")
    
    def set_premiumize_key(self, api_key: str):
        """Set Premiumize API key for premium streaming"""
        self.premiumize_api_key = api_key
        logger.info("Premiumize API key configured")
    
    def _extract_torrent_hash(self, magnet_uri: str) -> str:
        """Extract torrent hash from magnet URI"""
        try:
            # Magnet URI format: magnet:?xt=urn:btih:<hash>&...
            parts = magnet_uri.split('&')
            for part in parts:
                if part.startswith('xt=urn:btih:'):
                    return part.split(':')[2].lower()
        except Exception as e:
            logger.warning(f"Failed to extract torrent hash: {e}")
        
        # Fallback: generate hash from URI
        return hashlib.sha1(magnet_uri.encode()).hexdigest()
    
    async def start_torrent_stream(
        self,
        magnet_uri: str,
        file_index: int = 0,
        use_premium: bool = True
    ) -> TorrentStream:
        """Start streaming a torrent"""
        
        torrent_hash = self._extract_torrent_hash(magnet_uri)
        stream_id = f"torrent_{torrent_hash[:8]}"
        
        # Check if using premium service
        if use_premium and self.realdebrid_api_key:
            return await self._stream_with_realdebrid(magnet_uri, stream_id)
        elif use_premium and self.premiumize_api_key:
            return await self._stream_with_premiumize(magnet_uri, stream_id)
        else:
            return await self._stream_direct(magnet_uri, file_index, stream_id)
    
    async def _stream_with_realdebrid(self, magnet_uri: str, stream_id: str) -> TorrentStream:
        """Stream torrent using RealDebrid premium service"""
        try:
            import aiohttp
            
            # Add magnet to RealDebrid
            headers = {'Authorization': f'Bearer {self.realdebrid_api_key}'}
            
            async with aiohttp.ClientSession() as session:
                # Step 1: Add magnet
                async with session.post(
                    'https://api.real-debrid.com/rest/1.0/torrents/addMagnet',
                    headers=headers,
                    data={'magnet': magnet_uri}
                ) as response:
                    if response.status != 201:
                        raise Exception(f"RealDebrid API error: {response.status}")
                    
                    torrent_data = await response.json()
                    torrent_id = torrent_data['id']
                
                # Step 2: Get torrent info
                async with session.get(
                    f'https://api.real-debrid.com/rest/1.0/torrents/{torrent_id}',
                    headers=headers
                ) as response:
                    torrent_info = await response.json()
                    
                    if not torrent_info.get('files'):
                        raise Exception("No files found in torrent")
                    
                    # Select first video file
                    selected_file = None
                    for file in torrent_info['files']:
                        if any(ext in file['path'].lower() for ext in ['.mp4', '.mkv', '.avi']):
                            selected_file = file
                            break
                    
                    if not selected_file:
                        selected_file = torrent_info['files'][0]
                    
                    file_id = selected_file['id']
                    
                    # Step 3: Select file and get link
                    async with session.post(
                        f'https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{torrent_id}',
                        headers=headers,
                        data={'files': str(file_id)}
                    ) as response:
                        if response.status != 204:
                            # Files already selected
                            pass
                    
                    # Step 4: Get streaming links
                    async with session.get(
                        f'https://api.real-debrid.com/rest/1.0/torrents/{torrent_id}',
                        headers=headers
                    ) as response:
                        torrent_status = await response.json()
                        
                        if torrent_status.get('links'):
                            stream_url = torrent_status['links'][0]
                            
                            stream = TorrentStream(
                                id=stream_id,
                                magnet_uri=magnet_uri,
                                torrent_hash=self._extract_torrent_hash(magnet_uri),
                                name=torrent_status.get('original_filename', 'Unknown'),
                                size_bytes=torrent_status.get('bytes', 0),
                                progress=100.0,
                                download_speed=0,
                                upload_speed=0,
                                peers=0,
                                seeds=0,
                                status='streaming',
                                selected_file=selected_file['path'],
                                stream_url=stream_url
                            )
                            
                            self.active_streams[stream_id] = stream
                            logger.info(f"RealDebrid stream ready: {stream.name}")
                            return stream
            
            raise Exception("Failed to get stream URL from RealDebrid")
            
        except Exception as e:
            logger.error(f"RealDebrid streaming failed: {e}")
            # Fallback to direct streaming
            return await self._stream_direct(magnet_uri, 0, stream_id)
    
    async def _stream_with_premiumize(self, magnet_uri: str, stream_id: str) -> TorrentStream:
        """Stream torrent using Premiumize premium service"""
        try:
            import aiohttp
            
            headers = {'Authorization': f'Bearer {self.premiumize_api_key}'}
            
            async with aiohttp.ClientSession() as session:
                # Create transfer
                async with session.post(
                    'https://www.premiumize.me/api/transfer/create',
                    headers=headers,
                    data={'src': magnet_uri}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Premiumize API error: {response.status}")
                    
                    transfer_data = await response.json()
                    transfer_id = transfer_data['id']
                
                # Wait for transfer to complete (polling)
                while True:
                    async with session.get(
                        f'https://www.premiumize.me/api/transfer/status',
                        headers=headers,
                        params={'id': transfer_id}
                    ) as response:
                        status_data = await response.json()
                        
                        if status_data.get('status') == 'finished':
                            # Get file link
                            if status_data.get('link'):
                                stream_url = status_data['link']
                                
                                stream = TorrentStream(
                                    id=stream_id,
                                    magnet_uri=magnet_uri,
                                    torrent_hash=self._extract_torrent_hash(magnet_uri),
                                    name=status_data.get('filename', 'Unknown'),
                                    size_bytes=status_data.get('file_size', 0),
                                    progress=100.0,
                                    download_speed=0,
                                    upload_speed=0,
                                    peers=0,
                                    seeds=0,
                                    status='streaming',
                                    stream_url=stream_url
                                )
                                
                                self.active_streams[stream_id] = stream
                                logger.info(f"Premiumize stream ready: {stream.name}")
                                return stream
                        elif status_data.get('status') in ['failed', 'deleted']:
                            raise Exception("Premiumize transfer failed")
                    
                    await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Premiumize streaming failed: {e}")
            return await self._stream_direct(magnet_uri, 0, stream_id)
    
    async def _stream_direct(self, magnet_uri: str, file_index: int, stream_id: str) -> TorrentStream:
        """Stream torrent directly using libtorrent or webtorrent"""
        try:
            # Try to use webtorrent-cli if available
            cache_path = self.cache_dir / stream_id
            
            cmd = [
                'webtorrent',
                magnet_uri,
                '--out', str(cache_path),
                '--index', str(file_index),
                '--port', '8081'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            self.stream_processes[stream_id] = process
            
            # Wait for stream to be ready
            await asyncio.sleep(10)
            
            stream = TorrentStream(
                id=stream_id,
                magnet_uri=magnet_uri,
                torrent_hash=self._extract_torrent_hash(magnet_uri),
                name=f"Torrent {stream_id}",
                size_bytes=0,
                progress=0.0,
                download_speed=0,
                upload_speed=0,
                peers=0,
                seeds=0,
                status='downloading',
                selected_file=None,
                stream_url=f'http://localhost:8081/0'
            )
            
            self.active_streams[stream_id] = stream
            logger.info(f"Direct torrent streaming started: {stream_id}")
            
            return stream
            
        except Exception as e:
            logger.error(f"Direct torrent streaming failed: {e}")
            raise
    
    def stop_stream(self, stream_id: str) -> bool:
        """Stop a torrent stream"""
        if stream_id not in self.stream_processes:
            return False
        
        process = self.stream_processes[stream_id]
        process.terminate()
        
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        
        if stream_id in self.active_streams:
            del self.active_streams[stream_id]
        if stream_id in self.stream_processes:
            del self.stream_processes[stream_id]
        
        logger.info(f"Stopped torrent stream: {stream_id}")
        return True
    
    def get_stream_status(self, stream_id: str) -> Optional[TorrentStream]:
        """Get current status of a torrent stream"""
        return self.active_streams.get(stream_id)
    
    def get_all_streams(self) -> List[TorrentStream]:
        """Get all active streams"""
        return list(self.active_streams.values())
    
    def get_cache_stats(self) -> Dict:
        """Get torrent cache statistics"""
        total_size = sum(
            f.stat().st_size 
            for f in self.cache_dir.rglob('*') 
            if f.is_file()
        )
        
        return {
            'active_streams': len(self.active_streams),
            'cache_size_mb': total_size / (1024 * 1024),
            'cache_size_gb': total_size / (1024 * 1024 * 1024),
            'max_cache_gb': self.cache_size_gb,
            'cache_path': str(self.cache_dir)
        }
    
    def clear_cache(self):
        """Clear torrent cache"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)
            logger.info("Torrent cache cleared")


# Example usage
if __name__ == "__main__":
    engine = TorrentStreamingEngine()
    
    # Example magnet URI (test torrent)
    test_magnet = "magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10&dn=Sintel"
    
    print("Torrent Streaming Engine initialized")
    print(f"Cache stats: {engine.get_cache_stats()}")
    
    # Note: Actual streaming requires webtorrent-cli or similar tool installed
    # pip install webtorrent-cli
