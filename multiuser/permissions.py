"""
Finovate StreamX AI - Permissions System
نظام الصلاحيات والتحكم في الوصول
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

from enum import Enum
from typing import Dict, List, Set
from dataclasses import dataclass, field


class PermissionType(Enum):
    """أنواع الصلاحيات"""
    # المشاهدة
    VIEW_LIVE_TV = "view_live_tv"
    VIEW_MOVIES = "view_movies"
    VIEW_SERIES = "view_series"
    VIEW_SPORTS = "view_sports"
    VIEW_KIDS = "view_kids"
    
    # المحتوى
    VIEW_ADULT = "view_adult"
    VIEW_PREMIUM = "view_premium"
    VIEW_4K = "view_4k"
    VIEW_8K = "view_8k"
    
    # التسجيل
    RECORD_DVR = "record_dvr"
    SCHEDULE_RECORDING = "schedule_recording"
    MANAGE_RECORDINGS = "manage_recordings"
    
    # التحميل
    DOWNLOAD_TORRENT = "download_torrent"
    STREAM_TORRENT = "stream_torrent"
    
    # الإدارة
    MANAGE_USERS = "manage_users"
    MANAGE_PLAYLISTS = "manage_playlists"
    MANAGE_SETTINGS = "manage_settings"
    MANAGE_PLUGINS = "manage_plugins"
    VIEW_ANALYTICS = "view_analytics"
    
    # الذكاء الاصطناعي
    USE_AI_ASSISTANT = "use_ai_assistant"
    USE_AI_AGENTS = "use_ai_agents"
    
    # المشاركة
    SHARE_CONTENT = "share_content"
    CREATE_PLAYLISTS = "create_playlists"


@dataclass
class Permission:
    """كائن الصلاحية"""
    name: str
    type: PermissionType
    description: str
    category: str = "general"
    

class PermissionManager:
    """مدير نظام الصلاحيات"""
    
    def __init__(self):
        self.permissions: Dict[str, Permission] = {}
        self.role_permissions: Dict[str, Set[str]] = {
            "guest": set(),
            "kids": set(),
            "standard": set(),
            "premium": set(),
            "admin": set()
        }
        self._initialize_permissions()
        self._initialize_role_permissions()
    
    def _initialize_permissions(self):
        """تهيئة جميع الصلاحيات"""
        permissions = [
            # المشاهدة الأساسية
            Permission("VIEW_LIVE_TV", PermissionType.VIEW_LIVE_TV, "مشاهدة القنوات المباشرة", "viewing"),
            Permission("VIEW_MOVIES", PermissionType.VIEW_MOVIES, "مشاهدة الأفلام", "viewing"),
            Permission("VIEW_SERIES", PermissionType.VIEW_SERIES, "مشاهدة المسلسلات", "viewing"),
            Permission("VIEW_SPORTS", PermissionType.VIEW_SPORTS, "مشاهدة الرياضة", "viewing"),
            Permission("VIEW_KIDS", PermissionType.VIEW_KIDS, "مشاهدة محتوى الأطفال", "viewing"),
            
            # المحتوى المتقدم
            Permission("VIEW_ADULT", PermissionType.VIEW_ADULT, "مشاهدة المحتوى البالغين", "content"),
            Permission("VIEW_PREMIUM", PermissionType.VIEW_PREMIUM, "مشاهدة المحتوى الممتاز", "content"),
            Permission("VIEW_4K", PermissionType.VIEW_4K, "مشاهدة بدقة 4K", "quality"),
            Permission("VIEW_8K", PermissionType.VIEW_8K, "مشاهدة بدقة 8K", "quality"),
            
            # التسجيل
            Permission("RECORD_DVR", PermissionType.RECORD_DVR, "تسجيل البرامج", "dvr"),
            Permission("SCHEDULE_RECORDING", PermissionType.SCHEDULE_RECORDING, "جدولة التسجيل", "dvr"),
            Permission("MANAGE_RECORDINGS", PermissionType.MANAGE_RECORDINGS, "إدارة التسجيلات", "dvr"),
            
            # التورنت
            Permission("DOWNLOAD_TORRENT", PermissionType.DOWNLOAD_TORRENT, "تحميل التورنت", "torrent"),
            Permission("STREAM_TORRENT", PermissionType.STREAM_TORRENT, "بث التورنت", "torrent"),
            
            # الإدارة
            Permission("MANAGE_USERS", PermissionType.MANAGE_USERS, "إدارة المستخدمين", "admin"),
            Permission("MANAGE_PLAYLISTS", PermissionType.MANAGE_PLAYLISTS, "إدارة قوائم التشغيل", "admin"),
            Permission("MANAGE_SETTINGS", PermissionType.MANAGE_SETTINGS, "إدارة الإعدادات", "admin"),
            Permission("MANAGE_PLUGINS", PermissionType.MANAGE_PLUGINS, "إدارة الإضافات", "admin"),
            Permission("VIEW_ANALYTICS", PermissionType.VIEW_ANALYTICS, "عرض التحليلات", "admin"),
            
            # الذكاء الاصطناعي
            Permission("USE_AI_ASSISTANT", PermissionType.USE_AI_ASSISTANT, "استخدام مساعد AI", "ai"),
            Permission("USE_AI_AGENTS", PermissionType.USE_AI_AGENTS, "استخدام وكلاء AI", "ai"),
            
            # المشاركة
            Permission("SHARE_CONTENT", PermissionType.SHARE_CONTENT, "مشاركة المحتوى", "social"),
            Permission("CREATE_PLAYLISTS", PermissionType.CREATE_PLAYLISTS, "إنشاء قوائم تشغيل", "social"),
        ]
        
        for perm in permissions:
            self.permissions[perm.name] = perm
    
    def _initialize_role_permissions(self):
        """تهيئة صلاحيات الأدوار"""
        # ضيف - صلاحيات محدودة جداً
        self.role_permissions["guest"] = {
            "VIEW_LIVE_TV",
            "VIEW_MOVIES",
            "VIEW_SERIES",
            "VIEW_KIDS",
        }
        
        # أطفال - محتوى آمن فقط
        self.role_permissions["kids"] = {
            "VIEW_KIDS",
            "USE_AI_ASSISTANT",
        }
        
        # مستخدم عادي
        self.role_permissions["standard"] = {
            *self.role_permissions["guest"],
            "VIEW_SPORTS",
            "VIEW_4K",
            "RECORD_DVR",
            "SCHEDULE_RECORDING",
            "USE_AI_ASSISTANT",
            "SHARE_CONTENT",
            "CREATE_PLAYLISTS",
        }
        
        # مستخدم مميز
        self.role_permissions["premium"] = {
            *self.role_permissions["standard"],
            "VIEW_PREMIUM",
            "VIEW_8K",
            "MANAGE_RECORDINGS",
            "DOWNLOAD_TORRENT",
            "STREAM_TORRENT",
            "USE_AI_AGENTS",
        }
        
        # مدير النظام
        self.role_permissions["admin"] = {
            *self.role_permissions["premium"],
            "VIEW_ADULT",
            "MANAGE_USERS",
            "MANAGE_PLAYLISTS",
            "MANAGE_SETTINGS",
            "MANAGE_PLUGINS",
            "VIEW_ANALYTICS",
        }
    
    def has_permission(self, role: str, permission_name: str) -> bool:
        """التحقق من وجود صلاحية"""
        if role not in self.role_permissions:
            return False
        return permission_name in self.role_permissions[role]
    
    def get_role_permissions(self, role: str) -> List[Permission]:
        """الحصول على صلاحيات دور معين"""
        if role not in self.role_permissions:
            return []
        
        perm_names = self.role_permissions[role]
        return [self.permissions[name] for name in perm_names if name in self.permissions]
    
    def add_permission_to_role(self, role: str, permission_name: str) -> bool:
        """إضافة صلاحية لدور"""
        if role in self.role_permissions and permission_name in self.permissions:
            self.role_permissions[role].add(permission_name)
            return True
        return False
    
    def remove_permission_from_role(self, role: str, permission_name: str) -> bool:
        """إزالة صلاحية من دور"""
        if role in self.role_permissions:
            self.role_permissions[role].discard(permission_name)
            return True
        return False
    
    def create_custom_role(self, role_name: str, base_role: str = "standard") -> bool:
        """إنشاء دور مخصص"""
        if role_name in self.role_permissions:
            return False
        
        if base_role not in self.role_permissions:
            return False
        
        # نسخ صلاحيات الدور الأساسي
        self.role_permissions[role_name] = self.role_permissions[base_role].copy()
        return True
    
    def get_permission_categories(self) -> Dict[str, List[Permission]]:
        """الحصول على الصلاحيات مصنفة"""
        categories = {}
        for perm in self.permissions.values():
            if perm.category not in categories:
                categories[perm.category] = []
            categories[perm.category].append(perm)
        return categories
    
    def check_access(self, role: str, resource_type: str) -> bool:
        """التحقق من الوصول لمورد معين"""
        mapping = {
            "live_tv": "VIEW_LIVE_TV",
            "movies": "VIEW_MOVIES",
            "series": "VIEW_SERIES",
            "sports": "VIEW_SPORTS",
            "kids": "VIEW_KIDS",
            "adult": "VIEW_ADULT",
            "premium": "VIEW_PREMIUM",
            "4k": "VIEW_4K",
            "8k": "VIEW_8K",
            "dvr": "RECORD_DVR",
            "torrent": "STREAM_TORRENT",
            "ai": "USE_AI_ASSISTANT",
            "admin": "MANAGE_SETTINGS",
        }
        
        permission = mapping.get(resource_type)
        if not permission:
            return True
        
        return self.has_permission(role, permission)


# مثال للاستخدام
def main():
    manager = PermissionManager()
    
    print("📋 صلاحيات الأدوار:\n")
    
    for role in ["guest", "kids", "standard", "premium", "admin"]:
        perms = manager.get_role_permissions(role)
        print(f"\n👤 {role.upper()} ({len(perms)} صلاحية):")
        for perm in perms[:5]:  # عرض أول 5 فقط
            print(f"  ✓ {perm.description}")
        if len(perms) > 5:
            print(f"  ... و{len(perms) - 5} أخرى")
    
    # التحقق من الوصول
    print("\n\n🔐 اختبار الوصول:")
    test_cases = [
        ("kids", "kids"),
        ("kids", "adult"),
        ("standard", "4k"),
        ("premium", "8k"),
        ("admin", "adult"),
    ]
    
    for role, resource in test_cases:
        access = manager.check_access(role, resource)
        status = "✅" if access else "❌"
        print(f"{status} {role} يمكنه الوصول لـ {resource}: {access}")


if __name__ == "__main__":
    main()
