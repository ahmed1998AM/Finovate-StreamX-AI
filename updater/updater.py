"""
Updater Module
================
Automatic update system for the application.
"""

import asyncio
import aiohttp
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from core.config import get_config
from core.logger import get_logger


class Updater:
    """Application update manager."""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self.github_api = "https://api.github.com/repos/ahmed1998AM/finovate-streamx-ai"
        self.current_version = self.config.VERSION
    
    async def check_for_updates(self) -> Dict[str, Any]:
        """Check for available updates."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.github_api}/releases/latest",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        latest_version = data.get("tag_name", "").lstrip("v")
                        
                        return {
                            "available": self._compare_versions(latest_version, self.current_version),
                            "latest_version": latest_version,
                            "current_version": self.current_version,
                            "download_url": data.get("assets", [{}])[0].get("browser_download_url"),
                            "release_notes": data.get("body", ""),
                            "published_at": data.get("published_at")
                        }
        except Exception as e:
            self.logger.error(f"Update check failed: {e}")
            return {"available": False, "error": str(e)}
        
        return {"available": False}
    
    def _compare_versions(self, latest: str, current: str) -> bool:
        """Compare version strings."""
        try:
            latest_parts = [int(x) for x in latest.split(".")]
            current_parts = [int(x) for x in current.split(".")]
            
            for l, c in zip(latest_parts, current_parts):
                if l > c:
                    return True
                elif l < c:
                    return False
            
            return len(latest_parts) > len(current_parts)
        except:
            return False
    
    async def download_update(self, download_url: str, dest_path: Path) -> bool:
        """Download update file."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status == 200:
                        with open(dest_path, 'wb') as f:
                            f.write(await response.read())
                        return True
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
        
        return False
    
    def install_update(self, installer_path: Path) -> bool:
        """Install downloaded update."""
        # Implementation depends on platform
        # Windows: Run installer with /SILENT flag
        # TODO: Implement proper installation logic
        return True


async def auto_update_check():
    """Periodic update check task."""
    updater = Updater()
    config = get_config()
    
    while True:
        await asyncio.sleep(config.UPDATE_CHECK_INTERVAL_HOURS * 3600)
        
        if config.ENABLE_AUTO_UPDATE:
            result = await updater.check_for_updates()
            if result.get("available"):
                get_logger().info(f"Update available: {result['latest_version']}")
                # TODO: Show notification to user
