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


def test_rejects_historical_year_tags_in_title():
    cf = ContentFilter()
    thinkpad_hit = {
        "title": "The Secret ThinkPad Powerbutton Code to Bring Dead Laptops Back to Life (2007)",
        "url": "https://masnick.com/posts/the-secret-thinkpad-powerbutton-code-to-bring-dead-laptops-back-to-life/",
        "points": 153,
        "num_comments": 45
    }
    is_valid, category, score, reason = cf.evaluate_hit(thinkpad_hit)
    assert not is_valid
    assert category == "Eski İçerik"
    assert "2007" in reason

    lisp_hit = {
        "title": "Why We Chose Common Lisp [1999]",
        "url": "https://example.com/lisp",
        "points": 200,
        "num_comments": 50
    }
    is_valid_lisp, cat_lisp, _, reason_lisp = cf.evaluate_hit(lisp_hit)
    assert not is_valid_lisp
    assert "1999" in reason_lisp


def test_allows_current_year_tag():
    cf = ContentFilter()
    hit = {
        "title": "State of Software Engineering in (2026)",
        "url": "https://example.com/2026-report",
        "points": 120,
        "num_comments": 30
    }
    is_valid, category, score, _ = cf.evaluate_hit(hit)
    assert is_valid
    assert category == "💻 Yazılım & Geliştirme"


def test_rejects_historical_date_in_url():
    cf = ContentFilter()
    hit = {
        "title": "Deep Dive into Virtual Memory Systems",
        "url": "https://techblog.com/2011/05/virtual-memory-architecture",
        "points": 95,
        "num_comments": 20
    }
    is_valid, category, _, reason = cf.evaluate_hit(hit)
    assert not is_valid
    assert category == "Eski İçerik"
    assert "2011" in reason


def test_rejects_commercial_shopping_deals():
    cf = ContentFilter()
    hit = {
        "title": "Many of Amazon’s Black Friday and Cyber Monday “Deals” Offered No Savings",
        "url": "https://wsj.com/shopping-analysis",
        "points": 240,
        "num_comments": 80
    }
    is_valid, category, _, reason = cf.evaluate_hit(hit)
    assert not is_valid
    assert "Negatif filtre" in reason


def test_rejects_vintage_retro_computing_nostalgia():
    cf = ContentFilter()
    hit = {
        "title": "Winudf – DVD / BluRay driver for DOS, Windows 1.x – 3x / 95 / 98 / ME",
        "url": "https://example.com/winudf",
        "points": 55,
        "num_comments": 15
    }
    is_valid, category, _, reason = cf.evaluate_hit(hit)
    assert not is_valid
    assert "Negatif filtre" in reason


def test_categorizes_ai_models_with_version_numbers():
    cf = ContentFilter()
    hit = {
        "title": "Qwen4-Max Benchmarks and Evaluation",
        "url": "https://qwen.ai/blog/qwen4-max",
        "points": 743,
        "num_comments": 110
    }
    is_valid, category, score, _ = cf.evaluate_hit(hit)
    assert is_valid
    assert category == "🤖 AI / ML"
    assert score >= 1


def test_categorizes_cybersecurity_cves_and_attacks():
    cf = ContentFilter()
    xss_hit = {
        "title": "Universal XSS in uBlock Origin from website-driven element picker",
        "url": "https://github.com/gorhill/uBlock",
        "points": 512,
        "num_comments": 90
    }
    valid_x, cat_x, score_x, _ = cf.evaluate_hit(xss_hit)
    assert valid_x
    assert cat_x == "🛡️ Güvenlik"
    assert score_x >= 1

    ddos_hit = {
        "title": "Tor Project Issues Rapid-Response DoS-Defense Fix Amid Sustained DDoS Attack",
        "url": "https://blog.torproject.org/ddos-defense",
        "points": 210,
        "num_comments": 40
    }
    valid_d, cat_d, score_d, _ = cf.evaluate_hit(ddos_hit)
    assert valid_d
    assert cat_d == "🛡️ Güvenlik"
    assert score_d >= 1
