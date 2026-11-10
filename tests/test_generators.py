"""
Unit tests for ReportGenerator and ReadmeUpdater.
"""

import pytest
from src.generators.report_generator import ReportGenerator
from src.generators.readme_updater import ReadmeUpdater
from src.models import TrendItem, ArxivPaper, SourceStatus


@pytest.fixture
def mock_trend_item():
    return TrendItem(
        title="Rust UI Framework",
        url="https://github.com/example/rust-ui",
        hn_url="https://news.ycombinator.com/item?id=123",
        points=150,
        comments=40,
        category="💻 Yazılım & Geliştirme",
        tech_score=3,
        ranking_score=500.0
    )


@pytest.fixture
def mock_arxiv_paper():
    return ArxivPaper(
        title="Agentic Reasoning",
        summary="A study on autonomous agent reasoning.",
        link="https://arxiv.org/abs/2611.12345",
        authors="Alice, Bob",
        category="cs.AI",
        published_date="2026-11-10",
        is_archived_fallback=False
    )


def test_report_generator_markdown_output(tmp_path, mock_trend_item, mock_arxiv_paper):
    gen = ReportGenerator(reports_dir=tmp_path)
    md = gen.generate_markdown(
        date_str="2026-11-10",
        hn_items=[mock_trend_item],
        arxiv_items=[mock_arxiv_paper],
        hn_status=SourceStatus.SUCCESS,
        arxiv_status=SourceStatus.SUCCESS
    )

    assert "# 📡 AI & Tech Daily Radar — 2026-11-10" in md
    assert "Rust UI Framework" in md
    assert "Agentic Reasoning" in md
    assert "2026-11-10" in md


def test_readme_updater_replaces_block(tmp_path, mock_trend_item, mock_arxiv_paper):
    readme = tmp_path / "README.md"
    readme.write_text(
        "# Header\n<!-- LATEST_REPORT_START -->\nOld content\n<!-- LATEST_REPORT_END -->\n# Footer",
        encoding="utf-8"
    )

    updater = ReadmeUpdater(readme_path=readme, reports_dir=tmp_path)
    success = updater.update(
        date_str="2026-11-10",
        hn_items=[mock_trend_item],
        arxiv_items=[mock_arxiv_paper]
    )

    assert success is True
    updated = readme.read_text(encoding="utf-8")
    assert "Old content" not in updated
    assert "Rust UI Framework" in updated
    assert "Agentic Reasoning" in updated


def test_readme_updater_raises_on_missing_tags(tmp_path, mock_trend_item, mock_arxiv_paper):
    readme = tmp_path / "README.md"
    readme.write_text("# Invalid Readme without markers", encoding="utf-8")

    updater = ReadmeUpdater(readme_path=readme, reports_dir=tmp_path)
    with pytest.raises(ValueError, match="Marker tags"):
        updater.update(
            date_str="2026-11-10",
            hn_items=[mock_trend_item],
            arxiv_items=[mock_arxiv_paper]
        )
