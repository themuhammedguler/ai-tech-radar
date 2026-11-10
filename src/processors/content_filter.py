"""
Content filter and relevance scoring engine.
Screens out non-tech noise (obituaries, pure medical advice, politics, job ads)
while boosting and categorizing high-impact technology and AI developments.
"""

import re
from typing import Any
from src.config import (
    NEGATIVE_PATTERNS,
    STRONG_TECH_EXCEPTIONS,
    TECH_CATEGORIES,
    TECH_DOMAINS,
    HN_MIN_POINTS,
    HN_TARGET_COUNT
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
        min_points: int = HN_MIN_POINTS
    ):
        self.negative_patterns = negative_patterns or NEGATIVE_PATTERNS
        self.strong_exceptions = strong_exceptions or STRONG_TECH_EXCEPTIONS
        self.categories = categories or TECH_CATEGORIES
        self.tech_domains = tech_domains or TECH_DOMAINS
        self.min_points = min_points

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

        Returns:
            Tuple of (category_name, tech_score).
        """
        matched_category = "⚡ Teknoloji"
        tech_score = 0

        for cat_name, keywords in self.categories.items():
            cat_matches = sum(
                1 for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", title_lower)
            )
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
