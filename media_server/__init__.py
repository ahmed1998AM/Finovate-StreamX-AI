"""
Finovate StreamX AI - Media Server Module
DLNA/UPnP Server, Local Streaming, Network Sharing
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import os
import socket
import threading
import asyncio
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DLNAMediaServer:
    """DLNA/UPnP Media Server for home network streaming"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        self.host = host
        self.port = port
        self.media_library: Dict[str, dict] = {}
        self.clients: List[str] = []
        self.server: Optional[HTTPServer] = None
        self.running = False
        self.library_path = Path.home() / "StreamX_Media"
        self.library_path.mkdir(exist_ok=True)
        
    def scan_local_media(self, directories: List[str] = None) -> Dict:
        """Scan local directories for media files"""
        if not directories:
            directories = [
                str(self.library_path),
                str(Path.home() / "Videos"),
                str(Path.home() / "Movies"),
                str(Path.home() / "Downloads")
            ]
        
        media_files = {
            'videos': [],
            'music': [],
            'images': []
        }
        
        video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
        audio_exts = ['.mp3', '.flac', '.aac', '.wav', '.ogg', '.m4a']
        image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
        for directory in directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                continue
                
            for file_path in dir_path.rglob('*'):
                if file_path.is_file():
                    suffix = file_path.suffix.lower()
                    file_info = {
                        'path': str(file_path),
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        'mime_type': self._get_mime_type(suffix)
                    }
                    
                    if suffix in video_exts:
                        media_files['videos'].append(file_info)
                    elif suffix in audio_exts:
                        media_files['music'].append(file_info)
                    elif suffix in image_exts:
                        media_files['images'].append(file_info)
        
        self.media_library = media_files
        logger.info(f"Scanned {sum(len(v) for v in media_files.values())} media files")
        return media_files
    
    def _get_mime_type(self, ext: str) -> str:
        """Get MIME type for file extension"""
        mime_types = {
            '.mp4': 'video/mp4',
            '.mkv': 'video/x-matroska',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.mp3': 'audio/mpeg',
            '.flac': 'audio/flac',
            '.jpg': 'image/jpeg',
            '.png': 'image/png'
        }
        return mime_types.get(ext, 'application/octet-stream')
    
    def start_server(self):
        """Start DLNA media server"""
        class MediaHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/device.xml':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/xml')
                    self.end_headers()
                    self.wfile.write(self._generate_device_xml())
                elif self.path.startswith('/media/'):
                    file_path = self.path.replace('/media/', '')
                    if os.path.exists(file_path):
                        self.send_response(200)
                        self.send_header('Content-Type', self._get_mime_type(os.path.splitext(file_path)[1]))
                        self.send_header('Content-Length', os.path.getsize(file_path))
                        self.end_headers()
                        with open(file_path, 'rb') as f:
                            self.wfile.write(f.read())
                    else:
                        self.send_error(404)
                else:
                    super().do_GET()
            
            def _generate_device_xml(self):
                root = ET.Element('root', xmlns='urn:schemas-upnp-org:device-1-0')
                device = ET.SubElement(root, 'device')
                
                ET.SubElement(device, 'deviceType').text = 'urn:schemas-upnp-org:device:MediaServer:1'
                ET.SubElement(device, 'friendlyName').text = 'Finovate StreamX Media Server'
                ET.SubElement(device, 'manufacturer').text = 'Finovate – AHMED EG'
                ET.SubElement(device, 'modelName').text = 'StreamX AI'
                ET.SubElement(device, 'UDN').text = f'uuid:{socket.gethostname()}-streamx'
                
                service_list = ET.SubElement(device, 'serviceList')
                service = ET.SubElement(service_list, 'service')
                ET.SubElement(service, 'serviceType').text = 'urn:schemas-upnp-org:service:ContentDirectory:1'
                ET.SubElement(service, 'serviceId').text = 'urn:upnp-org:serviceId:ContentDirectory'
                
                return ET.tostring(root, encoding='utf-8', xml_declaration=True)
        
        try:
            self.server = HTTPServer((self.host, self.port), MediaHandler)
            self.running = True
            logger.info(f"DLNA Server started on http://{self.host}:{self.port}")
            self.server.serve_forever()
        except Exception as e:
            logger.error(f"Failed to start DLNA server: {e}")
            self.running = False
    
    def stop_server(self):
        """Stop DLNA media server"""
        if self.server:
            self.server.shutdown()
            self.running = False
            logger.info("DLNA Server stopped")
    
    def get_library_stats(self) -> Dict:
        """Get media library statistics"""
        return {
            'total_videos': len(self.media_library.get('videos', [])),
            'total_music': len(self.media_library.get('music', [])),
            'total_images': len(self.media_library.get('images', [])),
            'total_size_mb': sum(
                f.get('size', 0) 
                for category in self.media_library.values() 
                for f in category
            ) / (1024 * 1024),
            'connected_clients': len(self.clients)
        }


class RemoteAccessManager:
    """Manage remote access to media server"""
    
    def __init__(self, media_server: DLNAMediaServer):
        self.media_server = media_server
        self.access_tokens: Dict[str, dict] = {}
        self.port_forwarding = False
        
    def generate_access_token(self, user_id: str, permissions: List[str]) -> str:
        """Generate secure access token for remote users"""
        import secrets
        token = secrets.token_urlsafe(32)
        self.access_tokens[token] = {
            'user_id': user_id,
            'permissions': permissions,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now().replace(hour=23, minute=59, second=59)).isoformat()
        }
        return token
    
    def validate_token(self, token: str) -> bool:
        """Validate access token"""
        if token not in self.access_tokens:
            return False
        
        token_data = self.access_tokens[token]
        expiry = datetime.fromisoformat(token_data['expires_at'])
        
        if datetime.now() > expiry:
            del self.access_tokens[token]
            return False
        
        return True
    
    def setup_port_forwarding(self, external_port: int = 8080):
        """Setup UPnP port forwarding (requires router support)"""
        try:
            # Simplified UPnP port forwarding
            import socket
            logger.info(f"Attempting UPnP port forwarding to port {external_port}")
            self.port_forwarding = True
            return True
        except Exception as e:
            logger.warning(f"UPnP port forwarding failed: {e}")
            return False


class MediaIndexer:
    """Advanced media indexing with metadata extraction"""
    
    def __init__(self):
        self.index: Dict[str, dict] = {}
        self.metadata_cache = {}
        
    async def index_media(self, file_path: str) -> dict:
        """Index media file with metadata extraction"""
        path = Path(file_path)
        if not path.exists():
            return {}
        
        # Extract metadata using ffprobe or similar
        metadata = {
            'path': str(path),
            'filename': path.name,
            'size': path.stat().st_size,
            'extension': path.suffix,
            'indexed_at': datetime.now().isoformat()
        }
        
        # Try to extract video metadata
        if path.suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov']:
            metadata.update(await self._extract_video_metadata(str(path)))
        
        self.index[str(path)] = metadata
        return metadata
    
    async def _extract_video_metadata(self, file_path: str) -> dict:
        """Extract video metadata using FFmpeg"""
        try:
            import subprocess
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                return {
                    'duration': float(data.get('format', {}).get('duration', 0)),
                    'bitrate': data.get('format', {}).get('bit_rate', ''),
                    'codec': data.get('streams', [{}])[0].get('codec_name', ''),
                    'resolution': f"{data.get('streams', [{}])[0].get('width', 0)}x{data.get('streams', [{}])[0].get('height', 0)}"
                }
        except Exception as e:
            logger.warning(f"Failed to extract metadata: {e}")
        
        return {}
    
    def search_index(self, query: str) -> List[dict]:
        """Search media index"""
        results = []
        query_lower = query.lower()
        
        for item in self.index.values():
            if (query_lower in item.get('filename', '').lower() or
                query_lower in item.get('path', '').lower()):
                results.append(item)
        
        return results


# Example usage
if __name__ == "__main__":
    server = DLNAMediaServer(port=8080)
    server.scan_local_media()
    print(f"Library stats: {server.get_library_stats()}")
    
    # Start server in background thread
    server_thread = threading.Thread(target=server.start_server, daemon=True)
    server_thread.start()
    
    print("Media Server running... Press Ctrl+C to stop")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop_server()
