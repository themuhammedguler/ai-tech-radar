"""
HackerNews data collector.
Queries Algolia's HackerNews API and coordinates with ContentFilter.
"""

from typing import Any
import requests

from src.collectors.base import BaseCollector
from src.config import HN_API_URL, HN_POOL_SIZE, HN_TARGET_COUNT
from src.logging_config import logger
from src.models import SourceStatus, TrendItem
from src.processors.content_filter import ContentFilter


class HackerNewsCollector(BaseCollector):
    """Fetches front page tech trends from HackerNews via Algolia API."""

    def __init__(
        self,
        api_url: str = HN_API_URL,
        pool_size: int = HN_POOL_SIZE,
        target_count: int = HN_TARGET_COUNT,
        content_filter: ContentFilter | None = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.api_url = api_url
        self.pool_size = pool_size
        self.target_count = target_count
        self.filter = content_filter or ContentFilter()

    def collect(self) -> list[TrendItem]:
        """
        Executes HackerNews collection, filters noise, and returns top tech items.

        Returns:
            List of validated TrendItem objects.
        """
        logger.info(f"Initiating HackerNews collection (target pool: {self.pool_size})...")
        params = {
            "tags": "front_page",
            "hitsPerPage": self.pool_size
        }

        try:
            response = self.get(self.api_url, params=params)
            data = response.json()
        except requests.RequestException as e:
            self.status = SourceStatus.FAILED
            logger.error(f"HackerNews API request failed: {e}")
            raise RuntimeError(f"HackerNews collection failed: {e}") from e
        except ValueError as e:
            self.status = SourceStatus.FAILED
            logger.error(f"Failed to parse HackerNews JSON response: {e}")
            raise RuntimeError(f"HackerNews invalid JSON payload: {e}") from e

        hits = data.get("hits", [])
        if not hits:
            self.status = SourceStatus.EMPTY
            logger.warning("HackerNews API returned 0 hits.")
            return []

        curated_trends = self.filter.filter_and_rank(hits, limit=self.target_count)

        if len(curated_trends) == 0:
            self.status = SourceStatus.EMPTY
            logger.warning("No trends remained after filtering.")
        elif len(curated_trends) < self.target_count:
            self.status = SourceStatus.DEGRADED
            logger.warning(
                f"HackerNews yielded only {len(curated_trends)} items (expected {self.target_count})."
            )
        else:
            self.status = SourceStatus.SUCCESS
            logger.info(f"Successfully collected {len(curated_trends)} HackerNews tech trends.")

        return curated_trends
