import logging
import sys
import os
from pathlib import Path
from .config import settings

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

DEFAULT_LOG_LEVEL = 'INFO'

def get_valid_log_level(level_str: str) -> int:
    upper_level = level_str.upper()
    if upper_level not in LOG_LEVELS:
        valid_levels = ', '.join(LOG_LEVELS.keys())
        raise ValueError(
            f"Invalid log level '{level_str}'. "
            f"Valid levels are: {valid_levels}"
        )
    return LOG_LEVELS[upper_level]

def setup_logger(log_level_str=DEFAULT_LOG_LEVEL):
    logger = logging.getLogger(settings.logger.name)
    
    try:
        log_level = get_valid_log_level(log_level_str)
    except ValueError as e:
        print(f"Log level error: {e}. Using default level {DEFAULT_LOG_LEVEL}")
        log_level = LOG_LEVELS[DEFAULT_LOG_LEVEL]
    
    logger.setLevel(log_level)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Консольный вывод
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    
    return logger

logger = setup_logger(settings.logger.level)