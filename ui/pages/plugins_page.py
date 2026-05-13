"""
Plugins Page Module
====================
Plugin management and marketplace.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout, QPushButton, QScrollArea,
    QGroupBox, QListWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PluginsPage(QWidget):
    """Plugins page for managing extensions."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the Plugins page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        title = QLabel("🔌 Plugins & Extensions")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        # Top actions
        actions_frame = self._create_actions_bar()
        main_layout.addWidget(actions_frame)
        
        # Main content with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Installed plugins
        installed_section = self._create_installed_plugins()
        content_layout.addWidget(installed_section)
        
        # Available plugins marketplace
        marketplace_section = self._create_marketplace()
        content_layout.addWidget(marketplace_section)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def _create_actions_bar(self) -> QFrame:
        """Create actions toolbar."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        frame.setFixedHeight(50)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        layout.addWidget(refresh_btn)
        
        # Install from file
        install_btn = QPushButton("📥 Install Plugin")
        install_btn.setObjectName("primaryButton")
        layout.addWidget(install_btn)
        
        layout.addStretch()
        
        # Check for updates
        update_btn = QPushButton("⬆️ Check Updates")
        update_btn.setObjectName("accentButton")
        layout.addWidget(update_btn)
        
        return frame
    
    def _create_installed_plugins(self) -> QGroupBox:
        """Create installed plugins section."""
        group = QGroupBox("📦 Installed Plugins")
        group.setObjectName("installedGroup")
        
        layout = QGridLayout(group)
        layout.setSpacing(15)
        
        # Sample installed plugins
        plugins = [
            ("🎨 Theme Manager", "Custom themes support", True),
            ("📡 Provider Plugin", "Additional IPTV providers", True),
            ("🤖 AI Enhancer", "Advanced AI features", False),
            ("📊 Statistics", "Viewing analytics", True),
        ]
        
        for i, (name, desc, enabled) in enumerate(plugins):
            plugin_card = self._create_plugin_card(name, desc, enabled, is_installed=True)
            row = i // 2
            col = i % 2
            layout.addWidget(plugin_card, row, col)
        
        return group
    
    def _create_marketplace(self) -> QGroupBox:
        """Create plugin marketplace section."""
        group = QGroupBox("🏪 Plugin Marketplace")
        group.setObjectName("marketplaceGroup")
        
        layout = QGridLayout(group)
        layout.setSpacing(15)
        
        # Sample available plugins
        plugins = [
            ("🌍 Multi-Language", "Support for 50+ languages", "Free"),
            ("🎮 Gamepad Support", "Controller integration", "Free"),
            ("📱 Remote Control", "Mobile remote app", "Free"),
            ("☁️ Cloud Sync Pro", "Advanced cloud features", "Premium"),
            ("🔐 VPN Integration", "Built-in VPN support", "Premium"),
            ("📹 DVR Recording", "Record live TV", "Premium"),
        ]
        
        for i, (name, desc, price) in enumerate(plugins):
            plugin_card = self._create_plugin_card(name, desc, False, is_installed=False, price=price)
            row = i // 3
            col = i % 3
            layout.addWidget(plugin_card, row, col)
        
        return group
    
    def _create_plugin_card(self, name: str, description: str, enabled: bool, 
                           is_installed: bool = True, price: str = None) -> QFrame:
        """Create a plugin card widget."""
        card = QFrame()
        card.setObjectName("cardWidget")
        card.setFixedSize(280, 140)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Plugin name
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        layout.addWidget(name_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("secondaryLabel")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        if is_installed:
            # Toggle enable/disable
            toggle_btn = QPushButton("✅ Enabled" if enabled else "❌ Disabled")
            toggle_btn.setObjectName("accentButton" if enabled else "primaryButton")
            toggle_btn.setFixedHeight(30)
            btn_layout.addWidget(toggle_btn)
            
            # Uninstall
            uninstall_btn = QPushButton("🗑️ Uninstall")
            uninstall_btn.setFixedHeight(30)
            btn_layout.addWidget(uninstall_btn)
        else:
            # Install button
            install_btn = QPushButton(f"{'💰 ' + price if price else '📥'} Install")
            install_btn.setObjectName("primaryButton")
            install_btn.setFixedHeight(30)
            btn_layout.addWidget(install_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        return card
