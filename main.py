"""
Finovate StreamX AI - Main Application Entry Point
===================================================
Ultimate AI IPTV & Media Center

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
Contact: 01225155329 | gogom8870@gmail.com
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

from core.config import get_config, AppConfig
from core.logger import setup_logging, get_logger
from database.db_manager import DatabaseManager, initialize_database
from ui.styles import get_stylesheet


def create_splash_screen() -> QSplashScreen:
    """Create and show splash screen."""
    # Create a simple splash screen programmatically
    splash_pixmap = QPixmap(400, 300)
    splash_pixmap.fill(Qt.GlobalColor.darkBlue)
    
    splash = QSplashScreen(splash_pixmap, Qt.WindowType.WindowStaysOnTopHint)
    splash.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
    
    # Show loading message
    splash.showMessage(
        "Finovate StreamX AI\nVersion 1.0.0\n\nLoading...",
        Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white
    )
    
    return splash


async def initialize_app():
    """Initialize application components asynchronously."""
    logger = get_logger()
    config = get_config()
    
    logger.info(f"Initializing {config.APP_NAME} v{config.VERSION}")
    logger.info(f"Developer: {config.AUTHOR}")
    
    # Initialize database
    db_manager = DatabaseManager(config.DATABASE_PATH)
    await db_manager.connect()
    await initialize_database(db_manager)
    logger.info("Database initialized successfully")
    
    return db_manager


def main():
    """Main application entry point."""
    # Setup logging
    config = get_config()
    logger = setup_logging(log_dir=config.LOGS_DIR)
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName(config.APP_NAME)
        app.setApplicationVersion(config.VERSION)
        app.setOrganizationName(config.BRAND)
        
        # Set application font
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        # Show splash screen
        splash = create_splash_screen()
        splash.show()
        app.processEvents()
        
        # Initialize async components
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            db_manager = loop.run_until_complete(initialize_app())
        finally:
            loop.close()
        
        splash.finish(QApplication.instance().activeWindow() if QApplication.instance().activeWindow() else None)
        
        # Apply stylesheet
        app.setStyleSheet(get_stylesheet())
        
        # TODO: Create and show main window
        # from ui.main_window import MainWindow
        # window = MainWindow(db_manager)
        # window.show()
        
        logger.info("Application started successfully")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
