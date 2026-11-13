"""
Integration tests for RadarPipeline orchestration and error escalation (v4.0).
"""

from unittest.mock import MagicMock
import pytest
from src.pipeline import RadarPipeline, PipelineExecutionError
from src.models import (
    ArxivPaper,
    ExecutiveBriefing,
    GithubRepoItem,
    HuggingFacePaperItem,
    SourceStatus,
    TrendItem
)


def test_pipeline_runs_successfully(tmp_path):
    mock_hn = MagicMock()
    mock_hn.status = SourceStatus.SUCCESS
    mock_hn.collect.return_value = [
        TrendItem(
            title="Rust AI",
            url="https://github.com/rust-ai",
            hn_url="https://news.ycombinator.com/item?id=1",
            points=200,
            comments=50,
            category="🤖 AI / ML"
        )
    ]

    mock_github = MagicMock()
    mock_github.status = SourceStatus.SUCCESS
    mock_github.collect.return_value = [
        GithubRepoItem(
            name="cool/repo",
            url="https://github.com/cool/repo",
            description="desc",
            language="Rust",
            stars=500,
            forks=40
        )
    ]

    mock_hf = MagicMock()
    mock_hf.status = SourceStatus.SUCCESS
    mock_hf.collect.return_value = [
        HuggingFacePaperItem(
            title="HF Model",
            url="https://huggingface.co/papers/1",
            authors="Author",
            upvotes=25,
            num_comments=5,
            summary="HF summary",
            published_date="2026-11-13"
        )
    ]

    mock_arxiv = MagicMock()
    mock_arxiv.status = SourceStatus.SUCCESS
    mock_arxiv.collect.return_value = [
        ArxivPaper(
            title="Transformer Scaling",
            summary="A study on scaling laws.",
            link="https://arxiv.org/abs/2611.1111",
            authors="Dr. AI",
            category="cs.LG",
            published_date="2026-11-13"
        )
    ]

    mock_ai = MagicMock()
    mock_ai.synthesize.return_value = ExecutiveBriefing(
        sector_events="Sector update",
        software_opensource="Software update",
        ai_research="AI update",
        generated_by_ai=True
    )

    mock_report_gen = MagicMock()
    mock_report_gen.write_report.return_value = tmp_path / "2026-11-13.md"

    mock_readme_updater = MagicMock()
    mock_readme_updater.update.return_value = True

    pipeline = RadarPipeline(
        hn_collector=mock_hn,
        github_collector=mock_github,
        hf_collector=mock_hf,
        arxiv_collector=mock_arxiv,
        ai_summarizer=mock_ai,
        report_generator=mock_report_gen,
        readme_updater=mock_readme_updater
    )

    result = pipeline.run(date_str="2026-11-13")
    assert result.is_healthy
    assert len(result.hn_items) == 1
    assert len(result.github_items) == 1
    assert len(result.huggingface_items) == 1
    assert len(result.arxiv_items) == 1
    assert result.executive_briefing is not None
    assert result.report_file is not None


def test_pipeline_aborts_on_total_empty_data():
    """Validates that empty data triggers PipelineExecutionError instead of faking success."""
    mock_hn = MagicMock()
    mock_hn.status = SourceStatus.EMPTY
    mock_hn.collect.return_value = []

    mock_github = MagicMock()
    mock_github.status = SourceStatus.EMPTY
    mock_github.collect.return_value = []

    mock_hf = MagicMock()
    mock_hf.status = SourceStatus.EMPTY
    mock_hf.collect.return_value = []

    mock_arxiv = MagicMock()
    mock_arxiv.status = SourceStatus.EMPTY
    mock_arxiv.collect.return_value = []

    pipeline = RadarPipeline(
        hn_collector=mock_hn,
        github_collector=mock_github,
        hf_collector=mock_hf,
        arxiv_collector=mock_arxiv
    )

    with pytest.raises(PipelineExecutionError, match="CRITICAL PIPELINE FAILURE"):
        pipeline.run(date_str="2026-11-13", exit_on_critical_failure=False)
