"""
Finovate StreamX AI - GitHub IPTV Libraries Manager
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
إدارة مكتبات IPTV من GitHub مع تحديث تلقائي
"""

import aiohttp
import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class GitHubLibrary:
    """تمثيل مكتبة GitHub"""
    name: str
    type: str
    language: List[str]
    github: str
    website: Optional[str] = None
    features: List[str] = None
    priority: str = "MEDIUM"
    recommended_usage: str = ""
    stars: int = 0
    last_updated: Optional[str] = None
    latest_release: Optional[str] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []


class GitHubIPTVManager:
    """مدير مكتبات IPTV من GitHub"""
    
    # قائمة المكتبات الموصى بها
    LIBRARIES = [
        {
            "name": "IPTVnator",
            "type": "Cross Platform IPTV Player",
            "language": ["TypeScript", "Angular", "Electron"],
            "github": "https://github.com/4gray/iptvnator",
            "website": "https://4gray.github.io/iptvnator/",
            "features": ["M3U/M3U8", "Xtream Codes", "Stalker Portal", "EPG XMLTV", 
                        "Favorites", "History", "Catchup TV", "Remote Control"],
            "priority": "HIGH",
            "recommended_usage": "Main IPTV core inspiration and feature reference"
        },
        {
            "name": "Megacubo",
            "type": "Advanced IPTV Streaming Platform",
            "language": ["JavaScript", "Node.js"],
            "github": "https://github.com/EdenwareApps/Megacubo",
            "features": ["M3U support", "EPG", "Bookmarks", "Mini player", 
                        "Live TV", "Streaming optimization", "Android TV support"],
            "priority": "HIGH",
            "recommended_usage": "Streaming optimization and IPTV architecture"
        },
        {
            "name": "QiTV",
            "type": "Python IPTV Client",
            "language": ["Python", "Qt", "VLC"],
            "github": "https://github.com/ozankaraali/QiTV",
            "features": ["Python based", "Qt interface", "LibVLC integration", 
                        "M3U playback", "STB support", "Portable mode"],
            "priority": "VERY_HIGH",
            "recommended_usage": "Main Python desktop IPTV architecture"
        },
        {
            "name": "Another IPTV Player",
            "type": "Flutter IPTV Player",
            "language": ["Flutter", "Dart"],
            "github": "https://github.com/bsogulcan/another-iptv-player",
            "features": ["Xtream Codes", "M3U", "Series support", 
                        "Movies support", "Search", "Favorites"],
            "priority": "MEDIUM",
            "recommended_usage": "UI inspiration and Xtream integration"
        },
        {
            "name": "python-vlc",
            "type": "Python VLC Bindings",
            "language": ["Python"],
            "github": "https://github.com/oaubert/python-vlc",
            "features": ["VLC bindings", "Media playback", "Hardware acceleration", 
                        "Network streams", "Subtitle support"],
            "priority": "CRITICAL",
            "recommended_usage": "Primary video engine"
        },
        {
            "name": "libmpv",
            "type": "MPV Video Engine",
            "language": ["C", "Python bindings available"],
            "github": "https://github.com/mpv-player/mpv",
            "features": ["GPU acceleration", "Low latency playback", 
                        "Advanced rendering", "Hardware decoding"],
            "priority": "CRITICAL",
            "recommended_usage": "Secondary playback engine"
        },
        {
            "name": "FFmpeg",
            "type": "Media Processing Framework",
            "language": ["C"],
            "github": "https://github.com/FFmpeg/FFmpeg",
            "features": ["Video decoding", "HLS", "DASH", "RTMP", 
                        "Transcoding", "Recording", "Media analysis"],
            "priority": "CRITICAL",
            "recommended_usage": "Media backend and stream processing"
        },
        {
            "name": "yt-dlp",
            "type": "Streaming Extraction Engine",
            "language": ["Python"],
            "github": "https://github.com/yt-dlp/yt-dlp",
            "features": ["Stream extraction", "Metadata fetching", 
                        "Live stream support", "Subtitle extraction"],
            "priority": "HIGH",
            "recommended_usage": "Online stream extraction"
        },
        {
            "name": "streamlink",
            "type": "CLI Streaming Engine",
            "language": ["Python"],
            "github": "https://github.com/streamlink/streamlink",
            "features": ["HTTP streams", "HLS", "Live streaming", "Plugin system"],
            "priority": "HIGH",
            "recommended_usage": "Stream routing and playback"
        },
        {
            "name": "iptv-org",
            "type": "Public IPTV Database",
            "language": ["JSON", "M3U"],
            "github": "https://github.com/iptv-org/iptv",
            "features": ["Global IPTV channels", "Country sorting", 
                        "Category sorting", "Public playlists"],
            "priority": "HIGH",
            "recommended_usage": "Testing and channel metadata"
        },
        {
            "name": "awesome-iptv",
            "type": "IPTV Resources Collection",
            "language": ["Markdown"],
            "github": "https://github.com/iptv-org/awesome-iptv",
            "features": ["IPTV tools", "EPG sources", 
                        "Player collections", "Streaming resources"],
            "priority": "HIGH",
            "recommended_usage": "Auto discovery of IPTV tools"
        },
        {
            "name": "iptv-checker",
            "type": "IPTV Health Monitor",
            "language": ["Python"],
            "github": "https://github.com/zhimin-dev/iptv-checker",
            "features": ["Dead stream detection", "Response testing", 
                        "Channel validation", "Speed testing"],
            "priority": "HIGH",
            "recommended_usage": "Automatic IPTV repair system"
        },
        {
            "name": "globetvapp-epg",
            "type": "Free EPG Database",
            "language": ["XMLTV"],
            "github": "https://github.com/globetvapp/epg",
            "features": ["Daily updated EPG", "Country based XMLTV", "Global support"],
            "priority": "HIGH",
            "recommended_usage": "Electronic Program Guide system"
        }
    ]
    
    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(__file__).parent.parent / "cache" / "github"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.libraries: List[GitHubLibrary] = []
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _parse_github_url(self, url: str) -> tuple:
        """تحليل URL GitHub لاستخراج owner و repo"""
        url = url.strip().rstrip('/')
        parts = url.split('github.com/')[-1].split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
        return None, None
    
    async def fetch_repo_info(self, library: GitHubLibrary) -> Dict:
        """جلب معلومات المستودع من GitHub API"""
        owner, repo = self._parse_github_url(library.github)
        if not owner or not repo:
            return {}
        
        try:
            async with self.session.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers={"Accept": "application/vnd.github.v3+json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "stars": data.get("stargazers_count", 0),
                        "forks": data.get("forks_count", 0),
                        "last_updated": data.get("updated_at"),
                        "latest_release": await self._get_latest_release(owner, repo),
                        "description": data.get("description", ""),
                        "language": data.get("language", ""),
                        "license": data.get("license", {}).get("name", "Unknown") if data.get("license") else "Unknown"
                    }
        except Exception as e:
            logger.error(f"Error fetching info for {library.name}: {e}")
        
        return {}
    
    async def _get_latest_release(self, owner: str, repo: str) -> Optional[str]:
        """الحصول على آخر إصدار"""
        try:
            async with self.session.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
                headers={"Accept": "application/vnd.github.v3+json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("tag_name") or data.get("name")
        except:
            pass
        return None
    
    async def load_libraries(self) -> List[GitHubLibrary]:
        """تحميل جميع المكتبات مع معلومات محدثة"""
        self.libraries = []
        
        for lib_data in self.LIBRARIES:
            library = GitHubLibrary(**lib_data)
            
            # محاولة جلب المعلومات المحدثة من GitHub
            if self.session:
                info = await self.fetch_repo_info(library)
                if info:
                    library.stars = info.get("stars", 0)
                    library.last_updated = info.get("last_updated")
                    library.latest_release = info.get("latest_release")
            
            self.libraries.append(library)
        
        # حفظ في الكاش
        await self._save_to_cache()
        
        logger.info(f"Loaded {len(self.libraries)} IPTV libraries from GitHub")
        return self.libraries
    
    async def _save_to_cache(self):
        """حفظ المكتبات في الكاش"""
        cache_file = self.cache_dir / "libraries.json"
        data = {
            "timestamp": datetime.now().isoformat(),
            "libraries": [asdict(lib) for lib in self.libraries]
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    async def load_from_cache(self) -> List[GitHubLibrary]:
        """تحميل المكتبات من الكاش"""
        cache_file = self.cache_dir / "libraries.json"
        
        if not cache_file.exists():
            return []
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # التحقق من صلاحية الكاش (24 ساعة)
            cache_time = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - cache_time > timedelta(hours=24):
                logger.info("Cache expired, will refresh")
                return []
            
            self.libraries = [GitHubLibrary(**lib) for lib in data["libraries"]]
            return self.libraries
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            return []
    
    def get_by_priority(self, priority: str) -> List[GitHubLibrary]:
        """الحصول على المكتبات حسب الأولوية"""
        return [lib for lib in self.libraries if lib.priority == priority.upper()]
    
    def get_critical_libraries(self) -> List[GitHubLibrary]:
        """الحصول على المكتبات الحرجة فقط"""
        return self.get_by_priority("CRITICAL")
    
    def get_high_priority_libraries(self) -> List[GitHubLibrary]:
        """الحصول على المكتبات عالية الأولوية"""
        return self.get_by_priority("HIGH")
    
    def search_by_feature(self, feature: str) -> List[GitHubLibrary]:
        """البحث عن مكتبات تحتوي على ميزة معينة"""
        feature_lower = feature.lower()
        return [
            lib for lib in self.libraries 
            if any(feature_lower in f.lower() for f in lib.features)
        ]
    
    def search_by_language(self, language: str) -> List[GitHubLibrary]:
        """البحث عن مكتبات بلغة معينة"""
        language_lower = language.lower()
        return [
            lib for lib in self.libraries 
            if any(language_lower in lang.lower() for lang in lib.language)
        ]
    
    async def check_updates(self) -> Dict[str, str]:
        """التحقق من وجود تحديثات للمكتبات"""
        updates = {}
        
        for library in self.libraries:
            owner, repo = self._parse_github_url(library.github)
            if not owner or not repo:
                continue
            
            current_version = library.latest_release
            latest_version = await self._get_latest_release(owner, repo)
            
            if latest_version and latest_version != current_version:
                updates[library.name] = {
                    "current": current_version,
                    "latest": latest_version,
                    "repo": library.github
                }
        
        return updates
    
    def export_to_json(self, filepath: Path = None) -> Path:
        """تصدير المكتبات إلى JSON"""
        filepath = filepath or self.cache_dir / "export.json"
        
        data = {
            "exported_at": datetime.now().isoformat(),
            "developer": "Ahmed Mostafa Ibrahim | Finovate – AHMED EG",
            "total_libraries": len(self.libraries),
            "libraries": [asdict(lib) for lib in self.libraries]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(self.libraries)} libraries to {filepath}")
        return filepath
    
    def get_integration_recommendations(self) -> Dict:
        """الحصول على توصيات التكامل"""
        return {
            "main_player_engine": next(
                (lib.github for lib in self.libraries if lib.name == "python-vlc"), 
                None
            ),
            "secondary_player_engine": next(
                (lib.github for lib in self.libraries if lib.name == "libmpv"), 
                None
            ),
            "media_backend": next(
                (lib.github for lib in self.libraries if lib.name == "FFmpeg"), 
                None
            ),
            "iptv_core_reference": next(
                (lib.github for lib in self.libraries if lib.name == "IPTVnator"), 
                None
            ),
            "python_architecture_reference": next(
                (lib.github for lib in self.libraries if lib.name == "QiTV"), 
                None
            ),
            "streaming_backend": next(
                (lib.github for lib in self.libraries if lib.name == "streamlink"), 
                None
            ),
            "iptv_testing_engine": next(
                (lib.github for lib in self.libraries if lib.name == "iptv-checker"), 
                None
            ),
            "epg_provider": next(
                (lib.github for lib in self.libraries if lib.name == "globetvapp-epg"), 
                None
            ),
            "channel_database": next(
                (lib.github for lib in self.libraries if lib.name == "iptv-org"), 
                None
            )
        }


async def main():
    """دالة رئيسية للاختبار"""
    async with GitHubIPTVManager() as manager:
        # تحميل المكتبات
        libraries = await manager.load_libraries()
        
        print(f"\n{'='*60}")
        print("Finovate StreamX AI - GitHub IPTV Libraries")
        print("المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG")
        print(f"{'='*60}\n")
        
        print(f"Total Libraries: {len(libraries)}\n")
        
        # عرض المكتبات الحرجة
        critical = manager.get_critical_libraries()
        print(f"\n🔴 CRITICAL Libraries ({len(critical)}):")
        for lib in critical:
            print(f"  • {lib.name} - {lib.type}")
            print(f"    Stars: {lib.stars:,} | Release: {lib.latest_release}")
        
        # عرض المكتبات عالية الأولوية
        high = manager.get_high_priority_libraries()
        print(f"\n🟠 HIGH Priority Libraries ({len(high)}):")
        for lib in high[:5]:  # أول 5 فقط
            print(f"  • {lib.name} - {lib.type}")
            print(f"    Features: {', '.join(lib.features[:3])}")
        
        # توصيات التكامل
        print(f"\n📋 Integration Recommendations:")
        recommendations = manager.get_integration_recommendations()
        for key, value in recommendations.items():
            print(f"  • {key}: {value}")
        
        # التحقق من التحديثات
        print(f"\n🔄 Checking for updates...")
        updates = await manager.check_updates()
        if updates:
            for name, info in updates.items():
                print(f"  • {name}: {info['current']} → {info['latest']}")
        else:
            print("  All libraries are up to date!")
        
        # تصدير
        export_path = manager.export_to_json()
        print(f"\n💾 Exported to: {export_path}")


if __name__ == "__main__":
    asyncio.run(main())
