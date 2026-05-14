"""
Finovate StreamX AI - Family Mode & Parental Controls
نظام الرقابة الأبوية ووضع العائلة
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import asyncio
from datetime import datetime, time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class ContentRating(Enum):
    """تصنيفات المحتوى العمري"""
    G = "G"  # عام
    PG = "PG"  # إرشاد أبوي
    PG_13 = "PG-13"  # فوق 13 سنة
    R = "R"  # مقيد
    NC_17 = "NC-17"  # فوق 17 فقط
    ADULT = "18+"  # بالغين


@dataclass
class ContentRestriction:
    """قيود المحتوى"""
    max_rating: ContentRating = ContentRating.PG
    blocked_categories: Set[str] = field(default_factory=set)
    allowed_categories: Set[str] = field(default_factory=lambda: {"all"})
    blocked_channels: Set[str] = field(default_factory=set)
    allowed_channels: Set[str] = field(default_factory=set)
    keywords_blocked: Set[str] = field(default_factory=set)
    
    # قيود الوقت
    watch_time_limit: int = 0  # دقائق يومياً، 0 = غير محدود
    bedtime_start: Optional[time] = None
    bedtime_end: Optional[time] = None
    
    # أيام الأسبوع المسموحة
    allowed_days: Set[int] = field(default_factory=lambda: {0, 1, 2, 3, 4, 5, 6})  # الاثنين-الأحد
    
    # قيود الجودة
    max_quality: str = "HD"  # SD, HD, FHD, 4K, 8K


@dataclass
class ChildProfile:
    """ملف طفل"""
    child_id: str
    name: str
    age: int
    birth_date: datetime
    avatar: str = ""
    restrictions: ContentRestriction = field(default_factory=ContentRestriction)
    pin_code: str = ""  # PIN لتجاوز القيود
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    total_watch_time: int = 0  # إجمالي وقت المشاهدة بالدقائق
    today_watch_time: int = 0  # وقت اليوم


class FamilyMode:
    """نظام وضع العائلة والرقابة الأبوية"""
    
    def __init__(self):
        self.children: Dict[str, ChildProfile] = {}
        self.parent_pin: str = ""
        self.is_family_mode_enabled: bool = False
        self.safe_search: bool = True
        self.hide_adult_content: bool = True
        self._watch_sessions: Dict[str, datetime] = {}  # child_id -> start_time
        
    def enable_family_mode(self, parent_pin: str):
        """تفعيل وضع العائلة"""
        self.parent_pin = parent_pin
        self.is_family_mode_enabled = True
        self.safe_search = True
        self.hide_adult_content = True
        print("✅ تم تفعيل وضع العائلة")
    
    def disable_family_mode(self, parent_pin: str) -> bool:
        """تعطيل وضع العائلة"""
        if parent_pin == self.parent_pin:
            self.is_family_mode_enabled = False
            print("✅ تم تعطيل وضع العائلة")
            return True
        print("❌ رمز PIN غير صحيح")
        return False
    
    def add_child(
        self,
        name: str,
        age: int,
        birth_date: datetime,
        custom_restrictions: Optional[ContentRestriction] = None
    ) -> ChildProfile:
        """إضافة طفل"""
        child_id = f"child_{len(self.children) + 1}"
        
        # إنشاء قيود افتراضية حسب العمر
        if custom_restrictions is None:
            restrictions = self._get_age_appropriate_restrictions(age)
        else:
            restrictions = custom_restrictions
        
        profile = ChildProfile(
            child_id=child_id,
            name=name,
            age=age,
            birth_date=birth_date,
            restrictions=restrictions
        )
        
        self.children[child_id] = profile
        print(f"✅ تمت إضافة الطفل {name} ({age} سنوات)")
        return profile
    
    def _get_age_appropriate_restrictions(self, age: int) -> ContentRestriction:
        """الحصول على قيود مناسبة للعمر"""
        if age < 5:
            return ContentRestriction(
                max_rating=ContentRating.G,
                allowed_categories={"kids", "educational", "cartoons"},
                max_quality="HD",
                watch_time_limit=60  # ساعة واحدة
            )
        elif age < 10:
            return ContentRestriction(
                max_rating=ContentRating.PG,
                allowed_categories={"kids", "educational", "cartoons", "family"},
                max_quality="FHD",
                watch_time_limit=120  # ساعتان
            )
        elif age < 13:
            return ContentRestriction(
                max_rating=ContentRating.PG,
                blocked_categories={"adult", "violence", "horror"},
                max_quality="FHD",
                watch_time_limit=180  # 3 ساعات
            )
        elif age < 16:
            return ContentRestriction(
                max_rating=ContentRating.PG_13,
                blocked_categories={"adult", "extreme_violence"},
                max_quality="4K",
                watch_time_limit=240  # 4 ساعات
            )
        else:
            return ContentRestriction(
                max_rating=ContentRating.R,
                blocked_categories={"adult"},
                max_quality="4K",
                watch_time_limit=300  # 5 ساعات
            )
    
    def can_access_content(
        self,
        child_id: str,
        content_rating: ContentRating,
        content_category: str,
        content_title: str = ""
    ) -> tuple[bool, str]:
        """التحقق مما إذا كان الطفل يمكنه الوصول للمحتوى"""
        if child_id not in self.children:
            return True, "ليس طفلاً"
        
        if not self.is_family_mode_enabled:
            return True, "وضع العائلة معطل"
        
        child = self.children[child_id]
        if not child.is_active:
            return False, "الملف غير نشط"
        
        restrictions = child.restrictions
        
        # التحقق من التصنيف العمري
        rating_order = [
            ContentRating.G,
            ContentRating.PG,
            ContentRating.PG_13,
            ContentRating.R,
            ContentRating.NC_17,
            ContentRating.ADULT
        ]
        
        try:
            max_rating_index = rating_order.index(restrictions.max_rating)
            content_rating_index = rating_order.index(content_rating)
            
            if content_rating_index > max_rating_index:
                return False, f"المحتوى يتجاوز التصنيف المسموح ({restrictions.max_rating.value})"
        except ValueError:
            pass
        
        # التحقق من الفئات المحظورة
        if content_category in restrictions.blocked_categories:
            return False, f"الفئة '{content_category}' محظورة"
        
        # التحقق من الفئات المسموحة (إذا لم تكن 'all')
        if "all" not in restrictions.allowed_categories:
            if content_category not in restrictions.allowed_categories:
                return False, f"الفئة '{content_category}' غير مسموحة"
        
        # التحقق من الكلمات المحظورة في العنوان
        for keyword in restrictions.keywords_blocked:
            if keyword.lower() in content_title.lower():
                return False, f"العنوان يحتوي على كلمة محظورة"
        
        # التحقق من وقت النوم
        now = datetime.now().time()
        if restrictions.bedtime_start and restrictions.bedtime_end:
            if self._is_in_bedtime(now, restrictions.bedtime_start, restrictions.bedtime_end):
                return False, "وقت النوم الحالي"
        
        # التحقق من اليوم المسموح
        current_day = datetime.now().weekday()
        if current_day not in restrictions.allowed_days:
            return False, "اليوم غير مسموح للمشاهدة"
        
        # التحقق من وقت المشاهدة
        if restrictions.watch_time_limit > 0:
            if child.today_watch_time >= restrictions.watch_time_limit:
                return False, f"تم تجاوز حد المشاهدة اليومي ({restrictions.watch_time_limit} دقيقة)"
        
        return True, "مسموح"
    
    def _is_in_bedtime(self, now: time, start: time, end: time) -> bool:
        """التحقق مما إذا كان الوقت الحالي هو وقت النوم"""
        if start <= end:
            return start <= now <= end
        else:
            # وقت النوم يمتد بعد منتصف الليل
            return now >= start or now <= end
    
    def start_watching(self, child_id: str) -> bool:
        """بدء جلسة مشاهدة"""
        if child_id in self.children:
            self._watch_sessions[child_id] = datetime.now()
            return True
        return False
    
    def stop_watching(self, child_id: str) -> int:
        """إيقاف جلسة المشاهدة وإرجاع المدة"""
        if child_id in self._watch_sessions:
            start_time = self._watch_sessions.pop(child_id)
            duration = int((datetime.now() - start_time).total_seconds() / 60)
            
            if child_id in self.children:
                child = self.children[child_id]
                child.total_watch_time += duration
                child.today_watch_time += duration
            
            return duration
        return 0
    
    def reset_daily_watch_time(self):
        """إعادة تعيين وقت المشاهدة اليومي"""
        today = datetime.now().date()
        for child in self.children.values():
            # إعادة التعيين فقط إذا كان يوم جديد
            last_reset = getattr(child, '_last_reset_date', None)
            if last_reset != today:
                child.today_watch_time = 0
                child._last_reset_date = today
    
    def override_restrictions(self, child_id: str, pin_code: str) -> bool:
        """تجاوز القيود باستخدام PIN"""
        if child_id in self.children:
            child = self.children[child_id]
            if pin_code == child.pin_code or pin_code == self.parent_pin:
                print(f"✅ تم تجاوز القيود للطفل {child.name}")
                return True
        print("❌ رمز PIN غير صحيح")
        return False
    
    def get_safe_content_list(self, content_list: List[Dict], child_id: str) -> List[Dict]:
        """تصفية قائمة المحتوى لتكون آمنة للطفل"""
        if not self.is_family_mode_enabled or child_id not in self.children:
            return content_list
        
        safe_content = []
        for content in content_list:
            can_access, _ = self.can_access_content(
                child_id,
                ContentRating(content.get("rating", "G")),
                content.get("category", "general"),
                content.get("title", "")
            )
            if can_access:
                safe_content.append(content)
        
        return safe_content
    
    def get_statistics(self) -> Dict:
        """إحصائيات وضع العائلة"""
        total_children = len(self.children)
        active_children = sum(1 for c in self.children.values() if c.is_active)
        currently_watching = len(self._watch_sessions)
        
        children_stats = []
        for child in self.children.values():
            children_stats.append({
                "name": child.name,
                "age": child.age,
                "total_watch_time": child.total_watch_time,
                "today_watch_time": child.today_watch_time,
                "limit": child.restrictions.watch_time_limit
            })
        
        return {
            "family_mode_enabled": self.is_family_mode_enabled,
            "total_children": total_children,
            "active_children": active_children,
            "currently_watching": currently_watching,
            "children": children_stats
        }
    
    def update_child_restrictions(
        self,
        child_id: str,
        parent_pin: str,
        **kwargs
    ) -> bool:
        """تحديث قيود الطفل"""
        if parent_pin != self.parent_pin:
            print("❌ رمز PIN الأب غير صحيح")
            return False
        
        if child_id in self.children:
            child = self.children[child_id]
            for key, value in kwargs.items():
                if hasattr(child.restrictions, key):
                    setattr(child.restrictions, key, value)
            print(f"✅ تم تحديث قيود {child.name}")
            return True
        return False


# مثال للاستخدام
def main():
    family = FamilyMode()
    
    # تفعيل وضع العائلة
    family.enable_family_mode(parent_pin="1234")
    
    # إضافة أطفال
    child1 = family.add_child("أحمد", 7, datetime(2017, 5, 15))
    child2 = family.add_child("فاطمة", 12, datetime(2012, 8, 20))
    child3 = family.add_child("محمد", 15, datetime(2009, 3, 10))
    
    print("\n👨‍👩‍👧‍👦 نظام العائلة:")
    print(f"عدد الأطفال: {len(family.children)}")
    
    # اختبار الوصول للمحتوى
    test_contents = [
        ("كرتون تعليمي", ContentRating.G, "kids"),
        ("فيلم عائلي", ContentRating.PG, "family"),
        ("فلم أكشن", ContentRating.PG_13, "action"),
        ("فيلم رعب", ContentRating.R, "horror"),
        ("محتوى بالغين", ContentRating.ADULT, "adult"),
    ]
    
    print("\n\n🔐 اختبار الوصول للمحتوى:")
    for title, rating, category in test_contents:
        can_access, reason = family.can_access_content(child1.child_id, rating, category, title)
        status = "✅" if can_access else "❌"
        print(f"{status} أحمد (7 سنوات) - {title}: {reason}")
    
    # بدء مشاهدة
    print("\n\n▶️ بدء المشاهدة:")
    family.start_watching(child1.child_id)
    
    # الإحصائيات
    stats = family.get_statistics()
    print(f"\n📊 إحصائيات العائلة:")
    for key, value in stats.items():
        if key != "children":
            print(f"  {key}: {value}")
    
    for child_stat in stats["children"]:
        print(f"\n  👶 {child_stat['name']} ({child_stat['age']} سنوات):")
        print(f"     وقت اليوم: {child_stat['today_watch_time']} / {child_stat['limit']} دقيقة")


if __name__ == "__main__":
    main()
