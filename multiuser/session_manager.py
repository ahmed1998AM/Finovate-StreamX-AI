"""
Finovate StreamX AI - Session Manager
نظام إدارة الجلسات والأمان
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import json


@dataclass
class SessionInfo:
    """معلومات الجلسة"""
    session_id: str
    user_id: str
    device_id: str
    device_name: str
    device_type: str  # desktop, mobile, tablet, tv
    ip_address: str
    user_agent: str
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    is_active: bool = True


class SessionManager:
    """مدير جلسات المستخدمين"""
    
    def __init__(self, session_timeout_hours: int = 24):
        self.sessions: Dict[str, SessionInfo] = {}
        self.user_sessions: Dict[str, List[str]] = {}  # user_id -> [session_ids]
        self.session_timeout = timedelta(hours=session_timeout_hours)
        self._lock = asyncio.Lock()
        self._cleanup_task = None
    
    async def start_cleanup_task(self):
        """بدء مهمة التنظيف الدوري"""
        async def cleanup_loop():
            while True:
                await asyncio.sleep(3600)  # كل ساعة
                await self.cleanup_expired_sessions()
        
        self._cleanup_task = asyncio.create_task(cleanup_loop())
    
    async def create_session(
        self,
        user_id: str,
        device_id: str,
        device_name: str,
        device_type: str,
        ip_address: str,
        user_agent: str
    ) -> str:
        """إنشاء جلسة جديدة"""
        async with self._lock:
            session_id = f"sess_{uuid.uuid4().hex}"
            now = datetime.now()
            
            session = SessionInfo(
                session_id=session_id,
                user_id=user_id,
                device_id=device_id,
                device_name=device_name,
                device_type=device_type,
                ip_address=ip_address,
                user_agent=user_agent,
                created_at=now,
                last_activity=now,
                expires_at=now + self.session_timeout
            )
            
            self.sessions[session_id] = session
            
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = []
            self.user_sessions[user_id].append(session_id)
            
            print(f"✅ تم إنشاء جلسة جديدة لـ {user_id} على {device_name}")
            return session_id
    
    async def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """الحصول على معلومات الجلسة"""
        session = self.sessions.get(session_id)
        if session and session.is_active:
            # تحديث آخر نشاط
            session.last_activity = datetime.now()
            return session
        return None
    
    async def invalidate_session(self, session_id: str) -> bool:
        """إبطال جلسة"""
        async with self._lock:
            if session_id in self.sessions:
                self.sessions[session_id].is_active = False
                del self.sessions[session_id]
                
                # إزالة من قائمة جلسات المستخدم
                session = self.sessions.get(session_id)
                if session:
                    user_id = session.user_id
                    if user_id in self.user_sessions:
                        if session_id in self.user_sessions[user_id]:
                            self.user_sessions[user_id].remove(session_id)
                
                print(f"✅ تم إبطال الجلسة {session_id}")
                return True
            return False
    
    async def invalidate_all_user_sessions(self, user_id: str) -> int:
        """إبطال جميع جلسات المستخدم"""
        async with self._lock:
            count = 0
            if user_id in self.user_sessions:
                session_ids = self.user_sessions[user_id].copy()
                for session_id in session_ids:
                    if session_id in self.sessions:
                        self.sessions[session_id].is_active = False
                        del self.sessions[session_id]
                        count += 1
                self.user_sessions[user_id] = []
            
            print(f"✅ تم إبطال {count} جلسة للمستخدم {user_id}")
            return count
    
    async def cleanup_expired_sessions(self) -> int:
        """تنظيف الجلسات المنتهية"""
        async with self._lock:
            now = datetime.now()
            expired = [
                sid for sid, session in self.sessions.items()
                if session.expires_at < now or not session.is_active
            ]
            
            for session_id in expired:
                session = self.sessions[session_id]
                user_id = session.user_id
                
                del self.sessions[session_id]
                if user_id in self.user_sessions:
                    if session_id in self.user_sessions[user_id]:
                        self.user_sessions[user_id].remove(session_id)
            
            if expired:
                print(f"🧹 تم تنظيف {len(expired)} جلسة منتهية")
            
            return len(expired)
    
    async def get_user_sessions(self, user_id: str) -> List[SessionInfo]:
        """الحصول على جميع جلسات المستخدم"""
        if user_id not in self.user_sessions:
            return []
        
        sessions = []
        for session_id in self.user_sessions[user_id]:
            if session_id in self.sessions:
                sessions.append(self.sessions[session_id])
        
        return sessions
    
    async def get_active_sessions_count(self, user_id: str) -> int:
        """الحصول على عدد الجلسات النشطة"""
        sessions = await self.get_user_sessions(user_id)
        return sum(1 for s in sessions if s.is_active)
    
    async def update_activity(self, session_id: str) -> bool:
        """تحديث وقت النشاط الأخير"""
        if session_id in self.sessions:
            self.sessions[session_id].last_activity = datetime.now()
            # تمديد صلاحية الجلسة
            self.sessions[session_id].expires_at = datetime.now() + self.session_timeout
            return True
        return False
    
    async def get_statistics(self) -> Dict:
        """إحصائيات الجلسات"""
        now = datetime.now()
        total = len(self.sessions)
        active = sum(1 for s in self.sessions.values() if s.is_active)
        
        by_device = {}
        by_type = {}
        for session in self.sessions.values():
            if session.device_type not in by_type:
                by_type[session.device_type] = 0
            by_type[session.device_type] += 1
            
            if session.device_name not in by_device:
                by_device[session.device_name] = 0
            by_device[session.device_name] += 1
        
        return {
            "total_sessions": total,
            "active_sessions": active,
            "unique_users": len(self.user_sessions),
            "by_device_type": by_type,
            "by_device_name": by_device
        }
    
    async def kick_session(self, session_id: str, reason: str = "") -> bool:
        """طرد جلسة معينة"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            print(f"⚠️ تم طرد الجلسة من {session.device_name} ({session.ip_address})")
            if reason:
                print(f"   السبب: {reason}")
            return await self.invalidate_session(session_id)
        return False
    
    async def kick_all_other_sessions(self, user_id: str, keep_session_id: str) -> int:
        """طرد جميع الجلسات ما عدا واحدة"""
        sessions = await self.get_user_sessions(user_id)
        count = 0
        for session in sessions:
            if session.session_id != keep_session_id:
                await self.kick_session(session.session_id, "تم تسجيل الدخول من جهاز آخر")
                count += 1
        return count


# مثال للاستخدام
async def main():
    manager = SessionManager()
    
    # إنشاء جلسات
    session1 = await manager.create_session(
        user_id="user_123",
        device_id="dev_001",
        device_name="Chrome on Windows",
        device_type="desktop",
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0..."
    )
    
    session2 = await manager.create_session(
        user_id="user_123",
        device_id="dev_002",
        device_name="iPhone 14",
        device_type="mobile",
        ip_address="192.168.1.101",
        user_agent="Mozilla/5.0 (iPhone)..."
    )
    
    # عرض الجلسات
    sessions = await manager.get_user_sessions("user_123")
    print(f"\n📱 جلسات المستخدم ({len(sessions)}):")
    for sess in sessions:
        print(f"  • {sess.device_name} ({sess.device_type}) - {sess.ip_address}")
    
    # الإحصائيات
    stats = await manager.get_statistics()
    print(f"\n📊 إحصائيات الجلسات:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # طرد الجلسات الأخرى
    kicked = await manager.kick_all_other_sessions("user_123", session1)
    print(f"\n🚫 تم طرد {kicked} جلسة أخرى")


if __name__ == "__main__":
    asyncio.run(main())
