"""
Logging configuration for AI & Tech Daily Radar.
Provides standardized, level-aware, structured console logging.
"""

import logging
import sys


def setup_logger(name: str = "AITechRadar", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a structured logger instance."""
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = setup_logger()
