"""
Unit tests for ReportGenerator and ReadmeUpdater (v4.0 multi-source & AI summary).
"""

import pytest
from src.generators.report_generator import ReportGenerator
from src.generators.readme_updater import ReadmeUpdater
from src.models import (
    ArxivPaper,
    ExecutiveBriefing,
    GithubRepoItem,
    HuggingFacePaperItem,
    SourceStatus,
    TrendItem
)


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
def mock_github_repo():
    return GithubRepoItem(
        name="astral-sh/uv",
        url="https://github.com/astral-sh/uv",
        description="Fast Python package manager.",
        language="Rust",
        stars=35000,
        forks=1200
    )


@pytest.fixture
def mock_hf_paper():
    return HuggingFacePaperItem(
        title="Agent Scaling",
        url="https://huggingface.co/papers/123",
        authors="Dr. HF",
        upvotes=40,
        num_comments=8,
        summary="A study on synthetic data.",
        published_date="2026-11-13"
    )


@pytest.fixture
def mock_arxiv_paper():
    return ArxivPaper(
        title="Agentic Reasoning",
        summary="A study on autonomous agent reasoning.",
        link="https://arxiv.org/abs/2611.12345",
        authors="Alice, Bob",
        category="cs.AI",
        published_date="2026-11-13",
        is_archived_fallback=False
    )


@pytest.fixture
def mock_briefing():
    return ExecutiveBriefing(
        sector_events="Teknoloji pazarında büyük gelişmeler yaşandı.",
        software_opensource="Rust ve Python araçları öne çıktı.",
        ai_research="Ajan mimarileri Hugging Face'te popüler oldu.",
        generated_by_ai=True
    )


def test_report_generator_markdown_output(
    tmp_path,
    mock_trend_item,
    mock_github_repo,
    mock_hf_paper,
    mock_arxiv_paper,
    mock_briefing
):
    gen = ReportGenerator(reports_dir=tmp_path)
    md = gen.generate_markdown(
        date_str="2026-11-13",
        hn_items=[mock_trend_item],
        github_items=[mock_github_repo],
        hf_items=[mock_hf_paper],
        arxiv_items=[mock_arxiv_paper],
        briefing=mock_briefing,
        hn_status=SourceStatus.SUCCESS,
        github_status=SourceStatus.SUCCESS,
        hf_status=SourceStatus.SUCCESS,
        arxiv_status=SourceStatus.SUCCESS
    )

    assert "# AI & Tech Daily Radar — 2026-11-13" in md
    assert "Günün Yapay Zeka Özeti" in md
    assert "Rust ve Python araçları öne çıktı" in md
    assert "Rust UI Framework" in md
    assert "astral-sh/uv" in md
    assert "Agent Scaling" in md
    assert "Agentic Reasoning" in md


def test_readme_updater_replaces_block(
    tmp_path,
    mock_trend_item,
    mock_github_repo,
    mock_hf_paper,
    mock_arxiv_paper,
    mock_briefing
):
    readme = tmp_path / "README.md"
    readme.write_text(
        "# Header\n<!-- LATEST_REPORT_START -->\nOld content\n<!-- LATEST_REPORT_END -->\n# Footer",
        encoding="utf-8"
    )

    updater = ReadmeUpdater(readme_path=readme, reports_dir=tmp_path)
    success = updater.update(
        date_str="2026-11-13",
        hn_items=[mock_trend_item],
        github_items=[mock_github_repo],
        hf_items=[mock_hf_paper],
        arxiv_items=[mock_arxiv_paper],
        briefing=mock_briefing
    )

    assert success is True
    updated = readme.read_text(encoding="utf-8")
    assert "Old content" not in updated
    assert "Günün Yapay Zeka Özeti" in updated
    assert "astral-sh/uv" in updated
    assert "Agent Scaling" in updated


def test_readme_updater_raises_on_missing_tags(
    tmp_path,
    mock_trend_item,
    mock_github_repo,
    mock_hf_paper,
    mock_arxiv_paper,
    mock_briefing
):
    readme = tmp_path / "README.md"
    readme.write_text("# Invalid Readme without markers", encoding="utf-8")

    updater = ReadmeUpdater(readme_path=readme, reports_dir=tmp_path)
    with pytest.raises(ValueError, match="Marker tags"):
        updater.update(
            date_str="2026-11-13",
            hn_items=[mock_trend_item],
            github_items=[mock_github_repo],
            hf_items=[mock_hf_paper],
            arxiv_items=[mock_arxiv_paper],
            briefing=mock_briefing
        )
