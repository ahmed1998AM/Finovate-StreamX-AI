"""
Finovate StreamX AI - Multi-User System
نظام تعدد المستخدمين والصلاحيات
المطور: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

from .user_manager import UserManager, User, UserRole, UserProfile
from .permissions import PermissionManager, Permission
from .session_manager import SessionManager
from .family_mode import FamilyMode, ContentRestriction

# Aliases for backward compatibility
Permissions = Permission

__version__ = "1.0.0"
__all__ = [
    "UserManager",
    "User",
    "UserRole",
    "UserProfile",
    "PermissionManager",
    "Permission",
    "Permissions",  # Alias
    "SessionManager",
    "FamilyMode",
    "ContentRestriction"
]
