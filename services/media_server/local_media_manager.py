"""
Finovate StreamX AI - Local Media Manager
إدارة المكتبة المحلية للوسائط

المطور: Ahmed Mostafa Ibrahim
Finovate – AHMED EG
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import logging
import hashlib
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent, FileDeletedEvent

logger = logging.getLogger(__name__)


class MediaFileHandler(FileSystemEventHandler):
    """معالج أحداث نظام الملفات للوسائط"""
    
    def __init__(self, media_manager):
        self.media_manager = media_manager
    
    def on_created(self, event):
        if not event.is_directory:
            self.media_manager._on_file_created(event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.media_manager._on_file_modified(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.media_manager._on_file_deleted(event.src_path)


class LocalMediaManager:
    """
    مدير المكتبة المحلية للوسائط
    
    الميزات:
    - مسح المجلدات تلقائيًا
    - فهرسة الوسائط (فيديو، صوت، صور)
    - استخراج Metadata
    - توليد Thumbnails
    - مراقبة التغييرات في الوقت الفعلي
    - تنظيم حسب النوع والتصنيف
    """
    
    VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
    AUDIO_EXTENSIONS = {'.mp3', '.flac', '.aac', '.wav', '.ogg', '.wma', '.m4a'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    def __init__(self, scan_paths: List[str] = None):
        self.scan_paths = scan_paths or []
        self.media_library: Dict[str, Dict[str, Any]] = {}
        self.video_count = 0
        self.audio_count = 0
        self.image_count = 0
        self.observer: Optional[Observer] = None
        self.handler: Optional[MediaFileHandler] = None
        self._scan_lock = asyncio.Lock()
        
    def add_scan_path(self, path: str):
        """إضافة مسار للمسح"""
        path_obj = Path(path)
        if path_obj.exists() and path_obj.is_dir():
            if path not in self.scan_paths:
                self.scan_paths.append(path)
                logger.info(f"Added scan path: {path}")
                # مسح فوري للمسار الجديد
                asyncio.create_task(self.scan_path_async(path))
        else:
            logger.warning(f"Path does not exist or is not a directory: {path}")
    
    def remove_scan_path(self, path: str):
        """إزالة مسار من المسح"""
        if path in self.scan_paths:
            self.scan_paths.remove(path)
            # إزالة الوسائط من هذا المسار
            self._remove_media_from_path(path)
            logger.info(f"Removed scan path: {path}")
    
    async def scan_all_paths(self):
        """مسح جميع المسارات"""
        async with self._scan_lock:
            for path in self.scan_paths:
                await self.scan_path_async(path)
    
    async def scan_path_async(self, path: str):
        """مسح مسار بشكل غير متزامن"""
        try:
            path_obj = Path(path)
            if not path_obj.exists() or not path_obj.is_dir():
                return
            
            logger.info(f"Scanning path: {path}")
            
            # مسح متوازي للملفات
            tasks = []
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    tasks.append(self._process_file_async(file_path))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            logger.info(f"Completed scanning: {path}")
            logger.info(f"Library stats - Videos: {self.video_count}, Audio: {self.audio_count}, Images: {self.image_count}")
            
        except Exception as e:
            logger.error(f"Error scanning path {path}: {e}")
    
    async def _process_file_async(self, file_path: Path):
        """معالجة ملف بشكل غير متزامن"""
        try:
            ext = file_path.suffix.lower()
            
            if ext in self.VIDEO_EXTENSIONS:
                media_type = 'video'
                self.video_count += 1
            elif ext in self.AUDIO_EXTENSIONS:
                media_type = 'audio'
                self.audio_count += 1
            elif ext in self.IMAGE_EXTENSIONS:
                media_type = 'image'
                self.image_count += 1
            else:
                return
            
            # إنشاء معرف فريد
            file_id = self._generate_file_id(file_path)
            
            # استخراج المعلومات
            metadata = await self._extract_metadata(file_path, media_type)
            
            # إضافة للمكتبة
            self.media_library[file_id] = {
                'id': file_id,
                'path': str(file_path),
                'name': file_path.name,
                'type': media_type,
                'extension': ext,
                'size': file_path.stat().st_size,
                'created': datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                **metadata
            }
            
        except Exception as e:
            logger.debug(f"Error processing file {file_path}: {e}")
    
    async def _extract_metadata(self, file_path: Path, media_type: str) -> Dict[str, Any]:
        """استخراج Metadata من الملف"""
        metadata = {
            'title': file_path.stem,
            'duration': None,
            'resolution': None,
            'codec': None,
            'bitrate': None,
            'thumbnail': None,
            'artist': None,
            'album': None,
            'year': None,
            'genre': None,
        }
        
        # محاولة استخدام ffprobe لاستخراج المعلومات
        try:
            import subprocess
            result = subprocess.run(
                [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json',
                    '-show_format', '-show_streams', str(file_path)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # معلومات التنسيق
                if 'format' in data:
                    fmt = data['format']
                    metadata['duration'] = float(fmt.get('duration', 0))
                    metadata['bitrate'] = int(fmt.get('bit_rate', 0))
                    if 'tags' in fmt:
                        tags = fmt['tags']
                        metadata['title'] = tags.get('title', file_path.stem)
                        metadata['artist'] = tags.get('artist')
                        metadata['album'] = tags.get('album')
                        metadata['year'] = tags.get('date')
                        metadata['genre'] = tags.get('genre')
                
                # معلومات الفيديو
                if media_type == 'video' and 'streams' in data:
                    for stream in data['streams']:
                        if stream.get('codec_type') == 'video':
                            metadata['codec'] = stream.get('codec_name')
                            metadata['resolution'] = f"{stream.get('width', 0)}x{stream.get('height', 0)}"
                            break
                
                # توليد thumbnail
                if media_type == 'video' and metadata['duration']:
                    thumbnail_path = await self._generate_thumbnail(file_path, metadata['duration'])
                    if thumbnail_path:
                        metadata['thumbnail'] = thumbnail_path
                
        except Exception as e:
            logger.debug(f"Failed to extract metadata for {file_path}: {e}")
        
        return metadata
    
    async def _generate_thumbnail(self, video_path: Path, duration: float) -> Optional[str]:
        """توليد صورة مصغرة من الفيديو"""
        try:
            import subprocess
            
            thumbnail_dir = Path(__file__).parent.parent.parent / 'cache' / 'thumbnails'
            thumbnail_dir.mkdir(parents=True, exist_ok=True)
            
            # التقاط لقطة عند 10% من مدة الفيديو
            timestamp = min(duration * 0.1, 10)  # كحد أقصى 10 ثواني
            
            thumbnail_filename = f"{hashlib.md5(str(video_path).encode()).hexdigest()}.jpg"
            thumbnail_path = thumbnail_dir / thumbnail_filename
            
            if thumbnail_path.exists():
                return str(thumbnail_path)
            
            # استخدام ffmpeg لتوليد thumbnail
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-ss', str(timestamp),
                '-vframes', '1',
                '-vf', 'scale=320:-1',
                '-y', str(thumbnail_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and thumbnail_path.exists():
                return str(thumbnail_path)
            
        except Exception as e:
            logger.debug(f"Failed to generate thumbnail for {video_path}: {e}")
        
        return None
    
    def _generate_file_id(self, file_path: Path) -> str:
        """إنشاء معرف فريد للملف"""
        return hashlib.md5(str(file_path.resolve()).encode()).hexdigest()
    
    def start_monitoring(self):
        """بدء مراقبة التغييرات"""
        if not self.scan_paths:
            logger.warning("No scan paths configured")
            return
        
        self.handler = MediaFileHandler(self)
        self.observer = Observer()
        
        for path in self.scan_paths:
            self.observer.schedule(self.handler, path, recursive=True)
        
        self.observer.start()
        logger.info(f"Started monitoring {len(self.scan_paths)} paths")
    
    def stop_monitoring(self):
        """إيقاف مراقبة التغييرات"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped monitoring")
    
    def _on_file_created(self, file_path: str):
        """عند إنشاء ملف جديد"""
        path = Path(file_path)
        asyncio.create_task(self._process_file_async(path))
        logger.debug(f"File created: {file_path}")
    
    def _on_file_modified(self, file_path: str):
        """عند تعديل ملف"""
        logger.debug(f"File modified: {file_path}")
        # إعادة معالجة الملف
        path = Path(file_path)
        asyncio.create_task(self._process_file_async(path))
    
    def _on_file_deleted(self, file_path: str):
        """عند حذف ملف"""
        file_id = self._generate_file_id(Path(file_path))
        if file_id in self.media_library:
            del self.media_library[file_id]
            logger.debug(f"File deleted from library: {file_path}")
    
    def _remove_media_from_path(self, path: str):
        """إزالة جميع الوسائط من مسار"""
        to_remove = [
            file_id for file_id, media in self.media_library.items()
            if media['path'].startswith(path)
        ]
        
        for file_id in to_remove:
            del self.media_library[file_id]
        
        logger.info(f"Removed {len(to_remove)} media items from {path}")
    
    def get_media_by_type(self, media_type: str) -> List[Dict[str, Any]]:
        """الحصول على الوسائط حسب النوع"""
        return [
            media for media in self.media_library.values()
            if media['type'] == media_type
        ]
    
    def get_media_by_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        """الحصول على الوسائط من مجلد معين"""
        return [
            media for media in self.media_library.values()
            if media['path'].startswith(folder_path)
        ]
    
    def search_media(self, query: str) -> List[Dict[str, Any]]:
        """البحث في الوسائط"""
        query_lower = query.lower()
        results = []
        
        for media in self.media_library.values():
            if (query_lower in media['name'].lower() or
                query_lower in media.get('title', '').lower() or
                query_lower in media.get('artist', '').lower() or
                query_lower in media.get('album', '').lower()):
                results.append(media)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المكتبة"""
        total_size = sum(media['size'] for media in self.media_library.values())
        
        return {
            'total_items': len(self.media_library),
            'video_count': self.video_count,
            'audio_count': self.audio_count,
            'image_count': self.image_count,
            'total_size_bytes': total_size,
            'total_size_gb': round(total_size / (1024 ** 3), 2),
            'scan_paths': self.scan_paths,
            'monitoring_active': self.observer is not None and self.observer.is_alive()
        }
    
    def export_library(self, output_path: str):
        """تصدير المكتبة إلى ملف JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'exported_at': datetime.now().isoformat(),
                    'statistics': self.get_statistics(),
                    'media': list(self.media_library.values())
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Library exported to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to export library: {e}")
    
    def import_library(self, input_path: str):
        """استيراد مكتبة من ملف JSON"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.media_library = {item['id']: item for item in data.get('media', [])}
            
            # إعادة حساب العدادات
            self.video_count = sum(1 for m in self.media_library.values() if m['type'] == 'video')
            self.audio_count = sum(1 for m in self.media_library.values() if m['type'] == 'audio')
            self.image_count = sum(1 for m in self.media_library.values() if m['type'] == 'image')
            
            logger.info(f"Library imported from {input_path}")
            
        except Exception as e:
            logger.error(f"Failed to import library: {e}")
