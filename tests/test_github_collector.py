"""
Unit tests for GithubTrendingCollector.
"""

from unittest.mock import MagicMock
from src.collectors.github_trending import GithubTrendingCollector
from src.models import SourceStatus


def test_github_collector_success():
    collector = GithubTrendingCollector()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [
            {
                "full_name": "astral-sh/uv",
                "html_url": "https://github.com/astral-sh/uv",
                "description": "An extremely fast Python package and project manager.",
                "language": "Rust",
                "stargazers_count": 35000,
                "forks_count": 1200,
                "topics": ["python", "rust", "package-manager"]
            }
        ]
    }
    collector.get = MagicMock(return_value=mock_response)

    repos = collector.collect()
    assert len(repos) == 1
    repo = repos[0]
    assert repo.name == "astral-sh/uv"
    assert repo.language == "Rust"
    assert repo.stars == 35000
    assert repo.url.startswith("https://")
    assert collector.status in (SourceStatus.SUCCESS, SourceStatus.DEGRADED)


def test_github_collector_empty_response():
    collector = GithubTrendingCollector()
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": []}
    collector.get = MagicMock(return_value=mock_response)

    repos = collector.collect()
    assert repos == []
    assert collector.status == SourceStatus.EMPTY
