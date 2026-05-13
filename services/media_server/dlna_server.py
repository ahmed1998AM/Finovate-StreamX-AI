"""
Finovate StreamX AI - DLNA/UPnP Server
خادم DLNA للبث المنزلي على الشبكة المحلية

المطور: Ahmed Mostafa Ibrahim
Finovate – AHMED EG
"""

import asyncio
import socket
import struct
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from aiohttp import web
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class DLNAServer:
    """
    خادم DLNA/UPnP لبث الوسائط على الشبكة المحلية
    
    الميزات:
    - DLNA/UPnP server discovery
    - Media streaming عبر HTTP
    - Device detection التلقائي
    - Content directory service
    - AV transport service
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8200):
        self.host = host
        self.port = port
        self.server_uuid = str(uuid.uuid4())
        self.device_name = "Finovate StreamX AI Media Server"
        self.manufacturer = "Finovate – AHMED EG"
        self.running = False
        self.app = web.Application()
        self.runner: Optional[web.AppRunner] = None
        self.media_items: List[Dict[str, Any]] = []
        self.clients: List[Dict[str, Any]] = []
        
        self._setup_routes()
    
    def _setup_routes(self):
        """إعداد مسارات الخادم"""
        self.app.router.add_get('/', self._handle_root)
        self.app.router.add_get('/description.xml', self._handle_description)
        self.app.router.add_get('/media/{item_id}', self._handle_media)
        self.app.router.add_get('/media/{item_id}/thumbnail', self._handle_thumbnail)
        self.app.router.add_post('/control/*', self._handle_control)
        self.app.router.add_get('/event/*', self._handle_event)
    
    async def start(self):
        """تشغيل خادم DLNA"""
        try:
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            site = web.TCPSite(self.runner, self.host, self.port)
            await site.start()
            self.running = True
            
            # بدء إعلانات SSDP
            asyncio.create_task(self._start_ssdp_advertisements())
            
            logger.info(f"DLNA Server started on http://{self.host}:{self.port}")
            logger.info(f"Device UUID: {self.server_uuid}")
            
        except Exception as e:
            logger.error(f"Failed to start DLNA server: {e}")
            raise
    
    async def stop(self):
        """إيقاف خادم DLNA"""
        self.running = False
        if self.runner:
            await self.runner.cleanup()
        logger.info("DLNA Server stopped")
    
    async def _handle_root(self, request: web.Request) -> web.Response:
        """معالجة طلب الجذر"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.device_name}</title>
            <style>
                body {{ font-family: Arial; background: #0B1020; color: #fff; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #1E88E5; }}
                .media-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }}
                .media-item {{ background: #121A2B; border-radius: 10px; overflow: hidden; }}
                .media-item img {{ width: 100%; height: 150px; object-fit: cover; }}
                .media-item-info {{ padding: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{self.device_name}</h1>
                <p>Media Server by Finovate – AHMED EG</p>
                <div class="media-grid">
                    {''.join([self._render_media_item(item) for item in self.media_items[:20]])}
                </div>
            </div>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')
    
    def _render_media_item(self, item: Dict[str, Any]) -> str:
        """ت-render عنصر وسائط"""
        return f"""
        <div class="media-item">
            <img src="/media/{item['id']}/thumbnail" alt="{item.get('title', 'Unknown')}">
            <div class="media-item-info">
                <h3>{item.get('title', 'Unknown')}</h3>
                <p>{item.get('type', 'Media')}</p>
            </div>
        </div>
        """
    
    async def _handle_description(self, request: web.Request) -> web.Response:
        """معالجة وصف الجهاز DLNA"""
        url = f"http://{request.host}"
        
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="urn:schemas-upnp-org:device-1-0">
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>
    <device>
        <deviceType>urn:schemas-upnp-org:device:MediaServer:1</deviceType>
        <friendlyName>{self.device_name}</friendlyName>
        <manufacturer>{self.manufacturer}</manufacturer>
        <manufacturerURL>https://github.com/ahmed1998AM</manufacturerURL>
        <modelDescription>Finovate StreamX AI Media Server</modelDescription>
        <modelName>StreamX Media Server</modelName>
        <modelNumber>1.0</modelNumber>
        <serialNumber>{self.server_uuid}</serialNumber>
        <UDN>uuid:{self.server_uuid}</UDN>
        <serviceList>
            <service>
                <serviceType>urn:schemas-upnp-org:service:ContentDirectory:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:ContentDirectory</serviceId>
                <controlURL>/control/content_directory</controlURL>
                <eventSubURL>/event/content_directory</eventSubURL>
                <SCPDURL>/content_directory.xml</SCPDURL>
            </service>
            <service>
                <serviceType>urn:schemas-upnp-org:service:AVTransport:1</serviceType>
                <serviceId>urn:upnp-org:serviceId:AVTransport</serviceId>
                <controlURL>/control/av_transport</controlURL>
                <eventSubURL>/event/av_transport</eventSubURL>
                <SCPDURL>/av_transport.xml</SCPDURL>
            </service>
        </serviceList>
        <presentationURL>{url}/</presentationURL>
    </device>
</root>'''
        
        return web.Response(text=xml, content_type='text/xml')
    
    async def _handle_media(self, request: web.Request) -> web.Response:
        """معالجة طلب وسائط"""
        item_id = request.match_info['item_id']
        
        # البحث عن العنصر
        media_item = next((item for item in self.media_items if item['id'] == item_id), None)
        
        if not media_item:
            return web.Response(status=404, text="Media not found")
        
        file_path = Path(media_item['path'])
        
        if not file_path.exists():
            return web.Response(status=404, text="File not found")
        
        # بث الملف مع دعم Range requests
        return await self._stream_file(file_path, request)
    
    async def _stream_file(self, file_path: Path, request: web.Request) -> web.Response:
        """بث ملف مع دعم Range requests"""
        file_size = file_path.stat().st_size
        
        # التحقق من Range header
        range_header = request.headers.get('Range')
        
        if range_header:
            # معالجة طلب Range
            range_start, range_end = self._parse_range_header(range_header, file_size)
            
            with open(file_path, 'rb') as f:
                f.seek(range_start)
                data = f.read(range_end - range_start + 1)
            
            response = web.Response(
                status=206,
                body=data,
                content_type=self._get_content_type(file_path)
            )
            response.headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'
            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Content-Length'] = str(len(data))
            
        else:
            # بث كامل الملف
            with open(file_path, 'rb') as f:
                data = f.read()
            
            response = web.Response(
                body=data,
                content_type=self._get_content_type(file_path)
            )
            response.headers['Content-Length'] = str(file_size)
            response.headers['Accept-Ranges'] = 'bytes'
        
        return response
    
    def _parse_range_header(self, range_header: str, file_size: int) -> tuple:
        """تحليل Range header"""
        try:
            range_spec = range_header.replace('bytes=', '')
            start_str, end_str = range_spec.split('-')
            
            range_start = int(start_str) if start_str else 0
            range_end = int(end_str) if end_str else file_size - 1
            
            range_end = min(range_end, file_size - 1)
            
            return range_start, range_end
        except:
            return 0, file_size - 1
    
    async def _handle_thumbnail(self, request: web.Request) -> web.Response:
        """معالجة طلب صورة مصغرة"""
        item_id = request.match_info['item_id']
        
        media_item = next((item for item in self.media_items if item['id'] == item_id), None)
        
        if not media_item or 'thumbnail' not in media_item:
            # إرجاع صورة افتراضية
            return web.Response(status=404, text="Thumbnail not found")
        
        thumbnail_path = Path(media_item['thumbnail'])
        
        if not thumbnail_path.exists():
            return web.Response(status=404, text="Thumbnail not found")
        
        with open(thumbnail_path, 'rb') as f:
            data = f.read()
        
        return web.Response(body=data, content_type='image/jpeg')
    
    async def _handle_control(self, request: web.Request) -> web.Response:
        """معالجة طلبات التحكم SOAP"""
        # تحليل طلب SOAP
        body = await request.text()
        
        # تنفيذ الإجراء المطلوب
        # (تنفيذ مبسط - يحتاج لتطوير كامل)
        
        response_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <s:Body>
        <u:BrowseResponse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
            <Result>&lt;DIDL-Lite&gt;&lt;/DIDL-Lite&gt;</Result>
            <NumberReturned>0</NumberReturned>
            <TotalMatches>0</TotalMatches>
            <UpdateID>1</UpdateID>
        </u:BrowseResponse>
    </s:Body>
</s:Envelope>'''
        
        return web.Response(text=response_xml, content_type='text/xml')
    
    async def _handle_event(self, request: web.Request) -> web.Response:
        """معالجة طلبات الأحداث GENA"""
        # تنفيذ نظام الأحداث
        return web.Response(status=200)
    
    async def _start_ssdp_advertisements(self):
        """بدء إعلانات SSDP لاكتشاف الأجهزة"""
        while self.running:
            try:
                # إرسال إعلانات M-SEARCH و NOTIFY
                await self._send_ssdp_notify()
                await asyncio.sleep(30)  # إعادة كل 30 ثانية
            except Exception as e:
                logger.error(f"SSDP advertisement error: {e}")
                await asyncio.sleep(5)
    
    async def _send_ssdp_notify(self):
        """إرسال إعلان SSDP NOTIFY"""
        message = (
            f'NOTIFY * HTTP/1.1\r\n'
            f'HOST: 239.255.255.250:1900\r\n'
            f'CACHE-CONTROL: max-age=1800\r\n'
            f'LOCATION: http://{self.host}:{self.port}/description.xml\r\n'
            f'NT: urn:schemas-upnp-org:device:MediaServer:1\r\n'
            f'NTS: ssdp:alive\r\n'
            f'SERVER: Linux/UPnP/1.0 Finovate-StreamX/1.0\r\n'
            f'USN: uuid:{self.server_uuid}::urn:schemas-upnp-org:device:MediaServer:1\r\n'
            f'\r\n'
        ).encode('utf-8')
        
        # إرسال إلى multicast address
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        try:
            sock.sendto(message, ('239.255.255.250', 1900))
            logger.debug("Sent SSDP NOTIFY")
        finally:
            sock.close()
    
    def add_media_item(self, media_item: Dict[str, Any]):
        """إضافة عنصر وسائط"""
        self.media_items.append(media_item)
        logger.info(f"Added media item: {media_item.get('title', 'Unknown')}")
    
    def remove_media_item(self, item_id: str):
        """إزالة عنصر وسائط"""
        self.media_items = [item for item in self.media_items if item['id'] != item_id]
    
    def _get_content_type(self, file_path: Path) -> str:
        """الحصول على نوع المحتوى من الامتداد"""
        extensions = {
            '.mp4': 'video/mp4',
            '.mkv': 'video/x-matroska',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.wmv': 'video/x-ms-wmv',
            '.mp3': 'audio/mpeg',
            '.flac': 'audio/flac',
            '.aac': 'audio/aac',
            '.wav': 'audio/wav',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
        }
        return extensions.get(file_path.suffix.lower(), 'application/octet-stream')
    
    def get_server_info(self) -> Dict[str, Any]:
        """الحصول على معلومات الخادم"""
        return {
            'name': self.device_name,
            'uuid': self.server_uuid,
            'host': self.host,
            'port': self.port,
            'running': self.running,
            'media_count': len(self.media_items),
            'client_count': len(self.clients),
            'manufacturer': self.manufacturer
        }
