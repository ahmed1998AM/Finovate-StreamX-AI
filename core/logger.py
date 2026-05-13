"""
Logging Module
==============
Centralized logging with file rotation and multiple log levels.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional


class StreamXLogger:
    """Custom logger for Finovate StreamX AI application."""
    
    def __init__(
        self,
        name: str = "StreamX",
        log_dir: Optional[Path] = None,
        level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5
    ):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
            level: Logging level
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup log files to keep
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"streamx_{datetime.now().strftime('%Y%m%d')}.log"
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self.logger
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """Log error message with optional exception info."""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """Log critical message with optional exception info."""
        self.logger.critical(message, exc_info=exc_info)


# Global logger instance
_logger: Optional[StreamXLogger] = None


def get_logger(
    name: str = "StreamX",
    log_dir: Optional[Path] = None,
    level: int = logging.INFO
) -> StreamXLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = StreamXLogger(name=name, log_dir=log_dir, level=level)
    return _logger


def setup_logging(log_dir: Optional[Path] = None, level: int = logging.INFO):
    """Setup logging for the application."""
    global _logger
    _logger = StreamXLogger(log_dir=log_dir, level=level)
    return _logger
