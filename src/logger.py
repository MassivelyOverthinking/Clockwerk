#-------------------- Imports --------------------

import logging
import os

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

#-------------------- Logging Configuration --------------------

load_dotenv("/Users/simon/Desktop/Projects/Uptime Monitor/.env")

# Logging Variables & Formatting
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "monitor.log")
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"

LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d %H:%M:%S")

def setup_logger(name: str) -> logging.Logger:
    """
    Set ups, configures and returns a Logger-object with a given name.
    The Logger utilises a Stream Handler & optional Rotating File Handler
    """

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Returns Logger without adding additonal handlers if called multiple times
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file Handler
    if LOG_TO_FILE:
        file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger