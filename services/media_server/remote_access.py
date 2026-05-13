"""
Finovate StreamX AI - Remote Access Manager
الوصول عن بُعد للخادم

المطور: Ahmed Mostafa Ibrahim
Finovate – AHMED EG
"""

import logging
from typing import Dict, Any, Optional
import ssl
from pathlib import Path

logger = logging.getLogger(__name__)


class RemoteAccessManager:
    """
    إدارة الوصول عن بُعد
    
    الميزات:
    - HTTPS support
    - Authentication
    - Port forwarding
    - Dynamic DNS
    """
    
    def __init__(self):
        self.enabled = False
        self.port = 8443
        self.ssl_cert: Optional[Path] = None
        self.ssl_key: Optional[Path] = None
        self.authenticated_users: Dict[str, Any] = {}
    
    def enable_remote_access(self, port: int = 8443, ssl_cert: str = None, ssl_key: str = None):
        """تفعيل الوصول عن بُعد"""
        self.enabled = True
        self.port = port
        
        if ssl_cert and ssl_key:
            self.ssl_cert = Path(ssl_cert)
            self.ssl_key = Path(ssl_key)
        
        logger.info(f"Remote access enabled on port {port}")
    
    def disable_remote_access(self):
        """تعطيل الوصول عن بُعد"""
        self.enabled = False
        logger.info("Remote access disabled")
    
    def add_user(self, username: str, password_hash: str, permissions: Dict[str, bool]):
        """إضافة مستخدم مصرح له"""
        self.authenticated_users[username] = {
            'password_hash': password_hash,
            'permissions': permissions
        }
        logger.info(f"Added user: {username}")
    
    def authenticate(self, username: str, password_hash: str) -> bool:
        """مصادقة مستخدم"""
        if username in self.authenticated_users:
            return self.authenticated_users[username]['password_hash'] == password_hash
        return False
    
    def get_ssl_context(self) -> Optional[ssl.SSLContext]:
        """الحصول على سياق SSL"""
        if self.ssl_cert and self.ssl_key and self.ssl_cert.exists() and self.ssl_key.exists():
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(str(self.ssl_cert), str(self.ssl_key))
            return context
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة الوصول عن بُعد"""
        return {
            'enabled': self.enabled,
            'port': self.port,
            'ssl_configured': self.ssl_cert is not None,
            'user_count': len(self.authenticated_users)
        }
