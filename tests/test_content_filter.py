"""
Unit tests for ContentFilter.
Validates negative patterns, strong exceptions, scoring, and rankings.
"""

from src.processors.content_filter import ContentFilter


def test_rejects_obituaries(sample_hn_hits):
    cf = ContentFilter()
    hit = sample_hn_hits[0]  # "Patrick Stewart has died"
    is_valid, category, score, reason = cf.evaluate_hit(hit)
    assert not is_valid
    assert "Negatif filtre" in reason


def test_rejects_pure_medical(sample_hn_hits):
    cf = ContentFilter()
    hit = sample_hn_hits[1]  # "Things to know when you get cancer"
    is_valid, category, score, reason = cf.evaluate_hit(hit)
    assert not is_valid
    assert "Negatif filtre" in reason


def test_accepts_tech_exceptions_in_medical_topics(sample_hn_hits):
    cf = ContentFilter()
    hit = sample_hn_hits[2]  # "A 10-year-old CNN outperforms frontier LLMs for skin cancer diagnosis"
    is_valid, category, score, reason = cf.evaluate_hit(hit)
    assert is_valid
    assert category == "🤖 AI / ML"
    assert score >= 1


def test_rejects_zero_engagement_job_ads(sample_hn_hits):
    cf = ContentFilter()
    hit = sample_hn_hits[5]  # "UpCodes is hiring..."
    is_valid, category, score, reason = cf.evaluate_hit(hit)
    assert not is_valid


def test_categorizes_software_and_security(sample_hn_hits):
    cf = ContentFilter()
    blender_hit = sample_hn_hits[3]
    valid_b, cat_b, score_b, _ = cf.evaluate_hit(blender_hit)
    assert valid_b
    assert cat_b == "💻 Yazılım & Geliştirme"

    pwn_hit = sample_hn_hits[4]
    valid_p, cat_p, score_p, _ = cf.evaluate_hit(pwn_hit)
    assert valid_p
    assert cat_p == "🛡️ Güvenlik"


def test_filter_and_rank_returns_curated_trend_items(sample_hn_hits):
    cf = ContentFilter()
    results = cf.filter_and_rank(sample_hn_hits, limit=3)

    assert len(results) == 3
    # Check that all returned items are TrendItem instances
    titles = [item.title for item in results]
    assert "Patrick Stewart has died" not in titles
    assert "Things to know when you get cancer" not in titles
    assert "UpCodes is hiring SDR's to sell software" not in titles
    assert any("CNN outperforms" in t for t in titles)
