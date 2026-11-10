"""
Pytest configuration and shared test fixtures.
"""

import pytest


@pytest.fixture
def sample_hn_hits():
    """Provides representative HackerNews API JSON hits."""
    return [
        {
            "objectID": "1001",
            "title": "Patrick Stewart has died",
            "url": "https://example.com/obit",
            "points": 3000,
            "num_comments": 500
        },
        {
            "objectID": "1002",
            "title": "Things to know when you get cancer",
            "url": "https://example.com/health",
            "points": 1400,
            "num_comments": 300
        },
        {
            "objectID": "1003",
            "title": "A 10-year-old CNN outperforms frontier LLMs for skin cancer diagnosis",
            "url": "https://example.com/ai-paper",
            "points": 580,
            "num_comments": 240
        },
        {
            "objectID": "1004",
            "title": "Blender's UI and Runtime: Much Faster Than GPUI",
            "url": "https://github.com/ppmpreetham/BUI",
            "points": 620,
            "num_comments": 250
        },
        {
            "objectID": "1005",
            "title": "Firecracker VM Escape: PwnEscape Part 2",
            "url": "https://pwn.ai/blog/firecracker",
            "points": 60,
            "num_comments": 20
        },
        {
            "objectID": "1006",
            "title": "UpCodes is hiring SDR's to sell software",
            "url": "https://up.codes/careers",
            "points": 0,
            "num_comments": 0
        }
    ]


@pytest.fixture
def sample_arxiv_xml():
    """Provides representative ArXiv Atom XML feed bytes."""
    return b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2611.08483v1</id>
    <published>2026-11-09T18:00:00Z</published>
    <updated>2026-11-09T18:00:00Z</updated>
    <title>SwarmEvolve: Latent Agent Swarms for Evolutionary Discovery</title>
    <summary>LLM-guided evolutionary search uses AI agents to improve programs. However, the process is often slow because the LLM generates long chains of thought. We introduce SwarmEvolve to address this.</summary>
    <author>
      <name>Qile Jiang</name>
    </author>
    <author>
      <name>George Karniadakis</name>
    </author>
    <arxiv:primary_category term="cs.AI" />
  </entry>
</feed>
"""
