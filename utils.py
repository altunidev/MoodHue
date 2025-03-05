# utils.py
import logging
import sys
from typing import Optional
from config import OSC_CONFIG, LOGGING_CONFIG

def setup_logging(
    debug_level: int = 1, 
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None
) -> logging.Logger:
    """
    Centralized logging setup with flexible configuration
    
    Args:
        debug_level: Logging verbosity (0-2)
        log_file: Optional file to save logs
        log_format: Custom log message format
        date_format: Custom date format for logs
    
    Returns:
        Configured logger instance
    """
    # Log level mapping
    log_levels = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }
    
    # Default formats if not provided
    log_format = log_format or '%(asctime)s | %(levelname)8s | %(message)s'
    date_format = date_format or '%Y-%m-%d %H:%M:%S'
    
    # Configure logging
    logging.basicConfig(
        level=log_levels.get(debug_level, logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=[]  # We'll add handlers manually
    )
    
    # Create logger
    logger = logging.getLogger()
    logger.handlers.clear()  # Clear any existing handlers
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Could not create log file: {e}")
    
    return logger

def validate_config(config: dict) -> bool:
    """
    Validate configuration dictionary
    
    Args:
        config: Configuration dictionary to validate
    
    Returns:
        Boolean indicating if configuration is valid
    """
    # Add specific validation logic for your configuration
    required_keys = ['ip', 'port', 'debug_level']
    return all(key in config for key in required_keys)

def get_default_config():
    """
    Generate a default configuration dictionary
    
    Returns:
        Dictionary with default configuration values
    """
    return {
        'ip': OSC_CONFIG['IP'],  # Changed from 'DEFAULT_IP'
        'port': OSC_CONFIG['LISTEN_PORT'],  # Changed from 'DEFAULT_LISTEN_PORT'
        'debug_level': LOGGING_CONFIG['DEFAULT_DEBUG_LEVEL'],
        'throttle_ms': LOGGING_CONFIG['DEFAULT_THROTTLE_MS']
    }
