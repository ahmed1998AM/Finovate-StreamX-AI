"""
Stylesheet Module
=================
Cyberpunk Glassmorphism theme styles for PySide6.
"""

from core.config import THEME_COLORS


def get_stylesheet() -> str:
    """
    Get the main application stylesheet.
    
    Returns:
        Complete CSS stylesheet string
    """
    colors = THEME_COLORS
    
    return f"""
/* ============================================
   Finovate StreamX AI - Cyberpunk Glassmorphism Theme
   ============================================ */

/* Global Styles */
QWidget {{
    background-color: {colors["background"]};
    color: {colors["text_primary"]};
    font-family: "Segoe UI", "Roboto", sans-serif;
    font-size: 14px;
}}

QMainWindow {{
    background-color: {colors["background"]};
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {colors["cards"]};
    width: 10px;
    border-radius: 5px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {colors["primary"]};
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors["accent"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {colors["cards"]};
    height: 10px;
    border-radius: 5px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {colors["primary"]};
    border-radius: 5px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {colors["accent"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* Buttons */
QPushButton {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
}}

QPushButton:hover {{
    background-color: {colors["accent"]};
    color: {colors["background"]};
}}

QPushButton:pressed {{
    background-color: {colors["primary"]};
    padding: 11px 19px 9px 21px;
}}

QPushButton:disabled {{
    background-color: {colors["cards"]};
    color: {colors["text_secondary"]};
}}

/* Primary Button Variant */
QPushButton#primaryButton {{
    background-color: {colors["primary"]};
    border: 2px solid {colors["accent"]};
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
}}

QPushButton#dangerButton:hover {{
    background-color: #FF7070;
}}

/* Line Edits */
QLineEdit {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 8px;
    padding: 8px 12px;
    color: {colors["text_primary"]};
    selection-background-color: {colors["accent"]};
}}

QLineEdit:focus {{
    border: 2px solid {colors["accent"]};
}}

QLineEdit:disabled {{
    background-color: {colors["cards"]};
    color: {colors["text_secondary"]};
}}

/* Combo Boxes */
QComboBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 120px;
}}

QComboBox:focus {{
    border: 2px solid {colors["accent"]};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid {colors["accent"]};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 8px;
    selection-background-color: {colors["primary"]};
    selection-color: {colors["text_primary"]};
}}

/* Labels */
QLabel {{
    color: {colors["text_primary"]};
    background-color: transparent;
}}

QLabel#titleLabel {{
    font-size: 24px;
    font-weight: bold;
    color: {colors["accent"]};
}}

QLabel#subtitleLabel {{
    font-size: 16px;
    color: {colors["text_secondary"]};
}}

QLabel#secondaryLabel {{
    color: {colors["text_secondary"]};
    font-size: 12px;
}}

/* Group Box */
QGroupBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    margin-top: 15px;
    padding-top: 15px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 15px;
    padding: 0 10px;
    color: {colors["accent"]};
}}

/* Sliders */
QSlider::groove:horizontal {{
    border: none;
    height: 8px;
    background-color: {colors["cards"]};
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background-color: {colors["accent"]};
    border: none;
    width: 18px;
    height: 18px;
    margin: -5px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background-color: {colors["primary"]};
}}

/* Progress Bar */
QProgressBar {{
    background-color: {colors["cards"]};
    border: none;
    border-radius: 8px;
    height: 12px;
    text-align: center;
    color: transparent;
}}

QProgressBar::chunk {{
    background-color: {colors["primary"]};
    border-radius: 8px;
}}

/* Tab Widget */
QTabWidget::pane {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
}}

QTabBar::tab {{
    background-color: {colors["cards"]};
    color: {colors["text_secondary"]};
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
}}

QTabBar::tab:hover:!selected {{
    background-color: {colors["card_hover"]};
}}

/* List Widget */
QListWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    padding: 5px;
}}

QListWidget::item {{
    background-color: transparent;
    border-radius: 8px;
    padding: 10px;
    margin: 2px;
}}

QListWidget::item:hover {{
    background-color: {colors["card_hover"]};
}}

QListWidget::item:selected {{
    background-color: {colors["primary"]};
}}

/* Table Widget */
QTableWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    gridline-color: {colors["card_hover"]};
}}

QTableWidget::item {{
    padding: 10px;
}}

QTableWidget::item:hover {{
    background-color: {colors["card_hover"]};
}}

QTableWidget::item:selected {{
    background-color: {colors["primary"]};
}}

QHeaderView::section {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
    padding: 10px;
    border: none;
    font-weight: bold;
}}

/* Spin Box */
QSpinBox, QDoubleSpinBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 8px;
    padding: 8px 12px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {colors["accent"]};
}}

/* Check Box */
QCheckBox {{
    color: {colors["text_primary"]};
    spacing: 10px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 5px;
    border: 2px solid {colors["primary"]};
    background-color: {colors["cards"]};
}}

QCheckBox::indicator:checked {{
    background-color: {colors["primary"]};
    border: 2px solid {colors["primary"]};
}}

QCheckBox::indicator:hover {{
    border: 2px solid {colors["accent"]};
}}

/* Radio Button */
QRadioButton {{
    color: {colors["text_primary"]};
    spacing: 10px;
}}

QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid {colors["primary"]};
    background-color: {colors["cards"]};
}}

QRadioButton::indicator:checked {{
    background-color: {colors["primary"]};
    border: 5px solid {colors["cards"]};
}}

/* Tool Tip */
QToolTip {{
    background-color: {colors["cards"]};
    color: {colors["text_primary"]};
    border: 2px solid {colors["accent"]};
    border-radius: 8px;
    padding: 8px;
    font-size: 13px;
}}

/* Menu */
QMenu {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    padding: 10px;
}}

QMenu::item {{
    padding: 10px 20px;
    border-radius: 8px;
}}

QMenu::item:selected {{
    background-color: {colors["primary"]};
}}

QMenu::separator {{
    height: 2px;
    background-color: {colors["primary"]};
    margin: 5px 0;
}}

/* Status Bar */
QStatusBar {{
    background-color: {colors["cards"]};
    border-top: 2px solid {colors["primary"]};
    color: {colors["text_secondary"]};
}}

/* Frame with Glow Effect */
QFrame#glassFrame {{
    background-color: rgba(18, 26, 43, 0.8);
    border: 2px solid {colors["primary"]};
    border-radius: 15px;
}}

QFrame#accentFrame {{
    background-color: rgba(18, 26, 43, 0.8);
    border: 2px solid {colors["accent"]};
    border-radius: 15px;
}}

/* Success Label */
QLabel#successLabel {{
    color: {colors["success"]};
    font-weight: bold;
}}

/* Warning Label */
QLabel#warningLabel {{
    color: #FFC107;
    font-weight: bold;
}}

/* Error Label */
QLabel#errorLabel {{
    color: {colors["danger"]};
    font-weight: bold;
}}

/* Card Widget Style */
QFrame#cardWidget {{
    background-color: {colors["cards"]};
    border: 1px solid {colors["primary"]};
    border-radius: 12px;
}}

QFrame#cardWidget:hover {{
    border: 1px solid {colors["accent"]};
    background-color: {colors["card_hover"]};
}}

/* Search Box */
QLineEdit#searchBox {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 25px;
    padding: 10px 20px;
    font-size: 14px;
}}

QLineEdit#searchBox:focus {{
    border: 2px solid {colors["accent"]};
}}

/* Navigation Bar */
QToolBar#navBar {{
    background-color: {colors["cards"]};
    border: none;
    spacing: 10px;
    padding: 10px;
}}

QToolBar#navBar QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 10px;
    padding: 10px 15px;
    color: {colors["text_secondary"]};
    font-size: 13px;
}}

QToolBar#navBar QToolButton:hover {{
    background-color: {colors["card_hover"]};
    color: {colors["text_primary"]};
}}

QToolBar#navBar QToolButton:checked {{
    background-color: {colors["primary"]};
    color: {colors["text_primary"]};
}}

/* Stacked Widget Background */
QStackedWidget {{
    background-color: transparent;
}}

/* Graphics View */
QGraphicsView {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
}}

/* Plain Text Edit */
QPlainTextEdit {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
    padding: 10px;
}}

QPlainTextEdit:focus {{
    border: 2px solid {colors["accent"]};
}}

/* Calendar Widget */
QCalendarWidget {{
    background-color: {colors["cards"]};
    border: 2px solid {colors["primary"]};
    border-radius: 10px;
}}

QCalendarWidget QMenu {{
    background-color: {colors["background"]};
}}

QCalendarWidget QSpinBox {{
    background-color: {colors["background"]};
}}

/* Size Grip */
QSizeGrip {{
    width: 15px;
    height: 15px;
}}

/* Splitter */
QSplitter::handle {{
    background-color: {colors["primary"]};
    width: 2px;
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}
"""
