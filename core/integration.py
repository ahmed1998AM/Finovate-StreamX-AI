"""
Finovate StreamX AI - Integration Core
نظام التكامل المركزي
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class IntegrationStatus(Enum):
    """حالة التكامل"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"


@dataclass
class IntegrationConfig:
    """إعدادات التكامل"""
    integration_id: str
    name: str
    type: str
    enabled: bool = True
    config: Dict = field(default_factory=dict)
    status: IntegrationStatus = IntegrationStatus.PENDING
    last_sync: Optional[datetime] = None
    error_message: str = ""


class IntegrationCore:
    """النواة المركزية لتكامل جميع أنظمة التطبيق"""
    
    def __init__(self):
        self.integrations: Dict[str, IntegrationConfig] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        self._tasks: List[asyncio.Task] = []
        
        # مراجع للأنظمة
        self.user_manager = None
        self.permission_manager = None
        self.session_manager = None
        self.family_mode = None
        self.marketplace = None
        self.tv_mode = None
        
        self._register_default_integrations()
    
    def _register_default_integrations(self):
        """تسجيل التكاملات الافتراضية"""
        integrations = [
            IntegrationConfig(
                integration_id="user_system",
                name="نظام المستخدمين",
                type="core",
                enabled=True
            ),
            IntegrationConfig(
                integration_id="permissions",
                name="نظام الصلاحيات",
                type="core",
                enabled=True
            ),
            IntegrationConfig(
                integration_id="sessions",
                name="إدارة الجلسات",
                type="core",
                enabled=True
            ),
            IntegrationConfig(
                integration_id="family_mode",
                name="وضع العائلة",
                type="feature",
                enabled=False
            ),
            IntegrationConfig(
                integration_id="marketplace",
                name="سوق الإضافات",
                type="feature",
                enabled=True
            ),
            IntegrationConfig(
                integration_id="android_tv",
                name="وضع التلفزيون",
                type="ui",
                enabled=False
            ),
            IntegrationConfig(
                integration_id="dvr_system",
                name="نظام التسجيل",
                type="feature",
                enabled=True
            ),
            IntegrationConfig(
                integration_id="torrent_streaming",
                name="بث التورنت",
                type="feature",
                enabled=False
            ),
            IntegrationConfig(
                integration_id="ai_assistant",
                name="مساعد الذكاء الاصطناعي",
                type="ai",
                enabled=True
            ),
            IntegrationConfig(
                integration_id="cloud_sync",
                name="المزامنة السحابية",
                type="service",
                enabled=False
            ),
            IntegrationConfig(
                integration_id="web_dashboard",
                name="لوحة التحكم الويب",
                type="ui",
                enabled=False
            ),
            IntegrationConfig(
                integration_id="rest_api",
                name="واجهة API",
                type="api",
                enabled=True
            ),
        ]
        
        for integration in integrations:
            self.integrations[integration.integration_id] = integration
    
    async def start(self):
        """بدء نظام التكامل"""
        if self.is_running:
            return
        
        self.is_running = True
        print("🚀 بدء نظام التكامل المركزي...")
        
        # بدء مهمة معالجة الأحداث
        task = asyncio.create_task(self._process_events())
        self._tasks.append(task)
        
        # تهيئة التكاملات المفعلة
        for int_id, config in self.integrations.items():
            if config.enabled:
                await self._initialize_integration(int_id)
        
        print("✅ نظام التكامل جاهز")
    
    async def stop(self):
        """إيقاف نظام التكامل"""
        self.is_running = False
        
        # إلغاء المهام
        for task in self._tasks:
            task.cancel()
        
        # إيقاف التكاملات
        for int_id in list(self.integrations.keys()):
            await self._shutdown_integration(int_id)
        
        print("✅ تم إيقاف نظام التكامل")
    
    async def _initialize_integration(self, integration_id: str):
        """تهيئة تكامل معين"""
        config = self.integrations.get(integration_id)
        if not config:
            return
        
        try:
            print(f"  📦 تهيئة: {config.name}...")
            
            # محاكاة التهيئة
            await asyncio.sleep(0.1)
            
            config.status = IntegrationStatus.ACTIVE
            config.last_sync = datetime.now()
            print(f"  ✅ {config.name}: جاهز")
            
        except Exception as e:
            config.status = IntegrationStatus.ERROR
            config.error_message = str(e)
            print(f"  ❌ {config.name}: خطأ - {e}")
    
    async def _shutdown_integration(self, integration_id: str):
        """إيقاف تكامل معين"""
        config = self.integrations.get(integration_id)
        if not config:
            return
        
        config.status = IntegrationStatus.INACTIVE
        print(f"  🛑 {config.name}: تم الإيقاف")
    
    async def _process_events(self):
        """معالجة قائمة الأحداث"""
        while self.is_running:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                await self._handle_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ خطأ في معالجة الحدث: {e}")
    
    async def _handle_event(self, event: Dict):
        """معالجة حدث معين"""
        event_type = event.get("type")
        data = event.get("data", {})
        
        if event_type == "user_login":
            await self._on_user_login(data)
        elif event_type == "user_logout":
            await self._on_user_logout(data)
        elif event_type == "content_played":
            await self._on_content_played(data)
        elif event_type == "plugin_installed":
            await self._on_plugin_installed(data)
        elif event_type == "settings_changed":
            await self._on_settings_changed(data)
    
    async def _on_user_login(self, data: Dict):
        """عند تسجيل دخول مستخدم"""
        user_id = data.get("user_id")
        print(f"🔐 حدث: تسجيل دخول المستخدم {user_id}")
    
    async def _on_user_logout(self, data: Dict):
        """عند تسجيل خروج مستخدم"""
        user_id = data.get("user_id")
        print(f"🔓 حدث: تسجيل خروج المستخدم {user_id}")
    
    async def _on_content_played(self, data: Dict):
        """عند تشغيل محتوى"""
        user_id = data.get("user_id")
        content_id = data.get("content_id")
        content_type = data.get("content_type")
        
        print(f"▶️ حدث: تشغيل {content_type} ({content_id}) للمستخدم {user_id}")
    
    async def _on_plugin_installed(self, data: Dict):
        """عند تثبيت إضافة"""
        plugin_id = data.get("plugin_id")
        print(f"📦 حدث: تثبيت الإضافة {plugin_id}")
    
    async def _on_settings_changed(self, data: Dict):
        """عند تغيير الإعدادات"""
        setting_key = data.get("key")
        setting_value = data.get("value")
        print(f"⚙️ حدث: تغيير الإعداد {setting_key} = {setting_value}")
    
    def emit_event(self, event_type: str, data: Dict):
        """إصدار حدث"""
        event = {"type": event_type, "data": data}
        asyncio.create_task(self.event_queue.put(event))
    
    def register_system(self, system_name: str, system_instance: Any):
        """تسجيل نظام للتكامل"""
        if system_name == "user_manager":
            self.user_manager = system_instance
        elif system_name == "permission_manager":
            self.permission_manager = system_instance
        elif system_name == "session_manager":
            self.session_manager = system_instance
        elif system_name == "family_mode":
            self.family_mode = system_instance
        elif system_name == "marketplace":
            self.marketplace = system_instance
        elif system_name == "tv_mode":
            self.tv_mode = system_instance
        
        print(f"✅ تم تسجيل النظام: {system_name}")
    
    def get_integration_status(self, integration_id: str) -> Optional[IntegrationConfig]:
        """الحصول على حالة تكامل"""
        return self.integrations.get(integration_id)
    
    async def enable_integration(self, integration_id: str) -> bool:
        """تفعيل تكامل"""
        if integration_id in self.integrations:
            config = self.integrations[integration_id]
            config.enabled = True
            await self._initialize_integration(integration_id)
            return True
        return False
    
    async def disable_integration(self, integration_id: str) -> bool:
        """تعطيل تكامل"""
        if integration_id in self.integrations:
            config = self.integrations[integration_id]
            config.enabled = False
            await self._shutdown_integration(integration_id)
            return True
        return False
    
    async def get_statistics(self) -> Dict:
        """إحصائيات نظام التكامل"""
        total = len(self.integrations)
        enabled = sum(1 for i in self.integrations.values() if i.enabled)
        active = sum(1 for i in self.integrations.values() if i.status == IntegrationStatus.ACTIVE)
        errors = sum(1 for i in self.integrations.values() if i.status == IntegrationStatus.ERROR)
        
        by_type = {}
        for integration in self.integrations.values():
            t = integration.type
            by_type[t] = by_type.get(t, 0) + 1
        
        return {
            "total_integrations": total,
            "enabled": enabled,
            "active": active,
            "errors": errors,
            "by_type": by_type,
            "event_queue_size": self.event_queue.qsize()
        }
    
    def get_health_report(self) -> Dict:
        """تقرير صحة النظام"""
        healthy = []
        warnings = []
        critical = []
        
        for int_id, config in self.integrations.items():
            if config.status == IntegrationStatus.ACTIVE:
                healthy.append(int_id)
            elif config.status == IntegrationStatus.ERROR:
                critical.append({
                    "id": int_id,
                    "name": config.name,
                    "error": config.error_message
                })
            elif not config.enabled:
                warnings.append({
                    "id": int_id,
                    "name": config.name,
                    "reason": "معطل"
                })
        
        overall_status = "healthy"
        if critical:
            overall_status = "critical"
        elif warnings:
            overall_status = "warning"
        
        return {
            "overall_status": overall_status,
            "healthy_count": len(healthy),
            "warnings_count": len(warnings),
            "critical_count": len(critical),
            "healthy": healthy,
            "warnings": warnings,
            "critical": critical,
            "timestamp": datetime.now().isoformat()
        }


# مثال للاستخدام
async def main():
    core = IntegrationCore()
    
    print("🔧 نظام التكامل المركزي\n")
    
    # عرض التكاملات المسجلة
    print("📋 التكاملات المسجلة:")
    for int_id, config in core.integrations.items():
        status_icon = "🟢" if config.enabled else "⚪"
        print(f"  {status_icon} {config.name} ({config.type})")
    
    # بدء النظام
    print("\n\n🚀 بدء النظام...")
    await core.start()
    
    # إصدار أحداث اختبارية
    print("\n\n📡 اختبار الأحداث:")
    core.emit_event("user_login", {"user_id": "user_123", "username": "ahmed"})
    await asyncio.sleep(0.5)
    
    core.emit_event("content_played", {
        "user_id": "user_123",
        "content_id": "movie_456",
        "content_type": "movie"
    })
    await asyncio.sleep(0.5)
    
    # الإحصائيات
    print("\n\n📊 إحصائيات النظام:")
    stats = await core.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # تقرير الصحة
    print("\n\n💚 تقرير الصحة:")
    health = core.get_health_report()
    print(f"  الحالة العامة: {health['overall_status']}")
    print(f"  سليم: {health['healthy_count']}")
    print(f"  تحذيرات: {health['warnings_count']}")
    print(f"  حرجة: {health['critical_count']}")
    
    # إيقاف النظام
    print("\n\n🛑 إيقاف النظام...")
    await core.stop()


if __name__ == "__main__":
    asyncio.run(main())
