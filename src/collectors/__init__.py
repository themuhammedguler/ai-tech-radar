"""
Collectors package for remote data acquisition.
Provides resilient collectors for HackerNews, GitHub, Hugging Face, and ArXiv.
"""

from .base import BaseCollector
from .hackernews import HackerNewsCollector
from .github_trending import GithubTrendingCollector
from .huggingface import HuggingFaceCollector
from .arxiv import ArxivCollector

__all__ = [
    "BaseCollector",
    "HackerNewsCollector",
    "GithubTrendingCollector",
    "HuggingFaceCollector",
    "ArxivCollector"
]
