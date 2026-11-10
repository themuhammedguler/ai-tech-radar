"""
Collectors package for remote data acquisition.
"""

from .base import BaseCollector
from .hackernews import HackerNewsCollector
from .arxiv import ArxivCollector

__all__ = ["BaseCollector", "HackerNewsCollector", "ArxivCollector"]
