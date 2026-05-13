"""
Plugin Manager Module
=====================
Dynamic plugin discovery, loading, and management.
"""

import importlib.util
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Type
from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass
    
    @abstractmethod
    async def initialize(self):
        """Initialize plugin."""
        pass
    
    @abstractmethod
    async def shutdown(self):
        """Shutdown plugin."""
        pass
    
    def is_compatible(self, app_version: str) -> bool:
        """Check if plugin is compatible with app version."""
        return True


class PluginMetadata:
    """Plugin metadata container."""
    
    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        author: str = "",
        min_app_version: str = "1.0.0",
        max_app_version: str = "99.0.0",
        dependencies: List[str] = None,
        config_schema: Dict[str, Any] = None
    ):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.min_app_version = min_app_version
        self.max_app_version = max_app_version
        self.dependencies = dependencies or []
        self.config_schema = config_schema or {}


class PluginManager:
    """Manages plugin lifecycle and discovery."""
    
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_metadata: Dict[str, PluginMetadata] = {}
        self.enabled_plugins: set = set()
        
        # Ensure plugins directory exists
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
    
    def discover_plugins(self) -> List[Path]:
        """
        Discover available plugins in the plugins directory.
        
        Returns:
            List of plugin file paths
        """
        plugin_files = []
        
        for item in self.plugins_dir.iterdir():
            if item.is_file() and item.suffix == '.py':
                if item.name.startswith('plugin_') and not item.name.startswith('__'):
                    plugin_files.append(item)
            elif item.is_dir():
                # Check for package plugins
                init_file = item / '__init__.py'
                if init_file.exists():
                    plugin_files.append(init_file)
        
        return plugin_files
    
    def load_plugin(self, plugin_path: Path) -> Optional[Plugin]:
        """
        Load a single plugin from file.
        
        Args:
            plugin_path: Path to plugin file
            
        Returns:
            Loaded plugin instance or None
        """
        try:
            module_name = plugin_path.stem
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            
            if spec is None or spec.loader is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for plugin class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                if (isinstance(attr, type) and 
                    issubclass(attr, Plugin) and 
                    attr != Plugin):
                    
                    plugin_instance = attr()
                    self.plugins[plugin_instance.name] = plugin_instance
                    
                    return plugin_instance
            
            return None
            
        except Exception as e:
            print(f"Error loading plugin {plugin_path}: {e}")
            return None
    
    def load_all_plugins(self) -> int:
        """
        Load all discovered plugins.
        
        Returns:
            Number of successfully loaded plugins
        """
        plugin_files = self.discover_plugins()
        loaded_count = 0
        
        for plugin_file in plugin_files:
            plugin = self.load_plugin(plugin_file)
            if plugin:
                loaded_count += 1
        
        return loaded_count
    
    async def initialize_plugin(self, plugin_name: str) -> bool:
        """
        Initialize a specific plugin.
        
        Args:
            plugin_name: Name of plugin to initialize
            
        Returns:
            True if successful
        """
        if plugin_name not in self.plugins:
            return False
        
        try:
            await self.plugins[plugin_name].initialize()
            self.enabled_plugins.add(plugin_name)
            return True
        except Exception as e:
            print(f"Error initializing plugin {plugin_name}: {e}")
            return False
    
    async def initialize_all(self):
        """Initialize all loaded plugins."""
        for plugin_name in self.plugins:
            await self.initialize_plugin(plugin_name)
    
    async def shutdown_plugin(self, plugin_name: str) -> bool:
        """
        Shutdown a specific plugin.
        
        Args:
            plugin_name: Name of plugin to shutdown
            
        Returns:
            True if successful
        """
        if plugin_name not in self.plugins:
            return False
        
        try:
            await self.plugins[plugin_name].shutdown()
            self.enabled_plugins.discard(plugin_name)
            return True
        except Exception as e:
            print(f"Error shutting down plugin {plugin_name}: {e}")
            return False
    
    async def shutdown_all(self):
        """Shutdown all enabled plugins."""
        for plugin_name in list(self.enabled_plugins):
            await self.shutdown_plugin(plugin_name)
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def get_enabled_plugins(self) -> List[Plugin]:
        """Get list of enabled plugins."""
        return [self.plugins[name] for name in self.enabled_plugins if name in self.plugins]
    
    def is_plugin_enabled(self, name: str) -> bool:
        """Check if a plugin is enabled."""
        return name in self.enabled_plugins
    
    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin."""
        if name in self.plugins:
            self.enabled_plugins.add(name)
            return True
        return False
    
    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin."""
        if name in self.enabled_plugins:
            self.enabled_plugins.discard(name)
            return True
        return False
    
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin from memory."""
        if name in self.plugins:
            del self.plugins[name]
            self.enabled_plugins.discard(name)
            return True
        return False
    
    def get_plugin_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get information about a plugin."""
        plugin = self.get_plugin(name)
        if not plugin:
            return None
        
        return {
            "name": plugin.name,
            "version": plugin.version,
            "description": plugin.description,
            "enabled": name in self.enabled_plugins
        }
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all plugins with their info."""
        return [self.get_plugin_info(name) for name in self.plugins]
    
    def save_plugin_config(self, plugin_name: str, config: Dict[str, Any]):
        """Save plugin configuration."""
        config_file = self.plugins_dir / f"{plugin_name}_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Load plugin configuration."""
        config_file = self.plugins_dir / f"{plugin_name}_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        
        return {}


# Example plugin template
class ExamplePlugin(Plugin):
    """Example plugin implementation."""
    
    @property
    def name(self) -> str:
        return "Example Plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "An example plugin for StreamX"
    
    async def initialize(self):
        print(f"Initializing {self.name} v{self.version}")
    
    async def shutdown(self):
        print(f"Shutting down {self.name}")
