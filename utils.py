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

def validate_config(config: dict, required_keys: list) -> bool:
    """
    Validate that all required keys exist in the configuration.
    
    Args:
        config: The configuration dictionary.
        required_keys: A list of keys that must be present in the configuration.
        
    Returns:
        Boolean indicating whether all required keys are present.
    """
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f"Missing keys: {', '.join(missing_keys)}")
        return False
    return True

def get_default_config():
    return {
        'ip': OSC_CONFIG['IP'],
        'port': OSC_CONFIG['LISTEN_PORT'],
        'debug_level': LOGGING_CONFIG['DEBUG_LEVEL'],
        'throttle_ms': LOGGING_CONFIG['DEFAULT_THROTTLE_MS']
    }
