"""
ArXiv research paper collector.
Queries ArXiv API via secure HTTPS, parses Atom XML feeds,
extracts authentic publication timestamps, and provides transparent fallback handling.
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Any
import xml.etree.ElementTree as ET
import requests

from src.collectors.base import BaseCollector
from src.config import (
    ARXIV_API_URL,
    ARXIV_CATEGORIES,
    ARXIV_FETCH_COUNT,
    ARXIV_TARGET_COUNT,
    REPORTS_DIR
)
from src.logging_config import logger
from src.models import ArxivPaper, SourceStatus
from src.processors.text_summarizer import extract_smart_summary


class ArxivCollector(BaseCollector):
    """Fetches and parses frontier AI/ML papers from ArXiv over HTTPS."""

    def __init__(
        self,
        api_url: str = ARXIV_API_URL,
        categories: list[str] | None = None,
        fetch_count: int = ARXIV_FETCH_COUNT,
        target_count: int = ARXIV_TARGET_COUNT,
        reports_dir: Path = REPORTS_DIR,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        # Ensure HTTPS is enforced
        if not api_url.startswith("https://"):
            api_url = api_url.replace("http://", "https://")
        self.api_url = api_url
        self.categories = categories or ARXIV_CATEGORIES
        self.fetch_count = fetch_count
        self.target_count = target_count
        self.reports_dir = reports_dir

    def _parse_xml_feed(self, xml_content: bytes) -> list[ArxivPaper]:
        """Parses Atom XML bytes into validated ArxivPaper model instances."""
        namespace = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"
        }

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            logger.error(f"Malformed XML from ArXiv API: {e}")
            raise ValueError(f"XML Parse Error: {e}") from e

        papers: list[ArxivPaper] = []
        entries = root.findall("atom:entry", namespace)

        for entry in entries[:self.target_count]:
            title_elem = entry.find("atom:title", namespace)
            summary_elem = entry.find("atom:summary", namespace)
            id_elem = entry.find("atom:id", namespace)
            published_elem = entry.find("atom:published", namespace)

            raw_title = title_elem.text if title_elem is not None and title_elem.text else "Başlıksız Makale"
            raw_summary = summary_elem.text if summary_elem is not None and summary_elem.text else "Özet bulunamadı."
            raw_link = id_elem.text.strip() if id_elem is not None and id_elem.text else ""

            # Ensure HTTPS for link
            link = raw_link.replace("http://", "https://") if raw_link else "https://arxiv.org"

            # Parse publication date (YYYY-MM-DD)
            pub_date = datetime.now().strftime("%Y-%m-%d")
            if published_elem is not None and published_elem.text:
                pub_date = published_elem.text.split("T")[0]

            clean_title = re.sub(r"\s+", " ", raw_title).strip().replace("|", "-")
            smart_summary = extract_smart_summary(raw_summary)

            # Authors
            author_elems = entry.findall("atom:author", namespace)
            authors = [
                a.find("atom:name", namespace).text
                for a in author_elems
                if a.find("atom:name", namespace) is not None and a.find("atom:name", namespace).text
            ]
            authors_str = ", ".join(authors[:3]) + (" vb." if len(authors) > 3 else "")

            # Category
            category_elem = entry.find("arxiv:primary_category", namespace)
            category_tag = (
                category_elem.attrib.get("term", "cs.AI")
                if category_elem is not None and "term" in category_elem.attrib
                else "cs.AI"
            )

            try:
                paper = ArxivPaper(
                    title=clean_title,
                    summary=smart_summary,
                    link=link,
                    authors=authors_str or "Araştırmacılar Belirtilmemiş",
                    category=category_tag,
                    published_date=pub_date,
                    is_archived_fallback=False
                )
                papers.append(paper)
            except ValueError as e:
                logger.warning(f"Skipping invalid ArxivPaper: {e}")

        return papers

    def _load_fallback_papers(self) -> list[ArxivPaper]:
        """
        Loads papers from the most recent historical report when live ArXiv is unavailable.
        Explicitly marks them with is_archived_fallback=True so freshness is never misrepresented.
        """
        if not self.reports_dir.exists():
            return []

        past_reports = sorted(self.reports_dir.glob("*.md"), reverse=True)
        for r_path in past_reports:
            try:
                content = r_path.read_text(encoding="utf-8")
                matches = re.findall(
                    r"###\s*\d+\.\s*\[(.*?)\]\((.*?)\)\s*\n-\s*👥\s*\*\*Yazarlar:\*\*\s*(.*?)\s*\n(?:-\s*📅\s*\*\*Yayın Tarihi:\*\*\s*(.*?)\s*\n)?-\s*🏷️\s*\*\*Kategori:\*\*\s*(.*?)\s*\n-\s*🔗\s*\*\*Bağlantı:\*\*\s*.*?\n-\s*📝\s*\*\*Özet:\*\*\s*\*(.*?)\*",
                    content
                )
                if matches:
                    fallback_papers = []
                    for m in matches[:self.target_count]:
                        fallback_papers.append(
                            ArxivPaper(
                                title=m[0],
                                link=m[1],
                                authors=m[2],
                                published_date=m[3] if m[3] else r_path.stem,
                                category=m[4],
                                summary=m[5],
                                is_archived_fallback=True  # Clear transparency!
                            )
                        )
                    logger.info(
                        f"Transparent Fallback: Loaded {len(fallback_papers)} reference papers from {r_path.name}"
                    )
                    return fallback_papers
            except Exception as e:
                logger.warning(f"Could not parse fallback from {r_path.name}: {e}")

        return []

    def collect(self) -> list[ArxivPaper]:
        """
        Executes ArXiv collection, falling back transparently if needed.

        Returns:
            List of ArxivPaper instances.
        """
        query_cats = " OR ".join(self.categories)
        params = {
            "search_query": query_cats,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": self.fetch_count
        }

        logger.info(f"Querying ArXiv API via HTTPS (categories: {self.categories})...")

        try:
            response = self.get(self.api_url, params=params)
            papers = self._parse_xml_feed(response.content)
            if papers:
                self.status = SourceStatus.SUCCESS
                logger.info(f"Successfully collected {len(papers)} fresh ArXiv papers.")
                return papers
            else:
                logger.warning("ArXiv API returned empty feed.")
        except (requests.RequestException, ValueError, RuntimeError) as e:
            logger.warning(f"ArXiv live collection encountered an issue: {e}")

        # Fallback procedure
        logger.info("Engaging fallback procedure for ArXiv...")
        fallback_papers = self._load_fallback_papers()
        if fallback_papers:
            self.status = SourceStatus.DEGRADED
            logger.warning("ArXiv papers loaded from archive fallback (marked as degraded/reference).")
            return fallback_papers

        self.status = SourceStatus.EMPTY
        logger.error("ArXiv collection failed completely and no fallback data available.")
        return []
