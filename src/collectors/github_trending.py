"""
GitHub Trending repositories collector.
Queries GitHub's Search API to discover high-velocity open-source software,
developer tools, and AI infrastructure repositories.
"""

from datetime import datetime, timedelta
import os
from typing import Any
import requests

from src.collectors.base import BaseCollector
from src.config import GITHUB_SEARCH_URL, GITHUB_TARGET_COUNT, GITHUB_TOKEN_ENV
from src.logging_config import logger
from src.models import GithubRepoItem, SourceStatus


class GithubTrendingCollector(BaseCollector):
    """Collects top trending open-source projects on GitHub."""

    def __init__(
        self,
        api_url: str = GITHUB_SEARCH_URL,
        target_count: int = GITHUB_TARGET_COUNT,
        lookback_days: int = 14,
        min_stars: int = 30,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.api_url = api_url
        self.target_count = target_count
        self.lookback_days = lookback_days
        self.min_stars = min_stars

        # Optional GitHub Token authorization for higher rate limits
        token = os.getenv(GITHUB_TOKEN_ENV)
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Accept": "application/vnd.github+json"})

    def collect(self) -> list[GithubRepoItem]:
        """
        Executes GitHub Search API request and parses top trending repos.

        Returns:
            List of validated GithubRepoItem objects.
        """
        logger.info(f"Querying GitHub Search API for trending repos (past {self.lookback_days} days)...")
        date_cutoff = (datetime.now() - timedelta(days=self.lookback_days)).strftime("%Y-%m-%d")
        query = f"created:>{date_cutoff} stars:>{self.min_stars}"

        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": self.target_count * 2
        }

        try:
            response = self.get(self.api_url, params=params)
            data = response.json()
        except requests.RequestException as e:
            self.status = SourceStatus.FAILED
            logger.error(f"GitHub API request failed: {e}")
            return []
        except ValueError as e:
            self.status = SourceStatus.FAILED
            logger.error(f"GitHub API returned non-JSON payload: {e}")
            return []

        raw_items = data.get("items", [])
        if not raw_items:
            self.status = SourceStatus.EMPTY
            logger.warning("GitHub API returned 0 trending repositories.")
            return []

        repos: list[GithubRepoItem] = []
        for item in raw_items[:self.target_count]:
            full_name = item.get("full_name") or item.get("name") or "Unknown/Repo"
            url = item.get("html_url") or f"https://github.com/{full_name}"
            raw_desc = item.get("description") or "Açıklama bulunamadı."
            # Clean description of table delimiters
            clean_desc = raw_desc.replace("|", "-").strip()
            language = item.get("language") or "General"
            stars = max(0, int(item.get("stargazers_count") or 0))
            forks = max(0, int(item.get("forks_count") or 0))
            topics = item.get("topics") or []

            try:
                repo_item = GithubRepoItem(
                    name=full_name,
                    url=url,
                    description=clean_desc,
                    language=language,
                    stars=stars,
                    forks=forks,
                    topics=topics[:5]
                )
                repos.append(repo_item)
            except ValueError as e:
                logger.warning(f"Validation error for GitHub repo '{full_name}': {e}")

        if len(repos) == 0:
            self.status = SourceStatus.EMPTY
        elif len(repos) < self.target_count:
            self.status = SourceStatus.DEGRADED
        else:
            self.status = SourceStatus.SUCCESS

        logger.info(f"Successfully collected {len(repos)} GitHub trending projects.")
        return repos
