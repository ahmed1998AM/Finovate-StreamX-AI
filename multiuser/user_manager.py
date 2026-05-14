"""
Finovate StreamX AI - User Management System
نظام إدارة المستخدمين
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import asyncio
import hashlib
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import json


class UserRole(Enum):
    """أدوار المستخدمين"""
    ADMIN = "admin"
    PREMIUM = "premium"
    STANDARD = "standard"
    GUEST = "guest"
    KIDS = "kids"


@dataclass
class UserProfile:
    """ملف تعريف المستخدم"""
    user_id: str
    username: str
    email: str
    role: UserRole
    avatar: str = ""
    language: str = "ar"
    theme: str = "dark_elegant"
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    watch_history: List[str] = field(default_factory=list)
    favorites: List[str] = field(default_factory=list)
    parental_controls: bool = False
    max_stream_quality: str = "4K"
    allowed_categories: List[str] = field(default_factory=lambda: ["all"])
    watch_time_limit: int = 0  # بالدقائق، 0 = غير محدود


@dataclass
class User:
    """كائن المستخدم"""
    profile: UserProfile
    password_hash: str
    is_active: bool = True
    is_online: bool = False
    current_session: Optional[str] = None
    device_limit: int = 3
    concurrent_streams: int = 2


class UserManager:
    """مدير نظام المستخدمين المتعدد"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, str] = {}  # session_id -> user_id
        self._lock = asyncio.Lock()
        
    async def initialize(self):
        """تهيئة نظام المستخدمين"""
        # إنشاء مدير افتراضي
        admin_profile = UserProfile(
            user_id="admin_001",
            username="admin",
            email="admin@finovate.com",
            role=UserRole.ADMIN,
            allowed_categories=["all"],
            max_stream_quality="8K"
        )
        admin_user = User(
            profile=admin_profile,
            password_hash=self._hash_password("admin123"),
            device_limit=10,
            concurrent_streams=5
        )
        self.users["admin_001"] = admin_user
        print("✅ تم تهيئة نظام المستخدمين")
        
    def _hash_password(self, password: str) -> str:
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        role: UserRole = UserRole.STANDARD,
        **kwargs
    ) -> Optional[User]:
        """إنشاء مستخدم جديد"""
        async with self._lock:
            # التحقق من عدم وجود المستخدم
            for user in self.users.values():
                if user.profile.username == username or user.profile.email == email:
                    print(f"❌ المستخدم {username} موجود بالفعل")
                    return None
            
            user_id = f"user_{uuid.uuid4().hex[:8]}"
            profile = UserProfile(
                user_id=user_id,
                username=username,
                email=email,
                role=role,
                **kwargs
            )
            user = User(
                profile=profile,
                password_hash=self._hash_password(password)
            )
            self.users[user_id] = user
            print(f"✅ تم إنشاء المستخدم {username} بنجاح")
            return user
    
    async def authenticate(self, username: str, password: str) -> Optional[str]:
        """تسجيل الدخول"""
        async with self._lock:
            for user_id, user in self.users.items():
                if user.profile.username == username:
                    if not user.is_active:
                        print("❌ الحساب معطل")
                        return None
                    
                    if user.password_hash == self._hash_password(password):
                        # إنشاء جلسة
                        session_id = f"session_{uuid.uuid4().hex}"
                        self.sessions[session_id] = user_id
                        user.is_online = True
                        user.current_session = session_id
                        user.profile.last_login = datetime.now()
                        
                        print(f"✅ تم تسجيل دخول {username}")
                        return session_id
            
            print("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            return None
    
    async def logout(self, session_id: str) -> bool:
        """تسجيل الخروج"""
        async with self._lock:
            if session_id in self.sessions:
                user_id = self.sessions.pop(session_id)
                if user_id in self.users:
                    self.users[user_id].is_online = False
                    self.users[user_id].current_session = None
                    print(f"✅ تم تسجيل خروج المستخدم")
                    return True
            return False
    
    async def get_user_by_session(self, session_id: str) -> Optional[User]:
        """الحصول على بيانات المستخدم من الجلسة"""
        if session_id in self.sessions:
            user_id = self.sessions[session_id]
            return self.users.get(user_id)
        return None
    
    async def update_profile(self, user_id: str, **kwargs) -> bool:
        """تحديث ملف تعريف المستخدم"""
        if user_id in self.users:
            user = self.users[user_id]
            for key, value in kwargs.items():
                if hasattr(user.profile, key):
                    setattr(user.profile, key, value)
            print(f"✅ تم تحديث ملف المستخدم {user.profile.username}")
            return True
        return False
    
    async def add_to_watchlist(self, user_id: str, content_id: str) -> bool:
        """إضافة للمفضلة"""
        if user_id in self.users:
            if content_id not in self.users[user_id].profile.favorites:
                self.users[user_id].profile.favorites.append(content_id)
            return True
        return False
    
    async def add_to_history(self, user_id: str, content_id: str) -> bool:
        """إضافة لسجل المشاهدة"""
        if user_id in self.users:
            history = self.users[user_id].profile.watch_history
            if content_id in history:
                history.remove(content_id)
            history.insert(0, content_id)
            # الاحتفاظ بآخر 100 عنصر فقط
            if len(history) > 100:
                history = history[:100]
            return True
        return False
    
    async def get_all_users(self) -> List[Dict]:
        """الحصول على جميع المستخدمين"""
        return [
            {
                "user_id": user.profile.user_id,
                "username": user.profile.username,
                "email": user.profile.email,
                "role": user.profile.role.value,
                "is_active": user.is_active,
                "is_online": user.is_online,
                "last_login": user.profile.last_login.isoformat() if user.profile.last_login else None
            }
            for user in self.users.values()
        ]
    
    async def delete_user(self, user_id: str) -> bool:
        """حذف مستخدم"""
        if user_id in self.users and user_id != "admin_001":
            del self.users[user_id]
            # حذف الجلسات المرتبطة
            sessions_to_remove = [
                sid for sid, uid in self.sessions.items() if uid == user_id
            ]
            for sid in sessions_to_remove:
                del self.sessions[sid]
            print(f"✅ تم حذف المستخدم")
            return True
        return False
    
    async def get_statistics(self) -> Dict:
        """إحصائيات المستخدمين"""
        total = len(self.users)
        online = sum(1 for u in self.users.values() if u.is_online)
        by_role = {}
        for user in self.users.values():
            role = user.profile.role.value
            by_role[role] = by_role.get(role, 0) + 1
        
        return {
            "total_users": total,
            "online_users": online,
            "by_role": by_role,
            "active_sessions": len(self.sessions)
        }


# مثال للاستخدام
async def main():
    manager = UserManager()
    await manager.initialize()
    
    # إنشاء مستخدمين
    await manager.create_user("ahmed", "ahmed@example.com", "pass123", UserRole.PREMIUM)
    await manager.create_user("sara", "sara@example.com", "pass456", UserRole.KIDS, parental_controls=True)
    
    # تسجيل دخول
    session = await manager.authenticate("ahmed", "pass123")
    if session:
        user = await manager.get_user_by_session(session)
        print(f"مرحباً {user.profile.username}!")
        
        # إضافة للمفضلة
        await manager.add_to_watchlist(user.profile.user_id, "movie_123")
        
        # تسجيل خروج
        await manager.logout(session)
    
    # عرض الإحصائيات
    stats = await manager.get_statistics()
    print(f"\n📊 إحصائيات المستخدمين: {json.dumps(stats, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    asyncio.run(main())
