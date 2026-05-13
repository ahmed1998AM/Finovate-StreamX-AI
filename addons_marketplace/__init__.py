"""
Finovate StreamX AI - Addons Marketplace System
Addon Management, Sandbox Execution, Version Control
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import os
import json
import asyncio
import importlib.util
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import zipfile
import shutil

logger = logging.getLogger(__name__)


@dataclass
class Addon:
    """Addon metadata"""
    id: str
    name: str
    version: str
    description: str
    author: str
    category: str
    enabled: bool
    installed: bool
    path: str
    manifest_path: str
    dependencies: List[str]
    permissions: List[str]
    rating: float
    downloads: int
    last_updated: str
    icon_path: Optional[str] = None


class AddonManager:
    """Manage addon lifecycle: install, enable, disable, update, uninstall"""
    
    def __init__(self, addons_dir: str = None):
        self.addons_dir = Path(addons_dir) if addons_dir else Path.home() / "StreamX_Addons"
        self.addons_dir.mkdir(exist_ok=True)
        
        # Subdirectories
        (self.addons_dir / "installed").mkdir(exist_ok=True)
        (self.addons_dir / "downloads").mkdir(exist_ok=True)
        (self.addons_dir / "sandbox").mkdir(exist_ok=True)
        
        self.installed_addons: Dict[str, Addon] = {}
        self.available_addons: Dict[str, dict] = {}
        self.active_addons: Dict[str, Any] = {}
        
        self.marketplace_url = "https://api.streamx.finovate.eg/addons"
        self.sandbox_enabled = True
        self.auto_update = False
        
        # Load installed addons
        self._load_installed_addons()
    
    def _load_installed_addons(self):
        """Load all installed addons from disk"""
        installed_dir = self.addons_dir / "installed"
        
        for addon_folder in installed_dir.iterdir():
            if not addon_folder.is_dir():
                continue
            
            manifest_path = addon_folder / "manifest.json"
            if not manifest_path.exists():
                continue
            
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                
                addon = Addon(
                    id=manifest.get('id', addon_folder.name),
                    name=manifest.get('name', 'Unknown'),
                    version=manifest.get('version', '0.0.0'),
                    description=manifest.get('description', ''),
                    author=manifest.get('author', 'Unknown'),
                    category=manifest.get('category', 'general'),
                    enabled=manifest.get('enabled', False),
                    installed=True,
                    path=str(addon_folder),
                    manifest_path=str(manifest_path),
                    dependencies=manifest.get('dependencies', []),
                    permissions=manifest.get('permissions', []),
                    rating=manifest.get('rating', 0.0),
                    downloads=manifest.get('downloads', 0),
                    last_updated=manifest.get('last_updated', ''),
                    icon_path=str(addon_folder / manifest.get('icon', 'icon.png'))
                )
                
                self.installed_addons[addon.id] = addon
                
                # Auto-enable if marked as enabled
                if addon.enabled:
                    self.enable_addon(addon.id)
                    
            except Exception as e:
                logger.error(f"Failed to load addon {addon_folder.name}: {e}")
        
        logger.info(f"Loaded {len(self.installed_addons)} installed addons")
    
    async def fetch_marketplace_addons(self) -> List[dict]:
        """Fetch available addons from marketplace"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.marketplace_url}/list") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.available_addons = {addon['id']: addon for addon in data.get('addons', [])}
                        return list(self.available_addons.values())
        except Exception as e:
            logger.warning(f"Failed to fetch marketplace: {e}")
        
        # Return demo addons if marketplace unavailable
        self.available_addons = self._get_demo_addons()
        return list(self.available_addons.values())
    
    def _get_demo_addons(self) -> Dict[str, dict]:
        """Return demo addons for testing"""
        return {
            'youtube_plugin': {
                'id': 'youtube_plugin',
                'name': 'YouTube Plugin',
                'version': '1.2.0',
                'description': 'Watch YouTube videos directly in StreamX',
                'author': 'StreamX Team',
                'category': 'video',
                'rating': 4.8,
                'downloads': 15420,
                'last_updated': '2025-01-15'
            },
            'subtitles_downloader': {
                'id': 'subtitles_downloader',
                'name': 'Subtitles Downloader',
                'version': '2.0.1',
                'description': 'Auto-download subtitles from OpenSubtitles',
                'author': 'Community',
                'category': 'utility',
                'rating': 4.6,
                'downloads': 8930,
                'last_updated': '2025-01-10'
            },
            'theme_dark_neon': {
                'id': 'theme_dark_neon',
                'name': 'Dark Neon Theme',
                'version': '1.0.0',
                'description': 'Beautiful dark neon theme with animations',
                'author': 'Design Team',
                'category': 'theme',
                'rating': 4.9,
                'downloads': 22100,
                'last_updated': '2025-01-12'
            }
        }
    
    async def install_addon(self, addon_id: str, version: str = None) -> bool:
        """Install an addon from marketplace"""
        if addon_id not in self.available_addons:
            logger.error(f"Addon {addon_id} not found in marketplace")
            return False
        
        addon_info = self.available_addons[addon_id]
        
        if version is None:
            version = addon_info['version']
        
        try:
            import aiohttp
            
            # Download addon package
            async with aiohttp.ClientSession() as session:
                download_url = f"{self.marketplace_url}/download/{addon_id}/{version}"
                
                async with session.get(download_url) as response:
                    if response.status != 200:
                        raise Exception(f"Download failed: {response.status}")
                    
                    # Save to downloads folder
                    download_path = self.addons_dir / "downloads" / f"{addon_id}.zip"
                    download_path.parent.mkdir(exist_ok=True)
                    
                    with open(download_path, 'wb') as f:
                        f.write(await response.read())
                    
                    # Extract addon
                    extract_path = self.addons_dir / "installed" / addon_id
                    extract_path.mkdir(exist_ok=True)
                    
                    with zipfile.ZipFile(download_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    
                    # Clean up download
                    download_path.unlink()
                    
                    # Update installed addons
                    self._load_installed_addons()
                    
                    logger.info(f"Installed addon: {addon_id} v{version}")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to install addon {addon_id}: {e}")
            return False
    
    def install_addon_local(self, addon_path: str) -> bool:
        """Install addon from local file"""
        path = Path(addon_path)
        
        if not path.exists():
            logger.error(f"Addon path does not exist: {addon_path}")
            return False
        
        try:
            addon_id = path.stem
            
            # If it's a zip file, extract it
            if path.suffix == '.zip':
                extract_path = self.addons_dir / "installed" / addon_id
                extract_path.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
            else:
                # Assume it's a directory
                dest_path = self.addons_dir / "installed" / addon_id
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.copytree(path, dest_path)
            
            # Update installed addons
            self._load_installed_addons()
            
            logger.info(f"Installed local addon: {addon_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to install local addon: {e}")
            return False
    
    def enable_addon(self, addon_id: str) -> bool:
        """Enable an installed addon"""
        if addon_id not in self.installed_addons:
            logger.error(f"Addon {addon_id} not installed")
            return False
        
        addon = self.installed_addons[addon_id]
        
        try:
            # Load addon module
            addon_path = Path(addon.path)
            main_file = addon_path / "main.py"
            
            if not main_file.exists():
                logger.error(f"Main file not found in addon {addon_id}")
                return False
            
            # Create sandbox or load normally
            if self.sandbox_enabled:
                addon_module = self._load_addon_sandbox(main_file, addon_id)
            else:
                addon_module = self._load_addon_normal(main_file, addon_id)
            
            # Initialize addon
            if hasattr(addon_module, 'init'):
                addon_module.init()
            
            # Store reference
            self.active_addons[addon_id] = addon_module
            
            # Update manifest
            manifest_path = Path(addon.manifest_path)
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            manifest['enabled'] = True
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
            
            addon.enabled = True
            logger.info(f"Enabled addon: {addon_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable addon {addon_id}: {e}")
            return False
    
    def disable_addon(self, addon_id: str) -> bool:
        """Disable an active addon"""
        if addon_id not in self.installed_addons:
            return False
        
        addon = self.installed_addons[addon_id]
        
        try:
            # Call cleanup if available
            if addon_id in self.active_addons:
                addon_module = self.active_addons[addon_id]
                if hasattr(addon_module, 'cleanup'):
                    addon_module.cleanup()
                
                del self.active_addons[addon_id]
            
            # Update manifest
            manifest_path = Path(addon.manifest_path)
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            manifest['enabled'] = False
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
            
            addon.enabled = False
            logger.info(f"Disabled addon: {addon_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable addon {addon_id}: {e}")
            return False
    
    def uninstall_addon(self, addon_id: str) -> bool:
        """Uninstall an addon completely"""
        if addon_id not in self.installed_addons:
            logger.error(f"Addon {addon_id} not installed")
            return False
        
        addon = self.installed_addons[addon_id]
        
        try:
            # Disable first if enabled
            if addon.enabled:
                self.disable_addon(addon_id)
            
            # Remove addon directory
            addon_path = Path(addon.path)
            if addon_path.exists():
                shutil.rmtree(addon_path)
            
            # Remove from registry
            del self.installed_addons[addon_id]
            
            logger.info(f"Uninstalled addon: {addon_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall addon {addon_id}: {e}")
            return False
    
    async def update_addon(self, addon_id: str) -> bool:
        """Update an addon to latest version"""
        if addon_id not in self.installed_addons:
            return False
        
        current_version = self.installed_addons[addon_id].version
        
        # Fetch latest version from marketplace
        await self.fetch_marketplace_addons()
        
        if addon_id not in self.available_addons:
            logger.error(f"Addon {addon_id} not found in marketplace")
            return False
        
        latest_version = self.available_addons[addon_id]['version']
        
        if current_version >= latest_version:
            logger.info(f"Addon {addon_id} is already up to date")
            return True
        
        # Uninstall old version
        was_enabled = self.installed_addons[addon_id].enabled
        self.uninstall_addon(addon_id)
        
        # Install new version
        success = await self.install_addon(addon_id, latest_version)
        
        # Re-enable if was enabled before
        if success and was_enabled:
            self.enable_addon(addon_id)
        
        return success
    
    async def update_all_addons(self) -> Dict[str, bool]:
        """Update all installed addons"""
        results = {}
        
        for addon_id in list(self.installed_addons.keys()):
            results[addon_id] = await self.update_addon(addon_id)
            await asyncio.sleep(1)  # Rate limiting
        
        return results
    
    def _load_addon_normal(self, main_file: Path, addon_id: str) -> Any:
        """Load addon module normally"""
        spec = importlib.util.spec_from_file_location(f"addon_{addon_id}", main_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def _load_addon_sandbox(self, main_file: Path, addon_id: str) -> Any:
        """Load addon module in sandboxed environment"""
        # Create restricted environment
        sandbox_globals = {
            '__builtins__': __builtins__.copy(),
            '__name__': f'addon_{addon_id}',
            '__file__': str(main_file)
        }
        
        # Remove dangerous builtins
        dangerous = ['eval', 'exec', 'compile', 'open', 'import', '__import__']
        for builtin in dangerous:
            if builtin in sandbox_globals['__builtins__']:
                del sandbox_globals['__builtins__'][builtin]
        
        # Execute addon code
        with open(main_file, 'r', encoding='utf-8') as f:
            code = compile(f.read(), str(main_file), 'exec')
        
        exec(code, sandbox_globals)
        
        # Create module-like object
        class SandboxModule:
            def __init__(self, globals_dict):
                self.__dict__.update(globals_dict)
            
            def __getattr__(self, name):
                return self.__dict__.get(name)
        
        return SandboxModule(sandbox_globals)
    
    def get_installed_addons(self, category: str = None) -> List[Addon]:
        """Get list of installed addons"""
        addons = list(self.installed_addons.values())
        
        if category:
            addons = [a for a in addons if a.category == category]
        
        return addons
    
    def get_active_addons(self) -> List[str]:
        """Get list of active addon IDs"""
        return list(self.active_addons.keys())
    
    def get_addon_stats(self) -> Dict:
        """Get addon statistics"""
        return {
            'total_installed': len(self.installed_addons),
            'total_active': len(self.active_addons),
            'total_available': len(self.available_addons),
            'categories': self._get_category_counts(),
            'total_downloads': sum(a.downloads for a in self.installed_addons.values()),
            'average_rating': sum(a.rating for a in self.installed_addons.values()) / max(len(self.installed_addons), 1)
        }
    
    def _get_category_counts(self) -> Dict[str, int]:
        """Get count of addons per category"""
        counts = {}
        for addon in self.installed_addons.values():
            counts[addon.category] = counts.get(addon.category, 0) + 1
        return counts
    
    def search_addons(self, query: str) -> List[dict]:
        """Search addons in marketplace"""
        results = []
        query_lower = query.lower()
        
        for addon_id, addon in self.available_addons.items():
            if (query_lower in addon.get('name', '').lower() or
                query_lower in addon.get('description', '').lower() or
                query_lower in addon.get('author', '').lower()):
                results.append(addon)
        
        return results


# Example usage
if __name__ == "__main__":
    manager = AddonManager()
    
    print(f"Addon stats: {manager.get_addon_stats()}")
    print(f"Installed addons: {[a.name for a in manager.get_installed_addons()]}")
