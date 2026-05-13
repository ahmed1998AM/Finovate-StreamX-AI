"""
Cloud Sync Service Module
==========================
Synchronizes data with cloud providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp


class CloudProvider(ABC):
    """Abstract base class for cloud providers."""
    
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to cloud service."""
        pass
    
    @abstractmethod
    async def upload(self, key: str, data: bytes) -> bool:
        """Upload data to cloud."""
        pass
    
    @abstractmethod
    async def download(self, key: str) -> Optional[bytes]:
        """Download data from cloud."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete data from cloud."""
        pass
    
    @abstractmethod
    async def list_files(self, prefix: str = "") -> List[str]:
        """List files in cloud storage."""
        pass


class SupabaseProvider(CloudProvider):
    """Supabase cloud storage provider."""
    
    def __init__(self, api_key: str, project_url: str):
        self.api_key = api_key
        self.project_url = project_url
        self._session: Optional[aiohttp.ClientSession] = None
        self.connected = False
    
    async def connect(self) -> bool:
        """Connect to Supabase."""
        try:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "apikey": self.api_key,
                    "Content-Type": "application/json"
                }
            )
            
            # Test connection
            async with self._session.get(f"{self.project_url}/rest/v1/") as response:
                self.connected = response.status == 200
                return self.connected
        except Exception:
            return False
    
    async def upload(self, key: str, data: bytes) -> bool:
        """Upload to Supabase Storage."""
        if not self._session or not self.connected:
            return False
        
        try:
            # Convert to base64 for JSON storage
            import base64
            encoded = base64.b64encode(data).decode('utf-8')
            
            async with self._session.post(
                f"{self.project_url}/rest/v1/storage",
                json={"key": key, "data": encoded}
            ) as response:
                return response.status == 201
        except Exception:
            return False
    
    async def download(self, key: str) -> Optional[bytes]:
        """Download from Supabase Storage."""
        if not self._session or not self.connected:
            return None
        
        try:
            async with self._session.get(
                f"{self.project_url}/rest/v1/storage?key=eq.{key}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    import base64
                    return base64.b64decode(data[0]["data"])
        except Exception:
            pass
        
        return None
    
    async def delete(self, key: str) -> bool:
        """Delete from Supabase Storage."""
        if not self._session or not self.connected:
            return False
        
        try:
            async with self._session.delete(
                f"{self.project_url}/rest/v1/storage?key=eq.{key}"
            ) as response:
                return response.status == 204
        except Exception:
            return False
    
    async def list_files(self, prefix: str = "") -> List[str]:
        """List files in Supabase Storage."""
        if not self._session or not self.connected:
            return []
        
        try:
            url = f"{self.project_url}/rest/v1/storage"
            if prefix:
                url += f"?key=like.{prefix}%"
            
            async with self._session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [item["key"] for item in data]
        except Exception:
            pass
        
        return []
    
    async def close(self):
        """Close connection."""
        if self._session:
            await self._session.close()


class GoogleDriveProvider(CloudProvider):
    """Google Drive cloud storage provider."""
    
    def __init__(self, credentials: Dict[str, Any]):
        self.credentials = credentials
        self._service = None
        self.connected = False
    
    async def connect(self) -> bool:
        """Connect to Google Drive API."""
        try:
            # Lazy import to avoid dependency if not used
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            creds = service_account.Credentials.from_service_account_info(
                self.credentials,
                scopes=["https://www.googleapis.com/auth/drive.file"]
            )
            
            self._service = build("drive", "v3", credentials=creds)
            self.connected = True
            return True
        except Exception:
            return False
    
    async def upload(self, key: str, data: bytes) -> bool:
        """Upload to Google Drive."""
        if not self._service or not self.connected:
            return False
        
        try:
            from googleapiclient.http import MediaIoBaseUpload
            import io
            
            file_metadata = {"name": key}
            media = MediaIoBaseUpload(io.BytesIO(data), mimetype="application/octet-stream")
            
            self._service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()
            
            return True
        except Exception:
            return False
    
    async def download(self, key: str) -> Optional[bytes]:
        """Download from Google Drive."""
        if not self._service or not self.connected:
            return None
        
        try:
            # Find file by name
            results = self._service.files().list(
                q=f"name='{key}'",
                spaces="drive",
                fields="files(id)"
            ).execute()
            
            files = results.get("files", [])
            if files:
                request = self._service.files().get_media(fileId=files[0]["id"])
                
                import io
                from googleapiclient.http import MediaIoBaseDownload
                
                file_buffer = io.BytesIO()
                downloader = MediaIoBaseDownload(file_buffer, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                return file_buffer.getvalue()
        except Exception:
            pass
        
        return None
    
    async def delete(self, key: str) -> bool:
        """Delete from Google Drive."""
        if not self._service or not self.connected:
            return False
        
        try:
            results = self._service.files().list(
                q=f"name='{key}'",
                spaces="drive",
                fields="files(id)"
            ).execute()
            
            files = results.get("files", [])
            if files:
                self._service.files().delete(fileId=files[0]["id"]).execute()
                return True
        except Exception:
            pass
        
        return False
    
    async def list_files(self, prefix: str = "") -> List[str]:
        """List files in Google Drive."""
        if not self._service or not self.connected:
            return []
        
        try:
            query = f"name contains '{prefix}'" if prefix else ""
            results = self._service.files().list(
                q=query,
                spaces="drive",
                fields="files(name)"
            ).execute()
            
            return [f["name"] for f in results.get("files", [])]
        except Exception:
            return []


class CloudSyncService:
    """Main cloud synchronization service."""
    
    def __init__(self):
        self.provider: Optional[CloudProvider] = None
        self.provider_name: str = ""
        self.sync_enabled = False
    
    def setup_provider(self, provider_name: str, config: Dict[str, Any]) -> bool:
        """Setup cloud provider."""
        if provider_name == "supabase":
            self.provider = SupabaseProvider(
                api_key=config.get("api_key", ""),
                project_url=config.get("project_url", "")
            )
        elif provider_name == "google_drive":
            self.provider = GoogleDriveProvider(credentials=config)
        else:
            return False
        
        self.provider_name = provider_name
        return True
    
    async def connect(self) -> bool:
        """Connect to configured cloud provider."""
        if not self.provider:
            return False
        
        return await self.provider.connect()
    
    async def sync_settings(self, settings_data: bytes) -> bool:
        """Sync settings to cloud."""
        if not self.provider or not self.sync_enabled:
            return False
        
        return await self.provider.upload("settings.dat", settings_data)
    
    async def get_settings(self) -> Optional[bytes]:
        """Get settings from cloud."""
        if not self.provider or not self.sync_enabled:
            return None
        
        return await self.provider.download("settings.dat")
    
    async def sync_playlists(self, playlist_name: str, data: bytes) -> bool:
        """Sync playlist to cloud."""
        if not self.provider or not self.sync_enabled:
            return False
        
        return await self.provider.upload(f"playlists/{playlist_name}.m3u", data)
    
    async def get_playlist(self, playlist_name: str) -> Optional[bytes]:
        """Get playlist from cloud."""
        if not self.provider or not self.sync_enabled:
            return None
        
        return await self.provider.download(f"playlists/{playlist_name}.m3u")
    
    async def sync_watch_history(self, history_data: bytes) -> bool:
        """Sync watch history to cloud."""
        if not self.provider or not self.sync_enabled:
            return False
        
        return await self.provider.upload("history.dat", history_data)
    
    async def get_watch_history(self) -> Optional[bytes]:
        """Get watch history from cloud."""
        if not self.provider or not self.sync_enabled:
            return None
        
        return await self.provider.download("history.dat")
    
    async def list_synced_items(self) -> List[str]:
        """List all synced items."""
        if not self.provider:
            return []
        
        return await self.provider.list_files()
    
    async def disconnect(self):
        """Disconnect from cloud provider."""
        if self.provider and hasattr(self.provider, "close"):
            await self.provider.close()
        self.provider = None
        self.connected = False


# Global instance
_cloud_sync: Optional[CloudSyncService] = None


def get_cloud_sync() -> CloudSyncService:
    """Get global cloud sync instance."""
    global _cloud_sync
    if _cloud_sync is None:
        _cloud_sync = CloudSyncService()
    return _cloud_sync
