"""
Unit tests for data models and schema validation.
"""

import pytest
from src.models import TrendItem, ArxivPaper


def test_trend_item_valid():
    item = TrendItem(
        title="Valid Title",
        url="https://example.com",
        hn_url="https://news.ycombinator.com/item?id=123",
        points=100,
        comments=20,
        category="🤖 AI / ML"
    )
    assert item.title == "Valid Title"
    assert item.points == 100


def test_trend_item_validation_errors():
    with pytest.raises(ValueError, match="title cannot be empty"):
        TrendItem(title="", url="https://example.com", hn_url="https://hn.com", points=1, comments=1)

    with pytest.raises(ValueError, match="Invalid URL"):
        TrendItem(title="Title", url="invalid-url", hn_url="https://hn.com", points=1, comments=1)

    with pytest.raises(ValueError, match="non-negative"):
        TrendItem(title="Title", url="https://example.com", hn_url="https://hn.com", points=-5, comments=1)


def test_arxiv_paper_valid():
    paper = ArxivPaper(
        title="Deep Learning Study",
        summary="A comprehensive study.",
        link="https://arxiv.org/abs/123",
        authors="Alice, Bob",
        category="cs.AI",
        published_date="2026-11-09"
    )
    assert paper.title == "Deep Learning Study"
    assert paper.link.startswith("https://")
    assert not paper.is_archived_fallback


def test_arxiv_paper_validation_errors():
    with pytest.raises(ValueError, match="summary cannot be empty"):
        ArxivPaper(
            title="Title",
            summary="",
            link="https://arxiv.org/abs/1",
            authors="Alice"
        )
