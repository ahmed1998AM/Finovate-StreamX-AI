"""
Language Selector Widget
=========================
UI widget for switching between languages.

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon

from core.i18n.translator import get_translator, set_language, t


class LanguageSelector(QWidget):
    """Language selection widget with flag icons."""
    
    language_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.translator = get_translator()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Language label
        label = QLabel(t("settings.language"))
        label.setStyleSheet("color: #B0BEC5; font-size: 12px;")
        layout.addWidget(label)
        
        # Language combo box
        self.combo = QComboBox()
        self.combo.setMinimumWidth(150)
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #121A2B;
                color: #FFFFFF;
                border: 1px solid #1E88E5;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00E5FF;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #121A2B;
                color: #FFFFFF;
                border: 1px solid #1E88E5;
                selection-background-color: #1A2744;
            }
        """)
        
        # Populate languages
        self._populate_languages()
        
        self.combo.currentTextChanged.connect(self._on_language_selected)
        layout.addWidget(self.combo)
        
        self.setLayout(layout)
    
    def _populate_languages(self):
        """Populate the combo box with available languages."""
        languages = {
            "en": "🇬🇧 English",
            "ar": "🇸🇦 العربية"
        }
        
        current = self.translator.get_language()
        
        for code, name in languages.items():
            self.combo.addItem(name, code)
            if code == current:
                self.combo.setCurrentIndex(self.combo.count() - 1)
    
    def _on_language_selected(self, text):
        """Handle language selection."""
        # Extract language code from display text
        code = self.combo.currentData()
        
        if set_language(code):
            self.language_changed.emit(code)
            # Update UI direction for RTL languages
            if code == "ar":
                self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            else:
                self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


class LanguageDialog(QDialog):
    """Full language selection dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("settings.language"))
        self.setMinimumSize(400, 300)
        self.translator = get_translator()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(t("settings.language"))
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #00E5FF;
            padding: 10px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Select your preferred language / اختر لغتك المفضلة")
        desc.setStyleSheet("color: #B0BEC5; font-size: 12px; padding: 10px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Language list
        self.combo = QComboBox()
        self.combo.setMinimumHeight(40)
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #121A2B;
                color: #FFFFFF;
                border: 2px solid #1E88E5;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: #121A2B;
                color: #FFFFFF;
                border: 1px solid #1E88E5;
                selection-background-color: #1A2744;
                font-size: 14px;
            }
        """)
        
        languages = {
            "en": "🇬🇧 English",
            "ar": "🇸🇦 العربية"
        }
        
        current = self.translator.get_language()
        for code, name in languages.items():
            self.combo.addItem(name, code)
            if code == current:
                self.combo.setCurrentIndex(self.combo.count() - 1)
        
        layout.addWidget(self.combo)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        layout.addWidget(buttons)
    
    def get_selected_language(self) -> str:
        """Get the selected language code."""
        return self.combo.currentData()


def show_language_selector(parent=None) -> str:
    """Show language selection dialog and return selected language."""
    dialog = LanguageDialog(parent)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return dialog.get_selected_language()
    return None
