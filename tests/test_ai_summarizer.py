"""
Unit tests for AiSummarizer (Gemini Flash integration and graceful fallback).
"""

from unittest.mock import MagicMock
from src.processors.ai_summarizer import AiSummarizer
from src.models import (
    ArxivPaper,
    GithubRepoItem,
    HuggingFacePaperItem,
    TrendItem
)


def test_ai_summarizer_graceful_fallback_when_no_api_key():
    summarizer = AiSummarizer(api_key=None)
    briefing = summarizer.synthesize(
        hn_items=[],
        github_items=[],
        hf_items=[],
        arxiv_items=[]
    )
    assert not briefing.generated_by_ai
    assert "GEMINI_API_KEY" in briefing.disclaimer
    assert "sektör" in briefing.sector_events.lower()
    assert "yazılım" in briefing.software_opensource.lower()
    assert "yapay zeka" in briefing.ai_research.lower()


def test_ai_summarizer_parses_gemini_response():
    summarizer = AiSummarizer(api_key="mock_key")
    mock_llm_text = """
SEKTOR: Yapay zeka regülasyonları ve donanım ihracat kısıtlamaları teknoloji devlerinde strateji değişikliklerine yol açtı.
YAZILIM: Rust tabanlı CLI araçları ve yeni JavaScript runtime'ları açık kaynak geliştiricileri arasında rekor yıldız topladı.
ARASTIRMA: Otonom ajanlar için sentetik veri sentezi ve difüzyon tabanlı robotik kontrol makaleleri öne çıktı.
"""
    summarizer._call_gemini_api = MagicMock(return_value=mock_llm_text)

    hn = [TrendItem(title="Tech News", url="https://hn.com", hn_url="https://hn.com", points=100, comments=20)]
    gh = [GithubRepoItem(name="repo", url="https://github.com/r", description="d", language="Rust", stars=10, forks=2)]
    hf = [HuggingFacePaperItem(title="HF Paper", url="https://hf.co/p", authors="A", upvotes=5, num_comments=1, summary="s")]
    ax = [ArxivPaper(title="Arxiv Paper", summary="s", link="https://arxiv.org/1", authors="A")]

    briefing = summarizer.synthesize(hn, gh, hf, ax)
    assert briefing.generated_by_ai is True
    assert "regülasyonları" in briefing.sector_events
    assert "Rust" in briefing.software_opensource
    assert "Otonom ajanlar" in briefing.ai_research
