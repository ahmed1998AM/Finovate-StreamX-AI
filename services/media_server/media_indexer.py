"""
Finovate StreamX AI - Media Indexer
فهرسة الوسائط التلقائية

المطور: Ahmed Mostafa Ibrahim
Finovate – AHMED EG
"""

import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class MediaIndexer:
    """
    فهرسة الوسائط التلقائية
    
    الميزات:
    - Automatic media indexing
    - Metadata extraction
    - Category classification
    - Smart organization
    """
    
    def __init__(self):
        self.index: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, List[str]] = {
            'movies': [],
            'series': [],
            'documentaries': [],
            'music_videos': [],
            'home_videos': [],
            'other': []
        }
        self.last_index_time: Optional[datetime] = None
    
    async def index_media(self, media_items: List[Dict[str, Any]]):
        """فهرسة قائمة من الوسائط"""
        for item in media_items:
            await self._index_single_item(item)
        
        self.last_index_time = datetime.now()
        logger.info(f"Indexed {len(media_items)} media items")
    
    async def _index_single_item(self, item: Dict[str, Any]):
        """فهرسة عنصر واحد"""
        try:
            item_id = item.get('id')
            if not item_id:
                return
            
            # تصنيف العنصر
            category = self._classify_media(item)
            
            # استخراج معلومات إضافية
            enhanced_info = await self._extract_enhanced_info(item)
            
            self.index[item_id] = {
                **item,
                'category': category,
                'indexed_at': datetime.now().isoformat(),
                **enhanced_info
            }
            
            # إضافة للقائمة المناسبة
            if item_id not in self.categories[category]:
                self.categories[category].append(item_id)
            
        except Exception as e:
            logger.error(f"Error indexing item: {e}")
    
    def _classify_media(self, item: Dict[str, Any]) -> str:
        """تصنيف الوسائط"""
        name = item.get('name', '').lower()
        title = item.get('title', '').lower()
        path = item.get('path', '').lower()
        
        # التحقق من الأفلام
        if any(keyword in name or keyword in title for keyword in ['movie', 'film', 'cinema']):
            return 'movies'
        
        # التحقق من المسلسلات
        if any(keyword in name or keyword in title for keyword in ['series', 'episode', 'season', 's01', 's02']):
            return 'series'
        
        # التحقق من الوثائقيات
        if any(keyword in name or keyword in title for keyword in ['documentary', 'docu', 'nature', 'history']):
            return 'documentaries'
        
        # التحقق من فيديوهات الموسيقى
        if item.get('type') == 'audio' or 'music' in name or 'music' in title:
            return 'music_videos'
        
        # التحقق من الفيديوهات المنزلية
        if any(keyword in path for keyword in ['home', 'personal', 'family']):
            return 'home_videos'
        
        return 'other'
    
    async def _extract_enhanced_info(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """استخراج معلومات محسنة"""
        enhanced = {
            'tags': [],
            'language': None,
            'country': None,
            'rating': None,
            'description': None
        }
        
        # محاولة استخراج معلومات من الاسم
        name = item.get('name', '')
        
        # استخراج السنة من الاسم
        import re
        year_match = re.search(r'\b(19|20)\d{2}\b', name)
        if year_match:
            enhanced['year'] = int(year_match.group())
        
        # استخراج الدقة من الاسم
        resolution_patterns = ['4k', '1080p', '720p', '480p']
        for pattern in resolution_patterns:
            if pattern in name.lower():
                enhanced['resolution'] = pattern
                break
        
        return enhanced
    
    def search(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """البحث في الفهرس"""
        results = []
        query_lower = query.lower()
        
        for item_id, item in self.index.items():
            # تطبيق الفلاتر
            if filters:
                if 'category' in filters and item.get('category') != filters['category']:
                    continue
                if 'type' in filters and item.get('type') != filters['type']:
                    continue
            
            # البحث في الحقول
            searchable_fields = [
                item.get('name', ''),
                item.get('title', ''),
                item.get('description', ''),
                ' '.join(item.get('tags', []))
            ]
            
            if any(query_lower in field.lower() for field in searchable_fields):
                results.append(item)
        
        return results
    
    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """الحصول على عناصر حسب التصنيف"""
        item_ids = self.categories.get(category, [])
        return [self.index[item_id] for item_id in item_ids if item_id in self.index]
    
    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        """الحصول على العناصر الحديثة"""
        sorted_items = sorted(
            self.index.values(),
            key=lambda x: x.get('indexed_at', ''),
            reverse=True
        )
        return sorted_items[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الفهرس"""
        return {
            'total_items': len(self.index),
            'categories': {
                cat: len(items) for cat, items in self.categories.items()
            },
            'last_index_time': self.last_index_time.isoformat() if self.last_index_time else None
        }
    
    def export_index(self, output_path: str):
        """تصدير الفهرس"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'exported_at': datetime.now().isoformat(),
                    'statistics': self.get_statistics(),
                    'index': self.index
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Index exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export index: {e}")
    
    def import_index(self, input_path: str):
        """استيراد فهرس"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.index = data.get('index', {})
            
            # إعادة بناء التصنيفات
            self.categories = {cat: [] for cat in self.categories}
            for item_id, item in self.index.items():
                category = item.get('category', 'other')
                if category in self.categories:
                    self.categories[category].append(item_id)
            
            logger.info(f"Index imported from {input_path}")
        except Exception as e:
            logger.error(f"Failed to import index: {e}")
