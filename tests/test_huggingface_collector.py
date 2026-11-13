"""
Unit tests for HuggingFaceCollector.
"""

from unittest.mock import MagicMock
from src.collectors.huggingface import HuggingFaceCollector
from src.models import SourceStatus


def test_huggingface_collector_success():
    collector = HuggingFaceCollector()
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "2611.12345",
            "title": "Scaling Autonomous Agents via Synthetic Trajectories",
            "summary": "Large language models show strong reasoning capabilities. We explore synthetic trajectories to boost agentic tasks.",
            "numUpvotes": 45,
            "numComments": 12,
            "publishedAt": "2026-11-12T10:00:00Z",
            "paper": {
                "id": "2611.12345",
                "authors": [{"name": "Yann LeCun"}, {"name": "Geoffrey Hinton"}]
            }
        }
    ]
    collector.get = MagicMock(return_value=mock_response)

    papers = collector.collect()
    assert len(papers) == 1
    p = papers[0]
    assert p.title == "Scaling Autonomous Agents via Synthetic Trajectories"
    assert p.upvotes == 45
    assert "Yann LeCun" in p.authors
    assert p.url == "https://huggingface.co/papers/2611.12345"
    assert collector.status in (SourceStatus.SUCCESS, SourceStatus.DEGRADED)


def test_huggingface_collector_handles_empty():
    collector = HuggingFaceCollector()
    mock_response = MagicMock()
    mock_response.json.return_value = []
    collector.get = MagicMock(return_value=mock_response)

    papers = collector.collect()
    assert papers == []
    assert collector.status == SourceStatus.EMPTY
