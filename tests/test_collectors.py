"""
Unit tests for HackerNewsCollector and ArxivCollector with mocking.
"""

from unittest.mock import MagicMock
import pytest
from src.collectors.hackernews import HackerNewsCollector
from src.collectors.arxiv import ArxivCollector
from src.models import SourceStatus


def test_hackernews_collector_success(sample_hn_hits):
    collector = HackerNewsCollector()
    mock_response = MagicMock()
    mock_response.json.return_value = {"hits": sample_hn_hits}
    collector.get = MagicMock(return_value=mock_response)

    items = collector.collect()
    assert len(items) > 0
    assert collector.status in (SourceStatus.SUCCESS, SourceStatus.DEGRADED)


def test_hackernews_collector_handles_empty():
    collector = HackerNewsCollector()
    mock_response = MagicMock()
    mock_response.json.return_value = {"hits": []}
    collector.get = MagicMock(return_value=mock_response)

    items = collector.collect()
    assert items == []
    assert collector.status == SourceStatus.EMPTY


def test_arxiv_collector_xml_parsing(sample_arxiv_xml):
    collector = ArxivCollector()
    mock_response = MagicMock()
    mock_response.content = sample_arxiv_xml
    collector.get = MagicMock(return_value=mock_response)

    papers = collector.collect()
    assert len(papers) == 1
    p = papers[0]
    assert p.title == "SwarmEvolve: Latent Agent Swarms for Evolutionary Discovery"
    assert "Qile Jiang" in p.authors
    assert p.published_date == "2026-11-09"
    assert p.category == "cs.AI"
    assert p.link.startswith("https://")
    assert collector.status == SourceStatus.SUCCESS


def test_arxiv_collector_fallback_transparency(tmp_path):
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    sample_report = reports_dir / "2026-11-08.md"
    sample_report.write_text(
        """### 1. [Fallback Paper](https://arxiv.org/abs/999)
- 👥 **Yazarlar:** Jane Doe
- 📅 **Yayın Tarihi:** `2026-11-08`
- 🏷️ **Kategori:** `cs.LG`
- 🔗 **Bağlantı:** [https://arxiv.org/abs/999](https://arxiv.org/abs/999)
- 📝 **Özet:** *An archived summary from yesterday.*
""",
        encoding="utf-8"
    )

    collector = ArxivCollector(reports_dir=reports_dir)
    # Simulate API failure
    collector.get = MagicMock(side_effect=RuntimeError("ArXiv API Down"))

    papers = collector.collect()
    assert len(papers) == 1
    assert papers[0].is_archived_fallback is True
    assert papers[0].title == "Fallback Paper"
    assert collector.status == SourceStatus.DEGRADED
