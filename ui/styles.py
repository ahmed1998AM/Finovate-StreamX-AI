"""
Stylesheet Module
=================
Advanced Cyberpunk Glassmorphism theme styles for PySide6 with multiple theme support.
"""

from core.config import THEME_COLORS, THEMES


def get_stylesheet(theme_name: str = "cyberpunk_neon") -> str:
    """
    Get the main application stylesheet with specified theme.
    
    Args:
        theme_name: Name of the theme to use
        
    Returns:
        Complete CSS stylesheet string
    """
    colors = THEMES.get(theme_name, THEMES["cyberpunk_neon"])
    
    return f"""
/* ============================================
   Finovate StreamX AI - {colors['name']} Theme
   Enhanced Cyberpunk Glassmorphism Design
   ============================================ */

/* Global Styles with Gradient Background */
QWidget {{
    background-color: {colors["background"]};
    color: {colors["text_primary"]};
    font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
    font-size: 14px;
}}

QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors["gradient_start"]},
        stop:1 {colors["gradient_end"]});
}}

/* Scrollbars - Modern Rounded Design */
QScrollBar:vertical {{
    background-color: {colors["cards"]};
    width: 12px;
    border-radius: 6px;
    margin: 0px;
    border: 1px solid {colors["primary"]};
}}

QScrollBar::handle:vertical {{
    background-color: {colors["primary"]};
    border-radius: 6px;
    min-height: 30px;
    border: 2px solid transparent;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors["accent"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {colors["cards"]};
    height: 12px;
    border-radius: 6px;
    margin: 0px;
    border: 1px solid {colors["primary"]};
}}

QScrollBar::handle:horizontal {{
    background-color: {colors["primary"]};
    border-radius: 6px;
    min-width: 30px;
    border: 2px solid transparent;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {colors["accent"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* Buttons - Enhanced with Glow Effects */
QPushButton {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 14px;
    min-height: 40px;
}}

QPushButton:hover {{
    background-color: {colors["accent"]};
    color: {colors["background"]};
    border: 2px solid {colors["accent"]};
}}

QPushButton:pressed {{
    background-color: {colors["primary"]};
    padding: 13px 23px 11px 25px;
}}

QPushButton:disabled {{
    background-color: {colors["cards"]};
    color: {colors["text_secondary"]};
    border: 1px solid {colors["card_hover"]};
}}

/* Primary Button Variant */
QPushButton#primaryButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    border: 2px solid {colors["accent"]};
    font-size: 16px;
}}

/* Accent Button Variant */
QPushButton#accentButton {{
    background-color: transparent;
    border: 2px solid {colors["accent"]};
    color: {colors["accent"]};
}}

QPushButton#accentButton:hover {{
    background-color: {colors["accent"]};
    color: {colors["background"]};
}}

/* Danger Button */
QPushButton#dangerButton {{
    background-color: {colors["danger"]};
    border: 2px solid {colors["danger"]};
}}

QPushButton#dangerButton:hover {{
    background-color: #FF7070;
    border: 2px solid #FF7070;
}}

/* Success Button */
QPushButton#successButton {{
    background-color: {colors["success"]};
    color: {colors["background"]};
    border: 2px solid {colors["success"]};
}}

/* Warning Button */
QPushButton#warningButton {{
    background-color: {colors["warning"]};
    color: {colors["background"]};
    border: 2px solid {colors["warning"]};
}}

/* Line Edits - Modern Input Fields */
QLineEdit {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    padding: 10px 15px;
    color: {colors["text_primary"]};
    selection-background-color: {colors["accent"]};
    selection-color: {colors["background"]};
    font-size: 14px;
}}

QLineEdit:focus {{
    border: 2px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

QLineEdit:disabled {{
    background-color: {colors["cards"]};
    color: {colors["text_secondary"]};
    border: 2px solid {colors["card_hover"]};
}}

/* Combo Boxes - Dropdown Selectors */
QComboBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    padding: 10px 15px;
    min-width: 140px;
    color: {colors["text_primary"]};
}}

QComboBox:focus {{
    border: 2px solid {colors["accent"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 35px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 10px solid {colors["accent"]};
    margin-right: 12px;
}}

QComboBox QAbstractItemView {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    selection-background-color: {colors["primary"]};
    selection-color: {colors["text_primary"]};
    outline: none;
    padding: 5px;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 10px;
    border-radius: 5px;
    margin: 2px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {colors["card_hover"]};
}}

/* Labels - Text Elements */
QLabel {{
    color: {colors["text_primary"]};
    background-color: transparent;
}}

QLabel#titleLabel {{
    font-size: 28px;
    font-weight: bold;
    color: {colors["accent"]};
    qproperty-alignment: AlignCenter;
}}

QLabel#subtitleLabel {{
    font-size: 16px;
    color: {colors["text_secondary"]};
}}

QLabel#secondaryLabel {{
    color: {colors["text_secondary"]};
    font-size: 12px;
}}

QLabel#headingLabel {{
    font-size: 20px;
    font-weight: bold;
    color: {colors["primary"]};
}}

/* Group Box - Section Containers */
QGroupBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    font-weight: bold;
    font-size: 15px;
    color: {colors["accent"]};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 20px;
    padding: 0 15px;
    color: {colors["accent"]};
    background-color: {colors["card_hover"]};
    border-radius: 8px;
}}

/* Sliders - Progress Controls */
QSlider::groove:horizontal {{
    border: none;
    height: 10px;
    background-color: {colors["cards"]};
    border-radius: 5px;
    border: 1px solid {colors["card_hover"]};
}}

QSlider::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors["accent"]},
        stop:1 {colors["primary"]});
    border: none;
    width: 22px;
    height: 22px;
    margin: -6px 0;
    border-radius: 11px;
}}

QSlider::handle:horizontal:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    border: 2px solid {colors["text_primary"]};
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    border-radius: 5px;
}}

/* Progress Bar - Loading Indicators */
QProgressBar {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["card_hover"]};
    border-radius: 10px;
    height: 16px;
    text-align: center;
    color: {colors["text_primary"]};
    font-weight: bold;
    font-size: 12px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    border-radius: 8px;
}}

/* Tab Widget - Tabbed Interface */
QTabWidget::pane {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    border-top-left-radius: 0px;
}}

QTabBar::tab {{
    background-color: {colors["cards"]};
    color: {colors["text_secondary"]};
    padding: 12px 25px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 3px;
    border: 2px solid transparent;
    border-bottom: none;
    font-weight: bold;
}}

QTabBar::tab:selected {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
    border: 2px solid {colors["accent"]};
    border-bottom: 2px solid {colors["cards"]};
}}

QTabBar::tab:hover:!selected {{
    background-color: {colors["card_hover"]};
    border: 2px solid {colors["card_hover"]};
    border-bottom: none;
}}

/* List Widget - Item Lists */
QListWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    padding: 8px;
    outline: none;
}}

QListWidget::item {{
    background-color: transparent;
    border-radius: 10px;
    padding: 12px;
    margin: 3px;
    border: 1px solid transparent;
}}

QListWidget::item:hover {{
    background-color: {colors["card_hover"]};
    border: 1px solid {colors["primary"]};
}}

QListWidget::item:selected {{
    background-color: {colors["primary"]};
    border: 1px solid {colors["accent"]};
    color: {colors["text_primary"]};
}}

/* Table Widget - Data Tables */
QTableWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    gridline-color: {colors["card_hover"]};
    outline: none;
}}

QTableWidget::item {{
    padding: 12px;
    border-radius: 5px;
}}

QTableWidget::item:hover {{
    background-color: {colors["card_hover"]};
}}

QTableWidget::item:selected {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
}}

QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    color: {colors["text_primary"]};
    padding: 12px;
    border: none;
    font-weight: bold;
    font-size: 14px;
    border-radius: 8px;
    margin: 2px;
}}

/* Spin Box - Numeric Input */
QSpinBox, QDoubleSpinBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    padding: 10px 15px;
    color: {colors["text_primary"]};
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

/* Check Box - Toggle Options */
QCheckBox {{
    color: {colors["text_primary"]};
    spacing: 12px;
    font-size: 14px;
}}

QCheckBox::indicator {{
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid {colors["primary"]};
    background-color: {colors["cards"]};
}}

QCheckBox::indicator:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    border: 2px solid {colors["accent"]};
}}

QCheckBox::indicator:hover {{
    border: 2px solid {colors["accent"]};
}}

/* Radio Button - Single Selection */
QRadioButton {{
    color: {colors["text_primary"]};
    spacing: 12px;
    font-size: 14px;
}}

QRadioButton::indicator {{
    width: 22px;
    height: 22px;
    border-radius: 11px;
    border: 2px solid {colors["primary"]};
    background-color: {colors["cards"]};
}}

QRadioButton::indicator:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    border: 6px solid {colors["cards"]};
}}

QRadioButton::indicator:hover {{
    border: 2px solid {colors["accent"]};
}}

/* Tool Tips - Help Messages */
QToolTip {{
    background-color: {colors["cards"]};
    color: {colors["text_primary"]};
    border: 2px solid {colors["accent"]};
    border-radius: 10px;
    padding: 10px 15px;
    font-size: 13px;
    font-weight: bold;
}}

/* Menu - Context Menus */
QMenu {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    padding: 10px;
}}

QMenu::item {{
    padding: 10px 25px;
    border-radius: 8px;
    margin: 2px;
}}

QMenu::item:selected {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
}}

QMenu::separator {{
    height: 2px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    margin: 5px 0;
    border-radius: 1px;
}}

/* Status Bar - Bottom Information Bar */
QStatusBar {{
    background-color: {colors["cards"]};
    border-top: 2px solid {colors["primary"]};
    color: {colors["text_secondary"]};
    font-size: 13px;
}}

/* Frame with Glow Effect - Card Containers */
QFrame#glassFrame {{
    background-color: rgba(18, 26, 43, 0.9);
    border: 2px solid {colors["primary"]};
    border-radius: 18px;
}}

QFrame#accentFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(18, 26, 43, 0.9),
        stop:1 rgba(30, 136, 229, 0.2));
    border: 2px solid {colors["accent"]};
    border-radius: 18px;
}}

QFrame#contentFrame {{
    background-color: transparent;
}}

/* Special Label Styles */
QLabel#successLabel {{
    color: {colors["success"]};
    font-weight: bold;
    font-size: 15px;
}}

QLabel#warningLabel {{
    color: {colors["warning"]};
    font-weight: bold;
    font-size: 15px;
}}

QLabel#errorLabel {{
    color: {colors["danger"]};
    font-weight: bold;
    font-size: 15px;
}}

/* Card Widget Style - Content Cards */
QFrame#cardWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 15px;
}}

QFrame#cardWidget:hover {{
    border: 2px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

/* Search Box - Enhanced Search Input */
QLineEdit#searchBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 30px;
    padding: 12px 25px;
    font-size: 15px;
    color: {colors["text_primary"]};
}}

QLineEdit#searchBox:focus {{
    border: 2px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

/* Navigation Bar - Side/Top Navigation */
QToolBar#navBar {{
    background-color: {colors["cards"]};
    border: none;
    spacing: 8px;
    padding: 10px;
    border-right: 2px solid {colors["primary"]};
}}

QToolBar#navBar QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 12px;
    padding: 12px 10px;
    color: {colors["text_secondary"]};
    font-size: 12px;
    font-weight: bold;
}}

QToolBar#navBar QToolButton:hover {{
    background-color: {colors["card_hover"]};
    color: {colors["text_primary"]};
}}

QToolBar#navBar QToolButton:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {colors["primary"]},
        stop:1 {colors["accent"]});
    color: {colors["text_primary"]};
}}

/* Top Bar - Window Title Bar */
QFrame#topBar {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["gradient_start"]},
        stop:1 {colors["gradient_end"]});
    border-bottom: 2px solid {colors["primary"]};
}}

/* Window Control Buttons */
QToolButton#windowBtn {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    color: {colors["text_secondary"]};
    font-size: 16px;
}}

QToolButton#windowBtn:hover {{
    background-color: {colors["card_hover"]};
    color: {colors["text_primary"]};
}}

QToolButton#closeBtn {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    color: {colors["text_secondary"]};
    font-size: 16px;
}}

QToolButton#closeBtn:hover {{
    background-color: {colors["danger"]};
    color: {colors["text_primary"]};
}}

/* User Profile Button */
QToolButton#userBtn {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 20px;
    padding: 8px 16px;
    color: {colors["text_primary"]};
    font-weight: bold;
}}

QToolButton#userBtn:hover {{
    background-color: {colors["primary"]};
    border: 2px solid {colors["accent"]};
}}

/* Stacked Widget Background */
QStackedWidget {{
    background-color: transparent;
}}

/* Graphics View */
QGraphicsView {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
}}

/* Plain Text Edit - Multi-line Input */
QPlainTextEdit {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    padding: 12px;
    color: {colors["text_primary"]};
}}

QPlainTextEdit:focus {{
    border: 2px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

/* Calendar Widget */
QCalendarWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
}}

QCalendarWidget QMenu {{
    background-color: {colors["background"]};
}}

QCalendarWidget QSpinBox {{
    background-color: {colors["background"]};
}}

/* Size Grip */
QSizeGrip {{
    width: 18px;
    height: 18px;
}}

/* Splitter - Resizable Divider */
QSplitter::handle {{
    background-color: {colors["primary"]};
    width: 3px;
}}

QSplitter::handle:horizontal {{
    width: 3px;
}}

QSplitter::handle:vertical {{
    height: 3px;
}}

/* Tree Widget - Hierarchical Lists */
QTreeWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    outline: none;
}}

QTreeWidget::item {{
    padding: 8px;
    border-radius: 5px;
    margin: 2px;
}}

QTreeWidget::item:hover {{
    background-color: {colors["card_hover"]};
}}

QTreeWidget::item:selected {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
}}

/* Scroll Area */
QScrollArea {{
    background-color: transparent;
    border: none;
}}

/* Dock Widget */
QDockWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}}

QDockWidget::title {{
    background-color: {colors["primary"]};
    padding: 10px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    color: {colors["text_primary"]};
    font-weight: bold;
}}

/* Special Effects - Neon Glow Borders */
QFrame#neonGlow {{
    background-color: {colors["cards"]};
    border: 3px solid {colors["accent"]};
    border-radius: 20px;
}}

/* Animated Hover Effect Container */
QFrame#animatedFrame {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 15px;
}}

QFrame#animatedFrame:hover {{
    border: 2px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

/* Video Player Controls */
QFrame#playerControls {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0, 0, 0, 0.8),
        stop:1 rgba(18, 26, 43, 0.9));
    border: 1px solid {colors["primary"]};
    border-radius: 10px;
}}

/* Channel Card */
QFrame#channelCard {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 12px;
}}

QFrame#channelCard:hover {{
    border: 2px solid {colors["accent"]};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {colors["card_hover"]},
        stop:1 {colors["cards"]});
}}

/* Category Badge */
QLabel#categoryBadge {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
    border-radius: 15px;
    padding: 5px 15px;
    font-weight: bold;
    font-size: 12px;
}}

/* Quality Badge */
QLabel#qualityBadge {{
    background-color: {colors["accent"]};
    color: {colors["background"]};
    border-radius: 8px;
    padding: 3px 10px;
    font-weight: bold;
    font-size: 11px;
}}

/* Live Indicator */
QLabel#liveIndicator {{
    background-color: {colors["danger"]};
    color: {colors["text_primary"]};
    border-radius: 10px;
    padding: 5px 12px;
    font-weight: bold;
    font-size: 12px;
}}

/* AI Chat Bubble */
QFrame#aiChatBubble {{
    background-color: {colors["card_hover"]};
    border: 2px solid {colors["accent"]};
    border-radius: 15px;
    padding: 10px;
}}

/* Settings Section */
QFrame#settingsSection {{
    background-color: {colors["cards"]};
    border: 1px solid {colors["primary"]};
    border-radius: 12px;
    padding: 15px;
}}

/* Info Panel */
QFrame#infoPanel {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {colors["cards"]},
        stop:1 {colors["card_hover"]});
    border: 2px solid {colors["primary"]};
    border-radius: 15px;
}}
"""
