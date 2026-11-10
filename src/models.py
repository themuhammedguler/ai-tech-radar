"""
Data models and typed structures for the AI & Tech Radar pipeline.
Enforces strict schema validation, immutability, and typing.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class SourceStatus(str, Enum):
    """Health and execution status for a data collector."""
    SUCCESS = "SUCCESS"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    EMPTY = "EMPTY"


@dataclass(frozen=True)
class TrendItem:
    """Immutable data model representing a curated technology news item."""
    title: str
    url: str
    hn_url: str
    points: int
    comments: int
    category: str = "⚡ Teknoloji"
    tech_score: int = 0
    ranking_score: float = 0.0

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("TrendItem title cannot be empty.")
        if not self.url or not self.url.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL for TrendItem: {self.url}")
        if self.points < 0 or self.comments < 0:
            raise ValueError("Points and comments must be non-negative integers.")


@dataclass(frozen=True)
class ArxivPaper:
    """Immutable data model representing an academic research paper."""
    title: str
    summary: str
    link: str
    authors: str
    category: str = "cs.AI"
    published_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    is_archived_fallback: bool = False

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("ArxivPaper title cannot be empty.")
        if not self.link or not self.link.startswith(("http://", "https://")):
            raise ValueError(f"Invalid link for ArxivPaper: {self.link}")
        if not self.summary or not self.summary.strip():
            raise ValueError("ArxivPaper summary cannot be empty.")


@dataclass
class PipelineReportResult:
    """Result payload returned by the pipeline orchestrator."""
    date_str: str
    hn_items: list[TrendItem] = field(default_factory=list)
    arxiv_items: list[ArxivPaper] = field(default_factory=list)
    hn_status: SourceStatus = SourceStatus.SUCCESS
    arxiv_status: SourceStatus = SourceStatus.SUCCESS
    report_file: Optional[Path] = None
    readme_updated: bool = False
    errors: list[str] = field(default_factory=list)

    @property
    def is_healthy(self) -> bool:
        """Returns True if both sources completed successfully with data."""
        return (
            self.hn_status == SourceStatus.SUCCESS
            and self.arxiv_status in (SourceStatus.SUCCESS, SourceStatus.DEGRADED)
            and len(self.hn_items) > 0
            and len(self.arxiv_items) > 0
        )
