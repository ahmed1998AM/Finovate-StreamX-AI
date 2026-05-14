"""
Finovate StreamX AI - Plugin Marketplace
سوق الإضافات والتوسعات
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import asyncio
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class PluginCategory(Enum):
    """فئات الإضافات"""
    CONTENT = "content"  # مصادر محتوى جديدة
    UI = "ui"  # تحسينات الواجهة
    TOOLS = "tools"  # أدوات مساعدة
    INTEGRATION = "integration"  # تكامل مع خدمات خارجية
    AI = "ai"  # إضافات الذكاء الاصطناعي
    SECURITY = "security"  # أمان وخصوصية
    PERFORMANCE = "performance"  # تحسينات الأداء
    OTHER = "other"


class PluginStatus(Enum):
    """حالة الإضافة"""
    AVAILABLE = "available"
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    UPDATE_AVAILABLE = "update_available"
    INCOMPATIBLE = "incompatible"


@dataclass
class PluginInfo:
    """معلومات الإضافة"""
    plugin_id: str
    name: str
    description: str
    version: str
    author: str
    category: PluginCategory
    status: PluginStatus = PluginStatus.AVAILABLE
    icon: str = ""
    website: str = ""
    min_app_version: str = "1.0.0"
    max_app_version: str = "99.0.0"
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    size_mb: float = 0.0
    downloads: int = 0
    rating: float = 0.0
    reviews_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_verified: bool = False
    is_premium: bool = False
    price_usd: float = 0.0


@dataclass
class InstalledPlugin:
    """إضافة مثبتة"""
    info: PluginInfo
    installed_at: datetime
    enabled: bool = True
    config: Dict = field(default_factory=dict)
    last_used: Optional[datetime] = None


class PluginMarketplace:
    """سوق الإضافات"""
    
    def __init__(self, cache_dir: str = "plugins_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # قاعدة بيانات الإضافات
        self.available_plugins: Dict[str, PluginInfo] = {}
        self.installed_plugins: Dict[str, InstalledPlugin] = {}
        
        # Hooks للإضافات
        self.hooks: Dict[str, List[Callable]] = {
            "on_startup": [],
            "on_shutdown": [],
            "on_content_load": [],
            "on_player_start": [],
            "on_player_stop": [],
            "on_search": [],
            "on_recommendation": [],
        }
        
        self._initialize_default_plugins()
    
    def _initialize_default_plugins(self):
        """تهيئة إضافات افتراضية"""
        default_plugins = [
            PluginInfo(
                plugin_id="iptv_arabic",
                name="Arabic IPTV Pack",
                description="حزمة قنوات عربية مجانية",
                version="2.1.0",
                author="Finovate Team",
                category=PluginCategory.CONTENT,
                icon="📺",
                downloads=15420,
                rating=4.8,
                reviews_count=342,
                is_verified=True,
                min_app_version="1.0.0"
            ),
            PluginInfo(
                plugin_id="sports_live",
                name="Live Sports HD",
                description="قنوات رياضية مباشرة بجودة عالية",
                version="1.5.2",
                author="SportsFan Pro",
                category=PluginCategory.CONTENT,
                icon="⚽",
                downloads=8930,
                rating=4.6,
                reviews_count=187,
                is_verified=True,
                is_premium=True,
                price_usd=4.99,
                min_app_version="1.0.0"
            ),
            PluginInfo(
                plugin_id="kids_safe",
                name="Kids Safe Filter",
                description="فلتر أمان متقدم لمحتوى الأطفال",
                version="3.0.1",
                author="SafeKids Org",
                category=PluginCategory.SECURITY,
                icon="🛡️",
                downloads=12500,
                rating=4.9,
                reviews_count=456,
                is_verified=True,
                min_app_version="1.0.0"
            ),
            PluginInfo(
                plugin_id="ai_subtitles",
                name="AI Subtitles Generator",
                description="توليد ترجمات تلقائية بالذكاء الاصطناعي",
                version="2.3.0",
                author="AI Labs",
                category=PluginCategory.AI,
                icon="🤖",
                downloads=6780,
                rating=4.7,
                reviews_count=234,
                is_verified=True,
                is_premium=True,
                price_usd=2.99,
                min_app_version="1.2.0"
            ),
            PluginInfo(
                plugin_id="theme_cyberpunk",
                name="Cyberpunk Theme Extended",
                description="ثيم Cyberpunk محسن مع تأثيرات إضافية",
                version="1.2.0",
                author="ThemeMaster",
                category=PluginCategory.UI,
                icon="🎨",
                downloads=4320,
                rating=4.5,
                reviews_count=98,
                is_verified=False,
                min_app_version="1.0.0"
            ),
            PluginInfo(
                plugin_id="realdebrid_integration",
                name="RealDebrid Integration",
                description="تكامل كامل مع RealDebrid للتحميل السريع",
                version="4.1.0",
                author="DebridPro",
                category=PluginCategory.INTEGRATION,
                icon="🚀",
                downloads=9870,
                rating=4.8,
                reviews_count=312,
                is_verified=True,
                is_premium=True,
                price_usd=0.0,  # مجاني لكن يحتاج حساب RealDebrid
                min_app_version="1.0.0"
            ),
            PluginInfo(
                plugin_id="performance_boost",
                name="Performance Booster",
                description="تحسين أداء التطبيق وتسريع التحميل",
                version="2.0.5",
                author="OptimizeTeam",
                category=PluginCategory.PERFORMANCE,
                icon="⚡",
                downloads=7650,
                rating=4.4,
                reviews_count=156,
                is_verified=True,
                min_app_version="1.0.0"
            ),
            PluginInfo(
                plugin_id="epg_enhanced",
                name="Enhanced EPG",
                description="دليل برامج إلكتروني محسن مع صور وفيديو",
                version="3.2.1",
                author="EPG Master",
                category=PluginCategory.TOOLS,
                icon="📅",
                downloads=5430,
                rating=4.6,
                reviews_count=178,
                is_verified=True,
                min_app_version="1.0.0"
            ),
        ]
        
        for plugin in default_plugins:
            self.available_plugins[plugin.plugin_id] = plugin
    
    async def search_plugins(
        self,
        query: str = "",
        category: Optional[PluginCategory] = None,
        is_premium: Optional[bool] = None,
        min_rating: float = 0.0,
        sort_by: str = "downloads"
    ) -> List[PluginInfo]:
        """البحث عن الإضافات"""
        results = []
        
        for plugin in self.available_plugins.values():
            # تطبيق الفلاتر
            if query and query.lower() not in plugin.name.lower() and query.lower() not in plugin.description.lower():
                continue
            
            if category and plugin.category != category:
                continue
            
            if is_premium is not None and plugin.is_premium != is_premium:
                continue
            
            if plugin.rating < min_rating:
                continue
            
            results.append(plugin)
        
        # الترتيب
        if sort_by == "downloads":
            results.sort(key=lambda p: p.downloads, reverse=True)
        elif sort_by == "rating":
            results.sort(key=lambda p: p.rating, reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda p: p.name)
        elif sort_by == "updated":
            results.sort(key=lambda p: p.updated_at, reverse=True)
        
        return results
    
    async def install_plugin(self, plugin_id: str) -> tuple[bool, str]:
        """تثبيت إضافة"""
        if plugin_id not in self.available_plugins:
            return False, "الإضافة غير موجودة"
        
        if plugin_id in self.installed_plugins:
            return False, "الإضافة مثبتة بالفعل"
        
        plugin_info = self.available_plugins[plugin_id]
        
        # التحقق من التوافق
        app_version = "1.0.0"  # يجب جلبها من الإعدادات
        if app_version < plugin_info.min_app_version:
            return False, f"الإضافة تتطلب إصدار {plugin_info.min_app_version} أو أحدث"
        
        if app_version > plugin_info.max_app_version:
            return False, f"الإضافة غير متوافقة مع الإصدار {app_version}"
        
        # التحقق من المتطلبات
        for dep in plugin_info.dependencies:
            if dep not in self.installed_plugins:
                return False, f"يتطلب تثبيت الإضافة {dep} أولاً"
        
        # التثبيت
        installed = InstalledPlugin(
            info=plugin_info,
            installed_at=datetime.now(),
            enabled=True
        )
        
        self.installed_plugins[plugin_id] = installed
        
        # تحديث الحالة
        plugin_info.status = PluginStatus.ENABLED
        
        print(f"✅ تم تثبيت الإضافة: {plugin_info.name}")
        return True, "تم التثبيت بنجاح"
    
    async def uninstall_plugin(self, plugin_id: str) -> tuple[bool, str]:
        """إزالة إضافة"""
        if plugin_id not in self.installed_plugins:
            return False, "الإضافة غير مثبتة"
        
        # التحقق من وجود إضافات تعتمد عليها
        dependent_plugins = []
        for pid, installed in self.installed_plugins.items():
            if plugin_id in installed.info.dependencies:
                dependent_plugins.append(pid)
        
        if dependent_plugins:
            return False, f"لا يمكن الإزالة: الإضافات التالية تعتمد عليها: {', '.join(dependent_plugins)}"
        
        del self.installed_plugins[plugin_id]
        
        # تحديث الحالة
        if plugin_id in self.available_plugins:
            self.available_plugins[plugin_id].status = PluginStatus.AVAILABLE
        
        print(f"✅ تم إزالة الإضافة: {plugin_id}")
        return True, "تمت الإزالة بنجاح"
    
    async def enable_plugin(self, plugin_id: str) -> tuple[bool, str]:
        """تفعيل إضافة"""
        if plugin_id not in self.installed_plugins:
            return False, "الإضافة غير مثبتة"
        
        self.installed_plugins[plugin_id].enabled = True
        self.installed_plugins[plugin_id].info.status = PluginStatus.ENABLED
        
        print(f"✅ تم تفعيل الإضافة: {plugin_id}")
        return True, "تم التفعيل"
    
    async def disable_plugin(self, plugin_id: str) -> tuple[bool, str]:
        """تعطيل إضافة"""
        if plugin_id not in self.installed_plugins:
            return False, "الإضافة غير مثبتة"
        
        self.installed_plugins[plugin_id].enabled = False
        self.installed_plugins[plugin_id].info.status = PluginStatus.DISABLED
        
        print(f"✅ تم تعطيل الإضافة: {plugin_id}")
        return True, "تم التعطيل"
    
    async def update_plugin(self, plugin_id: str) -> tuple[bool, str]:
        """تحديث إضافة"""
        if plugin_id not in self.installed_plugins:
            return False, "الإضافة غير مثبتة"
        
        if plugin_id not in self.available_plugins:
            return False, "لا يتوفر تحديث"
        
        installed = self.installed_plugins[plugin_id]
        available = self.available_plugins[plugin_id]
        
        if installed.info.version >= available.version:
            return False, "الإضافة محدثة لآخر إصدار"
        
        # محاكاة التحديث
        installed.info.version = available.version
        installed.info.updated_at = datetime.now()
        
        print(f"✅ تم تحديث الإضافة: {plugin_id} إلى الإصدار {available.version}")
        return True, "تم التحديث"
    
    async def check_updates(self) -> List[str]:
        """التحقق من التحديثات المتاحة"""
        updates = []
        
        for plugin_id, installed in self.installed_plugins.items():
            if plugin_id in self.available_plugins:
                available = self.available_plugins[plugin_id]
                if installed.info.version < available.version:
                    updates.append(plugin_id)
                    installed.info.status = PluginStatus.UPDATE_AVAILABLE
        
        return updates
    
    def register_hook(self, hook_name: str, callback: Callable):
        """تسجيل Hook للإضافات"""
        if hook_name in self.hooks:
            self.hooks[hook_name].append(callback)
    
    async def trigger_hook(self, hook_name: str, *args, **kwargs):
        """تشغيل Hook"""
        if hook_name not in self.hooks:
            return
        
        for callback in self.hooks[hook_name]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args, **kwargs)
                else:
                    callback(*args, **kwargs)
            except Exception as e:
                print(f"❌ خطأ في hook {hook_name}: {e}")
    
    def get_installed_plugins(self) -> List[InstalledPlugin]:
        """الحصول على الإضافات المثبتة"""
        return list(self.installed_plugins.values())
    
    def get_plugin_details(self, plugin_id: str) -> Optional[PluginInfo]:
        """الحصول على تفاصيل الإضافة"""
        return self.available_plugins.get(plugin_id)
    
    async def get_statistics(self) -> Dict:
        """إحصائيات السوق"""
        total_available = len(self.available_plugins)
        total_installed = len(self.installed_plugins)
        enabled = sum(1 for p in self.installed_plugins.values() if p.enabled)
        
        by_category = {}
        for plugin in self.available_plugins.values():
            cat = plugin.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        premium_count = sum(1 for p in self.available_plugins.values() if p.is_premium)
        verified_count = sum(1 for p in self.available_plugins.values() if p.is_verified)
        
        return {
            "total_available": total_available,
            "total_installed": total_installed,
            "enabled_plugins": enabled,
            "by_category": by_category,
            "premium_plugins": premium_count,
            "verified_plugins": verified_count,
            "total_downloads": sum(p.downloads for p in self.available_plugins.values()),
            "average_rating": sum(p.rating for p in self.available_plugins.values()) / total_available if total_available > 0 else 0
        }


# مثال للاستخدام
async def main():
    marketplace = PluginMarketplace()
    
    print("🏪 سوق الإضافات\n")
    
    # البحث عن الإضافات
    print("🔍 جميع الإضافات المتاحة:")
    plugins = await marketplace.search_plugins()
    for plugin in plugins[:5]:
        status_icon = "✅" if plugin.is_verified else "⚪"
        premium_icon = "💎" if plugin.is_premium else "🆓"
        print(f"  {status_icon} {plugin.icon} {plugin.name} {premium_icon}")
        print(f"     ⭐ {plugin.rating} ({plugin.reviews_count} مراجعة) | 📥 {plugin.downloads} تحميل")
    
    # تثبيت إضافة
    print("\n\n📦 تثبيت الإضافات:")
    success, msg = await marketplace.install_plugin("iptv_arabic")
    print(f"{msg}")
    
    success, msg = await marketplace.install_plugin("kids_safe")
    print(f"{msg}")
    
    # عرض الإضافات المثبتة
    print("\n\n📋 الإضافات المثبتة:")
    installed = marketplace.get_installed_plugins()
    for plugin in installed:
        status = "🟢" if plugin.enabled else "🔴"
        print(f"  {status} {plugin.info.name} (v{plugin.info.version})")
    
    # التحقق من التحديثات
    print("\n\n🔄 التحقق من التحديثات:")
    updates = await marketplace.check_updates()
    if updates:
        print(f"  يتوفر {len(updates)} تحديثات:")
        for plugin_id in updates:
            plugin = marketplace.get_plugin_details(plugin_id)
            print(f"    • {plugin.name}")
    else:
        print("  ✅ جميع الإضافات محدثة")
    
    # الإحصائيات
    print("\n\n📊 إحصائيات السوق:")
    stats = await marketplace.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
