"""
Content filter and relevance scoring engine (v4.3 Anti-Staleness & Freshness).
Screens out non-tech noise (obituaries, pure medical advice, politics, job ads, shopping deals,
and historical/archived articles with past year tags) while boosting and categorizing
high-impact contemporary technology and AI developments.
"""

from datetime import datetime
import re
from typing import Any
from src.config import (
    HN_MIN_POINTS,
    HN_TARGET_COUNT,
    MAX_ALLOWED_ARTICLE_AGE_YEARS,
    NEGATIVE_PATTERNS,
    STALE_URL_DATE_PATTERN,
    STALE_YEAR_TAG_PATTERN,
    STRONG_TECH_EXCEPTIONS,
    TECH_CATEGORIES,
    TECH_DOMAINS
)
from src.models import TrendItem
from src.logging_config import logger


class ContentFilter:
    """Intelligent content filtering and scoring engine for tech trends."""

    def __init__(
        self,
        negative_patterns: list[str] | None = None,
        strong_exceptions: list[str] | None = None,
        categories: dict[str, list[str]] | None = None,
        tech_domains: list[str] | None = None,
        min_points: int = HN_MIN_POINTS,
        stale_year_pattern: str = STALE_YEAR_TAG_PATTERN,
        stale_url_pattern: str = STALE_URL_DATE_PATTERN,
        max_age_years: int = MAX_ALLOWED_ARTICLE_AGE_YEARS
    ):
        self.negative_patterns = negative_patterns or NEGATIVE_PATTERNS
        self.strong_exceptions = strong_exceptions or STRONG_TECH_EXCEPTIONS
        self.categories = categories or TECH_CATEGORIES
        self.tech_domains = tech_domains or TECH_DOMAINS
        self.min_points = min_points
        self.stale_year_pattern = stale_year_pattern
        self.stale_url_pattern = stale_url_pattern
        self.max_age_years = max_age_years

    def is_stale_article(self, title: str, url: str) -> tuple[bool, str]:
        """
        Detects if a title contains historical year markers (e.g. (2007), [1999])
        or if the URL path contains past archive dates (e.g. /2007/04/).

        Returns:
            Tuple of (is_stale, reason_string).
        """
        current_year = datetime.now().year

        # 1. Title year tag check: (YYYY) or [YYYY]
        tag_match = re.search(self.stale_year_pattern, title)
        if tag_match:
            try:
                year = int(tag_match.group(1))
                if year < current_year - self.max_age_years:
                    return True, f"Başlıkta eski/arşiv yıl etiketi ({year})"
            except (ValueError, IndexError):
                pass

        # 2. URL date path check: /YYYY/MM/
        url_match = re.search(self.stale_url_pattern, url)
        if url_match:
            try:
                url_year = int(url_match.group(1))
                if url_year < current_year - self.max_age_years:
                    return True, f"URL yolunda eski/arşiv tarih ({url_year})"
            except (ValueError, IndexError):
                pass

        return False, ""

    def has_strong_tech_exception(self, title_lower: str) -> bool:
        """Checks if title contains strong AI/software terms that override negative filters."""
        return any(re.search(rf"\b{re.escape(k)}\b", title_lower) for k in self.strong_exceptions)

    def is_negative_match(self, title_lower: str) -> bool:
        """Determines if a title matches off-topic or negative pattern filters."""
        for pattern in self.negative_patterns:
            if re.search(pattern, title_lower):
                return True
        return False

    def categorize_and_score(self, title_lower: str, url_lower: str) -> tuple[str, int]:
        """
        Determines the best matching category and computes an additive tech score.
        Supports model suffix version numbers (e.g. qwen4, gpt-4, claude3).

        Returns:
            Tuple of (category_name, tech_score).
        """
        matched_category = "⚡ Teknoloji"
        tech_score = 0

        for cat_name, keywords in self.categories.items():
            cat_matches = 0
            for kw in keywords:
                if re.search(r"\W$", kw):
                    pattern = rf"\b{re.escape(kw)}"
                else:
                    pattern = rf"\b{re.escape(kw)}(?:-?\d+)?\b"

                if re.search(pattern, title_lower):
                    cat_matches += 1

            if cat_matches > 0:
                tech_score += cat_matches
                if matched_category == "⚡ Teknoloji":
                    matched_category = cat_name

        # Domain credibility bonus
        if any(domain in url_lower for domain in self.tech_domains):
            tech_score += 1
            if matched_category == "⚡ Teknoloji":
                matched_category = "💻 Yazılım & Geliştirme"

        return matched_category, tech_score

    def evaluate_hit(self, hit: dict[str, Any]) -> tuple[bool, str, int, str]:
        """
        Evaluates a raw API hit dictionary.

        Returns:
            Tuple of (is_accepted, category, tech_score, reason).
        """
        raw_title = hit.get("title") or hit.get("story_title") or ""
        title = raw_title.strip()
        url = (hit.get("url") or "").lower()
        points = int(hit.get("points") or 0)
        comments = int(hit.get("num_comments") or 0)

        if not title:
            return False, "Geçersiz", 0, "Boş başlık"

        # Discard zero-engagement job posts or dead submissions
        if points < self.min_points and comments == 0:
            return False, "Düşük Etkileşim", 0, "Puan ve yorum yetersiz"

        # Check staleness first before any category scoring or exceptions
        is_stale, stale_reason = self.is_stale_article(title, url)
        if is_stale:
            return False, "Eski İçerik", 0, stale_reason

        title_lower = title.lower()

        # Check negative patterns unless saved by strong tech exceptions
        if not self.has_strong_tech_exception(title_lower):
            if self.is_negative_match(title_lower):
                return False, "Gürültü", 0, "Negatif filtre eşleşmesi"

        category, tech_score = self.categorize_and_score(title_lower, url)
        return True, category, tech_score, "Kabul edildi"

    def filter_and_rank(self, hits: list[dict[str, Any]], limit: int = HN_TARGET_COUNT) -> list[TrendItem]:
        """
        Filters candidate hits and ranks them by composite interaction and relevance score.
        """
        verified_items: list[TrendItem] = []
        general_items: list[TrendItem] = []

        for hit in hits:
            is_valid, category, tech_score, reason = self.evaluate_hit(hit)
            if not is_valid:
                logger.debug(f"Filtered out: '{hit.get('title')}' -> {reason}")
                continue

            title = (hit.get("title") or hit.get("story_title") or "Başlıksız").strip().replace("|", "-")
            object_id = str(hit.get("objectID") or "")
            hn_url = f"https://news.ycombinator.com/item?id={object_id}"
            story_url = hit.get("url") or hn_url
            points = max(0, int(hit.get("points") or 0))
            comments = max(0, int(hit.get("num_comments") or 0))

            # Composite ranking: points + (tech bonus) + comments weight
            ranking_score = float(points + (tech_score * 120) + (comments * 0.4))

            try:
                item = TrendItem(
                    title=title,
                    url=story_url,
                    hn_url=hn_url,
                    points=points,
                    comments=comments,
                    category=category,
                    tech_score=tech_score,
                    ranking_score=ranking_score
                )
            except ValueError as e:
                logger.warning(f"Validation error for item '{title}': {e}")
                continue

            if tech_score >= 1:
                verified_items.append(item)
            else:
                general_items.append(item)

        # Sort both tiers descending by ranking score
        verified_items.sort(key=lambda x: x.ranking_score, reverse=True)
        general_items.sort(key=lambda x: x.ranking_score, reverse=True)

        # Prefer verified technology items first, then supplement with top general items if needed
        final_selection = verified_items[:limit]
        if len(final_selection) < limit:
            needed = limit - len(final_selection)
            final_selection.extend(general_items[:needed])

        logger.info(
            f"ContentFilter completed: {len(hits)} evaluated, {len(verified_items)} tech-verified, "
            f"{len(final_selection)} selected for radar."
        )
        return final_selection
