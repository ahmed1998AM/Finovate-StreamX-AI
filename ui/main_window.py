"""
Main Window Module
===================
Primary application window with navigation and content management.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QToolBar, QToolButton, QLabel,
    QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QFont, QAction

from core.config import get_config, THEME_COLORS
from core.logger import get_logger


class NavigationBar(QToolBar):
    """Modern navigation bar with animated buttons."""
    
    page_changed = Signal(str)  # Emit page name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("navBar")
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))
        self.setFixedHeight(70)
        
        self.buttons = {}
        self.current_page = None
        
        self._setup_navigation()
    
    def _setup_navigation(self):
        """Setup navigation buttons."""
        pages = [
            ("home", "🏠", "Home"),
            ("live_tv", "📺", "Live TV"),
            ("movies", "🎬", "Movies"),
            ("series", "📀", "Series"),
            ("sports", "⚽", "Sports"),
            ("kids", "👶", "Kids"),
            ("favorites", "❤️", "Favorites"),
            ("history", "🕐", "History"),
            ("search", "🔍", "Search"),
            ("ai_assistant", "🤖", "AI Assistant"),
            ("settings", "⚙️", "Settings"),
            ("plugins", "🔌", "Plugins"),
        ]
        
        for page_id, icon, tooltip in pages:
            btn = QToolButton()
            btn.setText(f"{icon}\n{tooltip}")
            btn.setToolTip(tooltip)
            btn.setObjectName(f"navBtn_{page_id}")
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(lambda checked, pid=page_id: self._on_button_clicked(pid))
            
            self.addWidget(btn)
            self.buttons[page_id] = btn
        
        # Add spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)
    
    def _on_button_clicked(self, page_id: str):
        """Handle navigation button click."""
        if self.current_page:
            self.buttons[self.current_page].setChecked(False)
        
        self.current_page = page_id
        self.buttons[page_id].setChecked(True)
        self.page_changed.emit(page_id)
    
    def navigate_to(self, page_id: str):
        """Navigate to a specific page programmatically."""
        if page_id in self.buttons:
            self.buttons[page_id].click()


class ContentArea(QStackedWidget):
    """Main content area with page transitions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pages = {}
        self._setup_pages()
    
    def _setup_pages(self):
        """Initialize all content pages."""
        from ui.pages.home_page import HomePage
        from ui.pages.live_tv_page import LiveTVPage
        from ui.pages.movies_page import MoviesPage
        from ui.pages.series_page import SeriesPage
        from ui.pages.sports_page import SportsPage
        from ui.pages.kids_page import KidsPage
        from ui.pages.favorites_page import FavoritesPage
        from ui.pages.history_page import HistoryPage
        from ui.pages.search_page import SearchPage
        from ui.pages.ai_assistant_page import AIAssistantPage
        from ui.pages.settings_page import SettingsPage
        from ui.pages.plugins_page import PluginsPage
        
        # Create pages
        self.pages["home"] = HomePage()
        self.pages["live_tv"] = LiveTVPage()
        self.pages["movies"] = MoviesPage()
        self.pages["series"] = SeriesPage()
        self.pages["sports"] = SportsPage()
        self.pages["kids"] = KidsPage()
        self.pages["favorites"] = FavoritesPage()
        self.pages["history"] = HistoryPage()
        self.pages["search"] = SearchPage()
        self.pages["ai_assistant"] = AIAssistantPage()
        self.pages["settings"] = SettingsPage()
        self.pages["plugins"] = PluginsPage()
        
        # Add to stacked widget
        for page_name, page_widget in self.pages.items():
            self.addWidget(page_widget)
    
    def show_page(self, page_name: str):
        """Show a specific page by name."""
        if page_name in self.pages:
            index = list(self.pages.keys()).index(page_name)
            self.setCurrentIndex(index)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, db_manager=None):
        super().__init__()
        self.db_manager = db_manager
        self.config = get_config()
        self.logger = get_logger()
        
        self.setWindowTitle(f"{self.config.APP_NAME} v{self.config.VERSION}")
        self.setMinimumSize(1280, 720)
        self.resize(1400, 900)
        
        # Apply window flags for modern look
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowSystemMenuHint |
            Qt.WindowType.WindowMinMaxButtonsHint
        )
        
        # Setup UI
        self._setup_ui()
        self._apply_effects()
        
        self.logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Setup the main user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top bar
        top_bar = self._create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Content area
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Navigation bar (left sidebar)
        self.nav_bar = NavigationBar()
        self.nav_bar.setFixedWidth(120)
        self.nav_bar.setOrientation(Qt.Orientation.Vertical)
        content_layout.addWidget(self.nav_bar)
        
        # Main content
        self.content_area = ContentArea()
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.addWidget(self.content_area)
        
        main_layout.addWidget(content_frame)
        
        # Bottom status bar
        status_bar = self._create_status_bar()
        main_layout.addWidget(status_bar)
        
        # Connect signals
        self.nav_bar.page_changed.connect(self.content_area.show_page)
    
    def _create_top_bar(self) -> QWidget:
        """Create the top application bar."""
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(50)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(15, 5, 15, 5)
        
        # App logo/title
        title_label = QLabel(f"🎯 {self.config.APP_NAME}")
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # User profile / settings shortcut
        user_btn = QToolButton()
        user_btn.setText("👤 Profile")
        user_btn.setObjectName("userBtn")
        layout.addWidget(user_btn)
        
        # Minimize button
        min_btn = QToolButton()
        min_btn.setText("─")
        min_btn.setObjectName("windowBtn")
        min_btn.clicked.connect(self.showMinimized)
        layout.addWidget(min_btn)
        
        # Maximize/Restore button
        max_btn = QToolButton()
        max_btn.setText("◻")
        max_btn.setObjectName("windowBtn")
        max_btn.clicked.connect(self._toggle_maximize)
        layout.addWidget(max_btn)
        
        # Close button
        close_btn = QToolButton()
        close_btn.setText("✕")
        close_btn.setObjectName("closeBtn")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        return top_bar
    
    def _create_status_bar(self) -> QWidget:
        """Create custom status bar."""
        status_widget = QFrame()
        status_widget.setObjectName("statusBar")
        status_widget.setFixedHeight(30)
        
        layout = QHBoxLayout(status_widget)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Status info
        status_label = QLabel("✓ Ready")
        status_label.setObjectName("statusLabel")
        layout.addWidget(status_label)
        
        layout.addStretch()
        
        # Connection status
        connection_label = QLabel("🌐 Online")
        connection_label.setObjectName("connectionLabel")
        layout.addWidget(connection_label)
        
        # Version info
        version_label = QLabel(f"v{self.config.VERSION}")
        version_label.setObjectName("versionLabel")
        layout.addWidget(version_label)
        
        return status_widget
    
    def _apply_effects(self):
        """Apply visual effects to the window."""
        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(Qt.GlobalColor.black)
        self.setGraphicsEffect(shadow)
    
    def _toggle_maximize(self):
        """Toggle between maximized and normal state."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.logger.info("Application closing...")
        
        # Save settings, cleanup resources
        # TODO: Implement proper cleanup
        
        event.accept()
